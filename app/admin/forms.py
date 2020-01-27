# !/user/bin/env/python
# -*- coding:utf-8 -*-
# Author: qixuanye
# Time: 2019/11/14 14:25

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, FileField, IntegerField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import Admin, Function_list
from flask_sqlalchemy import SQLAlchemy

'''
登录表单
1. 账号
2. 密码
3. 登录按钮
'''
class login_form(FlaskForm):
    name = StringField(
        label = "账号",
        # 验证规则列表
        validators = [
            DataRequired("账号不能为空！")
        ],
        description = "账号",
        # 自定义html属性
        render_kw = {
            "class": "form-control textClear",
            "placeholder": "请输入账号!"
        }
    )
    pwd = PasswordField(
        label = "密码",
        validators = [
            DataRequired("密码不能为空")
        ],
        description = "密码",
        render_kw = {
            "class": "form-control textClear",
            "placeholder": "请输入密码!"
        }
    )
    submit = SubmitField(
        "登录",
        render_kw = {
            "class": "btn btn-primary"
        }
    )

    # 自定义字段验证规则：validate_字段名
    def validate_name(self, field):
        name = field.data
        user1 = Admin.query.filter_by(account_name = name).count()
        if user1 <= 0:
            raise ValidationError("账号不存在！")
        else:
            user2 = Admin.query.filter_by(account_name = name).first()
            pwd = self.pwd.data
            if not user2.check_pwd(pwd):
                raise ValidationError("密码不正确")


'''
    def validate_pwd(self, field):
        name = self.name
        pwd = field.data
        user = Admin.query.filter_by(account_name = self.name.data).first()
        if not user.check_pwd(pwd):
            raise ValidationError("密码不正确")
'''

'''
新增功能点
1. 功能点代码
2. 功能点名称
3. 账号信息
4. 提交按钮
'''
class function_add_form(FlaskForm):
    code = StringField(
        label = "功能点代码",
        description = "功能点代码",
        validators = [
            DataRequired("功能点代码不能为空")
        ],
        render_kw = {
            "class": "form-control",
            "placeholder": "功能点代码请符合相应规范！"
        }
    )
    name = StringField(
        label = "功能点名称",
        description = "功能点名称",
        validators = [
            DataRequired("功能点名称不能为空")
        ],
        render_kw = {
            "class": "form-control",
            "placeholder": "请输入功能点名称！"
        }
    )
    submit = SubmitField(
        "添加功能点",
        render_kw = {
            "class": "btn btn-primary"
        }
    )


'''
问题发布
1. 标题
2. 功能点分类
3. 文本关键字
4. 业务关键字
5. 回答内容
6. 账号信息
7. 发布问题按钮
'''
class question_add_form(FlaskForm):
    title = StringField(
        label = "标题",
        description = "标题",
        validators = [
            DataRequired("标题不能为空！")
        ],
        render_kw = {
            "class": "form-control",
            "placeholder": "请输入问题描述！"
        }
    )
    function_type = SelectField(
        label = "功能点分类",
        description = "功能点分类",
        validators = [
            DataRequired("分类不能为空！")
        ],
        choices = [(v.func_id, v.func_name) for v in Function_list.query.filter_by(is_del = 0)],
        default = 3,
        coerce = int,
        render_kw = {
            "class": "form-control"
        }

    )
    '''
    test_keyword = SelectField(
        label = "文本关键字",
        description = "文本关键字",
        validators = [
            DataRequired("文本关键字不能为空！")
        ],
        choices = [(1, "存在性关键字"), (2, "否定性关键字"), (3, "应该类关键字")],
        default = 2,
        coerce = int,
        render_kw = {
            "class": "form-control"
        }
    )
    '''
    bus_keyword = StringField(
        label = "业务关键字",
        description = "业务关键字",
        validators = [
            DataRequired("业务关键字不能为空！")
        ],
        render_kw = {
            "class": "form-control",
            "placeholder": "业务关键字请用';'分隔"
        }
    )
    content = TextAreaField(
        label = "回答内容",
        description = "回答内容",
        validators = [
            DataRequired("回答内容不能为空！")
        ],
        render_kw = {
            "style": "height: 300px",
            "id": "content"
        }
    )
    '''
    imagine = FileField(
        label = u"封面",
        validators = [
            DataRequired(u"封面不能为空！")
        ],
        description = u"封面",
        render_kw = {
            "class": "form-control-file"
        }
    )
    '''
    submit = SubmitField(
        "发布问题",
        render_kw = {
            "class": "btn btn-primary"
        }
    )


'''
问题编辑
1. 该问题编号
2. 标题
3. 功能点分类
4. 文本关键字
5. 业务关键字
6. 回答内容
7. 账号信息
8. 发布问题按钮
'''
class question_edit_form(FlaskForm):
    id = IntegerField(
        label = "问题编号",
        validators = [
            DataRequired("问题编号不能为空！")
        ]
    )
    title = StringField(
        label = "标题",
        description = "标题",
        validators = [
            DataRequired("标题不能为空！")
        ],
        render_kw = {
            "class": "form-control",
            "placeholder": "请输入问题描述！"
        }
    )
    function_type = SelectField(
        label = "功能点分类",
        description = "功能点分类",
        validators = [
            DataRequired("分类不能为空！")
        ],
        choices = [(v.func_id, v.func_name) for v in Function_list.query.filter_by(is_del = 0)],
        default = 3,
        coerce = int,
        render_kw = {
            "class": "form-control"
        }

    )
    '''
    test_keyword = SelectField(
        label = "文本关键字",
        description = "文本关键字",
        validators = [
            DataRequired("文本关键字不能为空！")
        ],
        choices = [(1, "存在性关键字"), (2, "否定性关键字"), (3, "应该类关键字")],
        default = 2,
        coerce = int,
        render_kw = {
            "class": "form-control"
        }
    )
    '''
    bus_keyword = StringField(
        label = "业务关键字",
        description = "业务关键字",
        validators = [
            DataRequired("业务关键字不能为空！")
        ],
        render_kw = {
            "class": "form-control",
            "placeholder": "业务关键字请用';'分隔"
        }
    )
    content = TextAreaField(
        label = "回答内容",
        description = "回答内容",
        validators = [
            DataRequired("回答内容不能为空！")
        ],
        render_kw = {
            "style": "height: 300px",
            "id": "content"
        }
    )
    '''
    imagine = FileField(
        label = u"封面",
        validators = [
            DataRequired(u"封面不能为空！")
        ],
        description = u"封面",
        render_kw = {
            "class": "form-control-file"
        }
    )
    '''
    submit = SubmitField(
        "编辑问题",
        render_kw = {
            "class": "btn btn-primary"
        }
    )