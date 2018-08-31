#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/23 下午6:01
# @Author  : jlinka
# @File    : views.py

from . import main
from flask import render_template, redirect, request, url_for, session
from app.form import Search, NewsForm
from app.main.search import searchAll, PaginateLeave, searchCondition, searchWeb, searchOfficialAccounts


@main.route('/searchNews', methods=['GET', 'POST'])
def searchNews():
    search = Search()
    newsform = NewsForm()
    page = int(request.args.get('page')) if request.args.get('page') else 1
    keywords = request.form.get('news')
    if keywords:
        pagination = PaginateLeave(page, searchCondition(keywords))
        posts = pagination.items
        return render_template('search.html', newsform=newsform, posts=posts, pagination=pagination, keywords=keywords,
                               web=searchWeb(), officialAccounts=searchOfficialAccounts())

    pagination = PaginateLeave(page, searchAll())
    posts = pagination.items
    return render_template('search.html', newsform=newsform, posts=posts, pagination=pagination, search=search,
                           web=searchWeb(), officialAccounts=searchOfficialAccounts())


@main.route('/search', methods=['GET', 'POST'])
def search():
    newsform = NewsForm()
    page = int(request.args.get('page')) if request.args.get('page') else 1
    if request.method == 'POST':
        keywords = request.form.get('news')
        source = request.form.getlist('source')
        session['source'] = source
        session['keywords'] = keywords
        pagination = PaginateLeave(page, searchCondition(keywords, source))
        posts = pagination.items
        return render_template('search.html', newsform=newsform, posts=posts, pagination=pagination, keywords=keywords,
                               web=searchWeb(), officialAccounts=searchOfficialAccounts())

    if request.method == 'GET':
        keywords = session['keywords']
        source = session['source']
        pagination = PaginateLeave(page, searchCondition(keywords, source))
        posts = pagination.items
        return render_template('search.html', newsform=newsform, posts=posts, pagination=pagination, keywords=keywords,
                               web=searchWeb(), officialAccounts=searchOfficialAccounts())
