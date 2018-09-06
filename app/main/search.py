#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/24 上午11:26
# @Author  : jlinka
# @File    : search.py


from pymongo import MongoClient
from bson.objectid import ObjectId

web = ['C114中国通信网', '中华人民共和国工业和信息化部', '中华人民共和国发展和改革委员会', '中华人民共和国科学技术部',
       '中华人民共和国商务部', '深圳市发展和改革委员会', 'ITU', 'ITU中国', '3GPP', 'IMT-2020推进组', '通信世界网',
       'OFweek光通讯网', '中国无线电管理', '电子发烧友', '电子产品世界', '新华网信息化', '新浪新闻', '新浪科技',
       '新浪财经', '网易科技', '网易财经', '搜狐', '搜狐科技', '腾讯财经', '腾讯科技', '凤凰网', '凤凰科技', '21CN科技',
       '环球科技', '飞象网', '中国科技网', '智通财经', 'CSDN', '和讯网', '华为', '中兴通讯', '上海诺基亚贝尔', '爱立信',
       '大唐电信', '三星', '英特尔', '英特尔IQ', '高通Qualcomm', '中国移动设计院', '中国移动设计院', '中国联通研究院',
       '中国电信北京研究院', '中国信通院']


class mongDbManger_web_showClass:
    __client = None
    __db = None
    __coll = None

    def __init__(self):
        print("__init__mongDbManger_webshow")

    def connect(self, url, port, user, password, database, table, auth):
        self.__client = MongoClient(url, port)
        self.__db = self.__client[auth]
        self.__db.authenticate(user, password)
        self.__db = self.__client[database]
        self.__coll = self.__db[table]

    def closeMongo(self):
        self.__client.close()

    def findOneWeek(self, dt):
        qureyCondition = {'createTime': {'$gt': dt}}
        cursor = self.__coll.find(qureyCondition)
        return cursor

    def find(self):
        cursor = self.__coll.find({"test": {'$exists': True}, 'isLimitSource': 1})
        return cursor

    def findSource(self):
        # cursor = self.__coll.find({"test": {'$exists': True}, 'isLimitSource': 1}, {"source": 1, "_id": 0})
        cursor = self.__coll.distinct('source', {"test": {'$exists': True}, 'isLimitSource': 1})
        return cursor

    def findAuther(self):
        # cursor = self.__coll.find({"test": {'$exists': True}, 'isLimitSource': 1}, {"auther": 1, "_id": 0})
        cursor = self.__coll.distinct('auther', {"test": {'$exists': True}, 'isLimitSource': 1})
        return cursor

    def findlike(self, filter, source, webs, auther):
        test_dict = {}
        source_list = []
        test_dict["test"] = {'$exists': True}
        test_dict['isLimitSource'] = 1
        if filter['content']['$regex'] != '':
            test_dict[list(filter.keys())[0]] = list(filter.values())[0]
        if source:
            for i in source:
                source_list.append(i)
                # test_dict['source'] = i
                if i == '网站':
                    source_list.extend(web)
            test_dict['source'] = {'$in': source_list}
        else:
            if webs and auther:
                test_dict['$or'] = [{'source': {'$in': webs}},
                                    {'auther': {'$in': auther}}]
            if len(webs) != 0 and len(auther) == 0:
                test_dict['source'] = {'$in': webs}
            if len(webs) == 0 and len(auther) != 0:
                test_dict['auther'] = {'$in': auther}
            # test_dict['source'] = {'$in': webs}
            # test_dict['auther'] = {'$in': auther}

        cursor = self.__coll.find(test_dict)
        cursor.close()
        return cursor

    def findOne(self, filter):
        cursor = self.__coll.find_one({'_id': ObjectId(filter)})
        cursor.close()
        return cursor

    def test(self, test_dict):
        cursor = db.__coll.find(test_dict)
        for i in cursor:
            print(i['source'])
            print(i['auther'])


class PaginateLeave:
    def __init__(self, page, leave):
        self.total = leave.count()
        self.pages = int(self.total / 10)
        if self.total % 10 != 0:
            self.pages += 1
        if page == -1:
            self.page = self.pages
        else:
            self.page = page
        if self.page == 1:
            self.has_prev = False
        else:
            self.has_prev = True
        if self.page == self.pages:
            self.has_next = False
        else:
            self.has_next = True
        self.next_num = self.page + 1
        self.per_page = 10
        self.prev_num = self.page - 1
        self.current_num = self.total - (10 * (self.page - 1))
        if self.current_num > 10:
            self.current_num = 10
        self.items = []
        for i in range(self.current_num):
            yes_time = str(leave[self.prev_num * 10 + i].get('createTime'))
            yes_time = "".join(str(yes_time[0:4]) + "年" + str(yes_time[4:6]) + "月" + str(yes_time[6:8])) + "日"
            self.items.append(
                {'ObjectId': leave[self.prev_num * 10 + i].get('_id'),
                 'title': leave[self.prev_num * 10 + i].get('title'),
                 # 'createTime': leave[self.prev_num * 10 + i].get('createTime'),
                 'createTime': yes_time,
                 'content': leave[self.prev_num * 10 + i].get('content'),
                 'url': leave[self.prev_num * 10 + i].get('url'),
                 'source': leave[self.prev_num * 10 + i].get('source'),
                 'auther': leave[self.prev_num * 10 + i].get('auther')})

    def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
                    (self.page - left_current - 1 < num < self.page + right_current) \
                    or num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num


db = mongDbManger_web_showClass()
db.connect('server21.raisound.com', 24000, "webuser", "webuser1957", "web_show", "xinChuang_topic", "web_show")


def searchAll():
    # 新建MongoDB类

    # 链接数据库

    # 查询所有结果并按照时间降序排序
    cursor = db.find().sort('createTime', -1)
    # 关闭游标
    cursor.close()
    db.closeMongo()
    return cursor


def searchCondition(keyword, source, web, auther):
    # db.connect('server21.raisound.com', 24000, "webuser", "webuser1957", "web_show", "xinChuang_topic", "web_show")
    filter = {}
    keyword = keyword
    condition = {}
    condition['$regex'] = keyword
    filter["content"] = condition
    # cursor = db.find(filter)
    cursor = db.findlike(filter, source, web, auther).sort('createTime', -1)
    cursor.close()
    db.closeMongo()
    return cursor


def searchWeb():
    # db.connect('server21.raisound.com', 24000, "webuser", "webuser1957", "web_show", "xinChuang_topic", "web_show")
    cursor = db.findSource()
    cursor.remove("微信公众号")
    # beg_web = []
    # for i in cursor:
    #     beg_web.append(i['source'])
    # beg_web.remove("微信公众号")
    # web = set(beg_web)
    db.closeMongo()
    return cursor


def searchOfficialAccounts():
    # db.connect('server21.raisound.com', 24000, "webuser", "webuser1957", "web_show", "xinChuang_topic", "web_show")
    cursor = db.findAuther()
    # officialAccounts = []
    # for i in cursor:
    #     if i['source'] == "微信公众号":
    #         officialAccounts.append(i['auther'])
    # officialAccounts = set(officialAccounts)
    # cursor.close()
    db.closeMongo()
    return cursor


def findObjectId(keywords):
    # db.connect('server21.raisound.com', 24000, "webuser", "webuser1957", "web_show", "xinChuang_topic", "web_show")
    cursor = db.findOne(keywords)
    db.closeMongo()
    return cursor


if __name__ == '__main__':
    # # a = searchCondition('3GPP', [])
    # b = searchAll()
    # for i in b:
    #     print(i)
    # for i in a:
    #     print(i['title'])
    # a = searchOfficialAccounts()
    # print(a)
    # a = findObjectId('000000000000000094890126')
    # print(a)
    # a = ['微信公众号']
    # a.extend(web)
    # print(a)
    # db = mongDbManger_web_showClass()
    # db.connect('server21.raisound.com', 24000, "webuser", "webuser1957", "web_show", "xinChuang_topic", "web_show")
    # test_dict = {'test': {'$exists': True}, 'isLimitSource': 1, '$or': [{'source': {'$in': ['C114中国通信网']}},
    #                                                                     {'auther': {'$in': ['Qualcomm中国']}}]}
    # # test_dict = {'source': 'C114中国通信网'}
    # db.test(test_dict)

    a = db.findSource()
    for i in a:
        print(i)
