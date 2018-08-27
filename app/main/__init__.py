#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/23 下午6:01
# @Author  : jlinka
# @File    : __init__.py

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors