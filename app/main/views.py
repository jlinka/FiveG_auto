#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/23 下午6:01
# @Author  : jlinka
# @File    : views.py

from . import main
from flask import render_template, redirect, request, url_for, session
from app.form import Search, NewsForm
from app.main.search import searchAll, PaginateLeave, searchCondition, searchWeb, searchOfficialAccounts, findObjectId


@main.route('/searchNews', methods=['GET', 'POST'])
def searchNews():
    search = Search()
    newsform = NewsForm()
    session['source'] = ''  # 清理session
    session['keywords'] = ''  # 清理session，不清理很严重啊，如果有更好的方法请告知，想不到方法保存条件了
    session['web'] = ''
    session['auther'] = ''
    page = int(request.args.get('page')) if request.args.get('page') else 1
    pagination = PaginateLeave(page, searchAll())
    posts = pagination.items
    web = searchWeb()
    officialAccounts = searchOfficialAccounts()
    return render_template('search.html', newsform=newsform, posts=posts, pagination=pagination, search=search,
                           web=web, officialAccounts=officialAccounts, session=session)


@main.route('/search', methods=['GET', 'POST'])
def search():
    newsform = NewsForm()
    search = Search()
    page = int(request.args.get('page')) if request.args.get('page') else 1
    if request.method == 'POST':
        keywords = request.form.get('news')
        source = request.form.getlist('source')
        web = request.form.getlist('web')
        auther = request.form.getlist('auther')
        session['source'] = source
        session['keywords'] = keywords
        session['web'] = web
        session['auther'] = auther
        if keywords == "" and len(source) == 0:  # 判断搜索条件为空时，显示全部新闻内容
            if web or auther:
                pagination = PaginateLeave(page, searchCondition(keywords, source, web, auther))
                posts = pagination.items
                return render_template('search.html', newsform=newsform, posts=posts, pagination=pagination,
                                       keywords=keywords,
                                       web=searchWeb(), officialAccounts=searchOfficialAccounts(), session=session)
            else:
                search = Search()
                newsform = NewsForm()
                session['source'] = ''  # 清理session
                session['keywords'] = ''  # 清理session，不清理很严重啊，如果有更好的方法请告知，想不到方法保存条件了
                session['web'] = ''
                session['auther'] = ''
                page = int(request.args.get('page')) if request.args.get('page') else 1
                pagination = PaginateLeave(page, searchAll())
                posts = pagination.items
                return render_template('search.html', newsform=newsform, posts=posts, pagination=pagination,
                                       search=search,
                                       web=searchWeb(), officialAccounts=searchOfficialAccounts(), session=session)
        pagination = PaginateLeave(page, searchCondition(keywords, source, web, auther))
        posts = pagination.items
        return render_template('search.html', newsform=newsform, posts=posts, pagination=pagination, keywords=keywords,
                               web=searchWeb(), officialAccounts=searchOfficialAccounts(), session=session)

    if request.method == 'GET':
        keywords = session['keywords']
        source = session['source']
        web = session['web']
        auther = session['auther']
        if keywords == '' and source == '' and web == '' and auther == '':
            pagination = PaginateLeave(page, searchAll())
            posts = pagination.items
            return render_template('search.html', newsform=newsform, posts=posts, pagination=pagination, search=search,
                                   web=searchWeb(), officialAccounts=searchOfficialAccounts(), session=session)
        else:
            pagination = PaginateLeave(page, searchCondition(keywords, source, web, auther))
            posts = pagination.items
            return render_template('search.html', newsform=newsform, posts=posts, pagination=pagination,
                                   keywords=keywords,
                                   web=searchWeb(), officialAccounts=searchOfficialAccounts(), session=session)


@main.route('/snapshoot', methods=['GET', 'POST'])
def snapshoot():
    if request.method == 'GET':
        ObjectId = request.args.get('ObjectId')
        news = findObjectId(ObjectId)
        createTime = str(news['createTime'])
        news['createTime'] = "".join(str(createTime[0:4]) + "年" + str(createTime[4:6]) + "月" + str(
            createTime[6:8])) + "日"
        return render_template('snapshoot.html', news=news)
