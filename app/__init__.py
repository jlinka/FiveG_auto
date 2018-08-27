#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/23 下午4:04
# @Author  : jlinka
# @File    : __init__.py
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_moment import Moment
import config

bootstrap = Bootstrap()

# mail = Mail()
moment = Moment()


def create_app():
    app = Flask(__name__, static_url_path='/static')
    bootstrap.init_app(app)
    app.config.update(dict(
        SECRET_KEY="powerful secretkey",
        WTF_CSRF_SECRET_KEY="a csrf secret key"))
    return app
