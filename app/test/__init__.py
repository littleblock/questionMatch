# !/user/bin/env/python
# -*- coding:utf-8 -*-
# Author: qixuanye
# Time: 2020/1/21 14:25

from flask import Blueprint

test = Blueprint("test", __name__)

import app.test.views