#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/21 上午10:32
# @Author  : jlinka
# @File    : complex_search.py


import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from collections import defaultdict
import time

DIMENSION = 128


def kmeans_search_condition(cursor):  # 使用条件的kmeans聚类查询
    start = time.time()
    c = []
    classfi = cursor.count() // 5
    if classfi == 0:
        classfi == 1
    cop = cursor.clone()
    for i in range(cursor.count()):
        # print(i.get('content'))
        # c.append(jieba.lcut(i.get('content'), cut_all=False, HMM=True))
        c.append(cursor[i].get('content'))
    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(c))
    word = vectorizer.get_feature_names()
    weight = tfidf.toarray()
    print(weight)
    estimator = PCA(n_components=DIMENSION)
    pca_x_train = estimator.fit_transform(weight)
    print(pca_x_train)
    kmeans = KMeans(n_clusters=classfi, random_state=0).fit(pca_x_train)
    center = kmeans.cluster_centers_
    df_center = pd.DataFrame(center)
    labels = kmeans.labels_
    print(list(labels))
    print(c)
    i = 0
    kdata = []
    s = list(labels)
    d = defaultdict(list)
    for k, va in [(v, i) for i, v in enumerate(s)]:
        d[k].append([{"title": cop[va].get("title"), "createTime": cop[va].get("createTime"),
                      "source": cop[va].get("source"), "auther": cop[va].get("auther"),
                      "content": cop[va].get("content"), "_id": cop[va].get("_id"), "url": cop[va].get("url")}])
    end = time.time()
    print(end - start)
    print(d)
    return classfi, d
    # ndict = {}
    # for i in range(classfi):
    #     ndict[i] = []
    #     for j in d[i]:
    #         ndict[i].append([{"title": cop[j].get("title")}, {"createTime": cop[j].get("createTime")},
    #                          {"source": cop[j].get("source")}, {"auther": cop[j].get("auther")},
    #                          {"content": cop[j].get("content")}])
    #     kdata.append(ndict)

    # while i < classfi:
    #     j = 0
    #     ndict = {}
    #     ndict[i] = []
    #     while j < cop.count():
    #         if labels[j] == i:
    #             ndict[i].append([{"title": cop[j].get("title")}, {"createTime": cop[j].get("createTime")},
    #                             {"source": cop[j].get("source")}, {"auther": cop[j].get("auther")},
    #                             {"content": cop[j].get("content")}])
    #         j += 1
    #     kdata.append(ndict)
    #     i += 1
    print("test")
