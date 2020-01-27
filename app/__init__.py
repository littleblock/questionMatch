# !/user/bin/env/python
# -*- coding:utf-8 -*-
# Author: qixuanye
# Time: 2019/11/14 14:25

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# 设置数据库连接地址
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@127.0.0.1:3306/diag_knowledge"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)
app.debug = True

from app.home import home as home_bluePrint
from app.admin import admin as admin_bluePrint
from app.test import test as test_bluePrint

app.register_blueprint(home_bluePrint, url_prefix = "/home")
app.register_blueprint(admin_bluePrint, url_prefix = "/admin")
app.register_blueprint(test_bluePrint, url_prefix = "/test")