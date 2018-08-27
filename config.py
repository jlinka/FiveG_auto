#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/23 下午3:55
# @Author  : jlinka
# @File    : config.py

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'



class DevelopmentConfig(Config):
    pass

config = {

    'default': DevelopmentConfig
}

