#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/23 下午3:07
# @Author  : jlinka
# @File    : form.py
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, DateTimeField, SelectField, BooleanField, DateField, \
    validators, FileField, SelectMultipleField
from wtforms.validators import Required, URL, Email


class Search(Form):
    searchName = StringField('任务名字', validators=[Required(message='此项不能为空')])
    submit = SubmitField('搜索')


class NewsForm(Form):
    news = StringField('搜索内容', validators=[Required(message='此项不能为空')])
    hobby = SelectMultipleField('Hobby', choices=[
        ('swim', 'Swimming'),
        ('skate', 'Skating'),
        ('hike', 'Hiking')
    ])
    submit = SubmitField('SEARCH')
