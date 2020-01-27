# !/user/bin/env/python
# -*- coding:utf-8 -*-
# Author: qixuanye
# Time: 2019/11/14 14:25

from flask import Blueprint

home = Blueprint("home", __name__)


import app.home.views