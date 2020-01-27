# !/user/bin/env/python
# -*- coding:utf-8 -*-
# Author: qixuanye
# Time: 2020/1/21 13:54

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# 设置数据库连接地址
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@127.0.0.1:3306/diag_knowledge"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

class Stu_road(db.Model):
    __tablename__ = "road"
    # 编号
    id = db.Column(db.Integer, primary_key = True)
    stu_id = db.Column(db.String(32), nullable = False)
    ques_id = db.Column(db.String(32), nullable = False)
    strategy = db.Column(db.String(32), nullable = False)
    period1 = db.Column(db.String(32), nullable = False)
    period2 = db.Column(db.String(32), nullable = False)
    period3 = db.Column(db.String(32), nullable = False)
    period4 = db.Column(db.String(32), nullable = False)
    is_del = db.Column(db.SmallInteger, default = 0, nullable = False)
    def __repr__(self):
        return "<Stu_road %r>" % self.name

#if __name__ == "__main__":
    # 创建数据库表
    # db.create_all()
