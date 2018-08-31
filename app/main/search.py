#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/24 上午11:26
# @Author  : jlinka
# @File    : search.py


from pymongo import MongoClient

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

    def findlike(self, filter, source):
        test_dict = {}
        source_list = []
        test_dict["test"] = {'$exists': True}
        test_dict['isLimitSource'] = 1
        test_dict[list(filter.keys())[0]] = list(filter.values())[0]
        if source:
            for i in source:
                source_list.append(i)
                # test_dict['source'] = i
                if i == '网站':
                    for j in web:
                        source_list.append(j)
            test_dict['source'] = {'$in': source_list}

        cursor = self.__coll.find(test_dict)
        return cursor


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
            print(yes_time)
            self.items.append(
                {'title': leave[self.prev_num * 10 + i].get('title'),
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


def searchAll():
    db = mongDbManger_web_showClass()
    db.connect('server21.raisound.com', 24000, "webuser", "webuser1957", "web_show", "xinChuang_topic", "web_show")
    cursor = db.find().sort('createTime', -1)

    cursor.close()
    return cursor


def searchCondition(keyword, source):
    db = mongDbManger_web_showClass()
    db.connect('server21.raisound.com', 24000, "webuser", "webuser1957", "web_show", "xinChuang_topic", "web_show")
    filter = {}
    keyword = keyword
    condition = {}
    condition['$regex'] = keyword
    filter["content"] = condition
    # cursor = db.find(filter)
    cursor = db.findlike(filter, source).sort('createTime', -1)
    cursor.close()
    return cursor


def searchWeb():
    db = mongDbManger_web_showClass()
    db.connect('server21.raisound.com', 24000, "webuser", "webuser1957", "web_show", "xinChuang_topic", "web_show")
    cursor = db.find().sort('createTime', -1)
    beg_web = []
    for i in cursor:
        beg_web.append(i['source'])
    web = set(beg_web)
    cursor.close()
    return web




if __name__ == '__main__':
    # a = searchCondition('3GPP', [])
    # b = searchAll()
    # for i in b:
    #     print(i['title'])
    # for i in a:
    #     print(i['title'])
    a = searchWeb()
    print(a)
