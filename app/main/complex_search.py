#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/21 上午10:32
# @Author  : jlinka
# @File    : complex_search.py


import pandas as pd
import os
from pymongo import MongoClient
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE

# 显示中文
import datetime
import numpy
import sys
import codecs
import jieba

DIMENSION = 128


def kmeans_search_condition(cursor):  # 使用条件的kmeans聚类查询
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
    input = open('pca156ttt11111.txt', 'a', encoding='utf-8', errors='ignore')
    while i < classfi:
        input.write("第" + str(i) + "类:\n")
        j = 0
        while j < cop.count():
            if labels[j] == i:
                input.write(cop[j].get('auther') + "\n" + str(cop[j].get("_id")) +
                            cop[j].get('title') + "\n" + cop[j].get('content').replace('\r', '').replace('\n',
                                                                                                         '').replace(
                    ' ',
                    '').replace(
                    '  ', '').replace('   ', '') \
                            .replace('    ', '').replace('     ', '').replace('      ', '').replace('       ',
                                                                                                    '').replace(
                    '        ',
                    '') \
                            .replace('         ', '').replace('          ', '').replace(
                    '\r\n            \r\n              \r\n    \r\n    '
                    '        \r\n           \r\n    ', '') \
                            .replace(
                    '\r\n                         \r\n                              \r\n                                '
                    '   ', '').replace('	', '').replace('　　', '').replace('', '').replace('　　 ', '') + "\n\n")
            j += 1
        i += 1
        input.write("\n\n\n\n\n\n\n")

    input.close()
