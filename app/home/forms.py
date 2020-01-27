# !/user/bin/env/python
# -*- coding:utf-8 -*-
# Author: qixuanye
# Time: 2019/12/09

from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from app.models import Function_list

'''
查询表单
'''
class query_form(FlaskForm):
    function_type = SelectField(
        label = "功能点分类",
        description = "功能点分类",
        validators = [
            DataRequired("分类不能为空！")
        ],
        choices = [(v.func_id, v.func_name) for v in Function_list.query.filter_by(is_del = 0)],
        default = 1,
        coerce = int,
        render_kw = {
            "class": "form-control boxClear",
            # "style": "width:600px"
        }
    )
    content = TextAreaField(
        label = "查询内容",
        description = "查询内容",
        validators = [
            DataRequired("查询内容不能为空！")
        ],
        render_kw = {
            "class": "form-control boxClear",
            # "style": "height: 150px",
            # "style": "width: 800px",
            "id": "content"
        }
    )
    submit = SubmitField(
        "问题查询",
        render_kw = {
            "class": "btn btn-primary"
        }
    )