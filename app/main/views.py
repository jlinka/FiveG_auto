#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/23 下午6:01
# @Author  : jlinka
# @File    : views.py

from . import main
from flask import render_template, redirect, request, url_for
from app.form import Search, NewsForm
from app.main.search import searchAll, PaginateLeave, searchCondition


@main.route('/searchNews', methods=['GET', 'POST'])
def searchNews():
    search = Search()
    newsform = NewsForm()
    page = int(request.args.get('page')) if request.args.get('page') else 1
    # pagesize = 10
    # prev_page = page - 1 if page - 1 else 1
    # next_page = page + 1
    # if request.method == 'POST':
    #     cursor = searchAll()
    #     for item in cursor:
    #         print(item['test'])
    #     return render_template('search.html', data=cursor, search=search, newsform=newsform, prev_page=prev_page,
    #                            next_page=next_page
    #                            , page=page)
    # return render_template('search.html')
    pagination = PaginateLeave(page, searchAll())
    posts = pagination.items
    return render_template('search.html', newsform=newsform, posts=posts, pagination=pagination, search=search)


@main.route('/search', methods=['GET', 'POST'])
def search():
    newsform = NewsForm()
    page = int(request.args.get('page')) if request.args.get('page') else 1

    if request.method == 'POST':
        keywords = request.form.get('news')
        pagination = PaginateLeave(page, searchCondition(keywords))
        posts = pagination.items
        return render_template('search.html', newsform=newsform, posts=posts, pagination=pagination, keywords=keywords)
