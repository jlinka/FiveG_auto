#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/24 上午11:26
# @Author  : jlinka
# @File    : search.py


from pymongo import MongoClient


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
        cursor = self.__coll.find({"test": {'$exists': True}})
        return cursor

    def findlike(self, filter):
        cursor = self.__coll.find({"test": {'$exists': True}, list(filter.keys())[0]: list(filter.values())[0]})
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
            self.items.append(
                {'title': leave[self.prev_num * 10 + i].get('title'),
                 'createTime': leave[self.prev_num * 10 + i].get('createTime'),
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


def searchCondition(keyword):
    db = mongDbManger_web_showClass()
    db.connect('server21.raisound.com', 24000, "webuser", "webuser1957", "web_show", "xinChuang_topic", "web_show")
    filter = {}
    keyword = keyword
    condition = {}
    condition['$regex'] = keyword
    filter["content"] = condition
    # cursor = db.find(filter)
    cursor = db.findlike(filter)
    cursor.close()
    return cursor


if __name__ == '__main__':
    searchCondition('3GPP')
