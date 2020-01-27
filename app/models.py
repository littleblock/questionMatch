# !/user/bin/env/python
# -*- coding:utf-8 -*-
# Author: qixuanye
# Time: 2019/11/14 14:25

from flask import Flask
from app import db
from datetime import datetime

'''
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@127.0.0.1:3306/diag_knowledge"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
app.debug = True
'''


# GS问题库数据模型
class Question_base(db.Model):
    # 表名
    __tablename__ = "question_base"
    # 问题编号
    ques_id = db.Column(db.Integer, primary_key = True)
    # 问题名
    ques_title = db.Column(db.String(1000), nullable = False)
    # 该问题的相关图片，可以为空
    ques_image = db.Column(db.String(255))
    # 创建人
    creator = db.Column(db.String(128), nullable = False)
    # 创建时间
    create_time = db.Column(db.DateTime, default = datetime.now)
    # 最后修改人
    last_modify_user = db.Column(db.String(128), nullable = False)
    # 最后修改时间
    last_modify_time = db.Column(db.DateTime, default = datetime.now)
    # 该条记录是否可用，默认为0，可用
    is_del = db.Column(db.SmallInteger, default = 0, nullable = False)
    # 答案库表外键连接
    answer_bases = db.relationship('Answer_base', backref = 'question_base')
    # 功能点-问题库对应表外键连接
    func_ques_relations = db.relationship('Func_ques_relation', backref = 'question_base')
    # 问题库日志外键连接
    question_logs = db.relationship('Question_log', backref = 'question_base')
    # 业务关键字外键连接
    keyword_buses = db.relationship('Keyword_bus', backref = 'question_base')

    def __repr__(self):
        return "<Question_base %r>" % self.name


# GS答案库表
class Answer_base(db.Model):
    # 表名
    __tablename__ = "answer_base"
    # 答案id
    answer_id = db.Column(db.Integer, primary_key = True)
    # 答案内容
    answer_text = db.Column(db.String(4000), nullable = False)
    # 答案相关图片，可以为空
    answer_image = db.Column(db.String(255))
    # 对应的问题id
    ques_id = db.Column(db.Integer, db.ForeignKey('question_base.ques_id'))
    # 创建人
    creator = db.Column(db.String(128), nullable = False)
    # 创建时间
    create_time = db.Column(db.DateTime, default = datetime.now)
    # 发布人
    publish_user = db.Column(db.String(128), nullable = False)
    # 发布时间
    publish_time = db.Column(db.DateTime, default = datetime.now)
    # 最后修改人
    last_modify_user = db.Column(db.String(128), nullable = False)
    # 最后修改时间
    last_modify_time = db.Column(db.DateTime, default = datetime.now)
    # 该条记录是否可用，默认为0，可用
    is_del = db.Column(db.SmallInteger, default = 0, nullable = False)
    # 答案库访问日志表外键连接
    answer_logs = db.relationship('Answer_log', backref = 'answer_base')

    def __repr__(self):
        return "<Answer_base %r>" % self.name


# 功能点列表
class Function_list(db.Model):
    __tablename__ = "function_list"
    # id
    func_id = db.Column(db.Integer, primary_key = True)
    # 功能点代码
    func_code = db.Column(db.String(128), nullable = False)
    # 功能点名称
    func_name = db.Column(db.String(256), nullable = False)
    # 资源id
    res_id = db.Column(db.Integer, db.ForeignKey('resource_list.res_id'), nullable = False)
    # 资源类别名称
    res_type_name = db.Column(db.String(256))
    # 创建人
    creator = db.Column(db.String(128), nullable = False)
    # 创建时间
    create_time = db.Column(db.DateTime, default = datetime.now)
    # 最后修改人
    last_modify_user = db.Column(db.String(128), nullable = False)
    # 最后修改时间
    last_modify_time = db.Column(db.DateTime, default = datetime.now)
    # 该条记录是否可用，默认为0，可用
    is_del = db.Column(db.SmallInteger, default = 0, nullable = False)
    # 功能点-问题库对应表外键连接
    func_ques_relations = db.relationship('Func_ques_relation', backref = 'function_list')
    # 功能点访问日志外键连接
    function_logs = db.relationship('Function_log', backref = 'function_list')

    def __repr__(self):
        return "<Function_list %r>" % self.name


# 功能点列表-问题库对应表
class Func_ques_relation(db.Model):
    __tablename__ = "func_ques_relation"
    # id
    id = db.Column(db.BigInteger, primary_key = True)
    # 功能点列表id
    func_id = db.Column(db.Integer, db.ForeignKey('function_list.func_id'), nullable = False)
    # 功能点名称
    func_name = db.Column(db.String(256))
    # 问题表id
    ques_id = db.Column(db.Integer, db.ForeignKey('question_base.ques_id'), nullable = False)
    # 问题标题
    ques_title = db.Column(db.String(1000))
    # 创建者
    creator = db.Column(db.String(128), nullable = False)
    # 创建时间
    create_time = db.Column(db.DateTime, default = datetime.now)
    # 最后修改人
    last_modify_user = db.Column(db.String(128), nullable = False)
    # 最后修改时间
    last_modify_time = db.Column(db.DateTime, default = datetime.now)
    # 该条记录是否可用，默认为0，可用
    is_del = db.Column(db.SmallInteger, default = 0, nullable = False)

    def __repr__(self):
        return "<Func_ques_relation %r>" % self.name


# 功能点访问日志
class Function_log(db.Model):
    __tablename__ = "function_log"
    # id
    id = db.Column(db.BigInteger, primary_key = True)
    # 功能点列表id
    func_id = db.Column(db.Integer, db.ForeignKey('function_list.func_id'), nullable = False)
    # 创建人
    creator = db.Column(db.String(128), nullable = False)
    # 创建时间
    create_time = db.Column(db.DateTime, default = datetime.now)
    # 该条记录是否可用，默认为0，可用
    is_del = db.Column(db.SmallInteger, default = 0, nullable = False)

    def __repr__(self):
        return "<Function_log %r>" % self.name


# 问题库访问日志
class Question_log(db.Model):
    __tablename__ = "question_log"
    # id
    id = db.Column(db.BigInteger, primary_key = True)
    # 问题库id
    ques_id = db.Column(db.Integer, db.ForeignKey('question_base.ques_id'), nullable = False)
    # 创建人
    creator = db.Column(db.String(128), nullable = False)
    # 创建时间
    create_time = db.Column(db.DateTime, default = datetime.now)
    # 该条记录是否可用，默认为0，可用
    is_del = db.Column(db.SmallInteger, default = 0, nullable = False)

    def __repr__(self):
        return "<Question_log %r>" % self.name


# 答案库访问日志
class Answer_log(db.Model):
    __tablename__ = "answer_log"
    # id
    id = db.Column(db.BigInteger, primary_key = True)
    # 答案库对应id
    ques_id = db.Column(db.Integer, db.ForeignKey('answer_base.ques_id'), nullable = False)
    # 是否有用, 0为无用,1为有用，2为未评价
    is_useful = db.Column(db.SmallInteger)
    # 对应搜索框内容
    search_text = db.Column(db.String(256))
    # 创建人
    creator = db.Column(db.String(128))
    # 创建时间
    create_time = db.Column(db.DateTime, default = datetime.now)
    # 该条记录是否可用，默认为0，可用
    is_del = db.Column(db.SmallInteger, default = 0, nullable = False)

    def __repr__(self):
        return "<Answer_log %r>" % self.name


# 资源列表
class Resource_list(db.Model):
    __tablename__ = "resource_list"
    # id
    res_id = db.Column(db.Integer, primary_key = True)
    # 资源类别名称
    res_type_name = db.Column(db.String(256), nullable = False)
    # 创建人
    creator = db.Column(db.String(128), nullable = False)
    # 创建时间
    create_time = db.Column(db.DateTime, default = datetime.now)
    # 最后修改人
    last_modify_user = db.Column(db.String(128), nullable = False)
    # 最后修改时间
    last_modify_time = db.Column(db.DateTime, default = datetime.now)
    # 该条记录是否可用，默认为0，可用
    is_del = db.Column(db.SmallInteger, default = 0, nullable = False)
    # 功能点列表外键连接
    function_lists = db.relationship('Function_list', backref = 'resource_list')

    def __repr__(self):
        return "<Resource_list %r>" % self.name


# 管理员表
class Admin(db.Model):
    __tablename__ = "admin"
    # id
    admin_id = db.Column(db.Integer, primary_key = True)
    # 真实姓名
    real_name = db.Column(db.String(128), nullable = False)
    # 账号名
    account_name = db.Column(db.String(128), nullable = False, unique = True)
    # 密码
    password = db.Column(db.String(128), nullable = False)
    # 邮箱
    email = db.Column(db.String(128))
    # 电话
    phone = db.Column(db.String(128))
    # 创建人
    creator = db.Column(db.String(128), nullable = False)
    # 创建时间
    create_time = db.Column(db.DateTime, default = datetime.now)
    # 最后修改人
    last_modify_user = db.Column(db.String(128), nullable = False)
    # 最后修改时间
    last_modify_time = db.Column(db.DateTime, default = datetime.now)
    # 该条记录是否可用，默认为0，可用
    is_del = db.Column(db.SmallInteger, default = 0, nullable = False)
    # 管理员登录日志外键连接
    admin_logs = db.relationship('Admin_log', backref = 'admin')
    # 操作日志外键连接
    operation_logs = db.relationship('Operation_log', backref = 'admin')
    # 管理员角色对应外键连接
    admin_role_relations = db.relationship('Admin_role_relation', backref = 'admin')

    def __repr__(self):
        return "<Admin %r>" % self.name

    def check_pwd(self, pwd):
        return self.password == pwd


# 管理员登录日志
class Admin_log(db.Model):
    __tablename__ = "admin_log"
    # id
    id = db.Column(db.BigInteger, primary_key = True)
    # 管理员id
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.admin_id'), nullable = False)
    # 管理员账号名
    admin_name = db.Column(db.String(128), nullable = False)
    # 登录ip
    ip = db.Column(db.String(128))
    # 创建时间
    create_time = db.Column(db.DateTime, default = datetime.now)

    def __repr__(self):
        return "<Admin_log %r>" % self.name


# 操作日志
class Operation_log(db.Model):
    __tablename__ = "operation_log"
    # id
    id = db.Column(db.BigInteger, primary_key = True)
    # 管理员id
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.admin_id'), nullable = False)
    # 管理员账号名
    admin_name = db.Column(db.String(128), nullable = False)
    # 操作ip
    ip = db.Column(db.String(128))
    # 操作行为
    action = db.Column(db.SmallInteger, nullable = False)
    # 操作对象
    operation_type = db.Column(db.SmallInteger, nullable = False,
                               comment = '1-问题，2-答案，3-功能点，4-业务关键字，5-文本关键字，6-权限，7-角色，8-管理员，9-资源')
    # 操作描述
    operation_desc = db.Column(db.String(1024), nullable = False, comment = '若为修改、删除，则记录操作对象的id，若为新增，则记录新增的内容')
    # 操作时间
    create_time = db.Column(db.DateTime, default = datetime.now)

    def __repr__(self):
        return "<Operation_log %r>" % self.name


# 权限表
class Auth(db.Model):
    __tablename__ = "auth"
    # id
    auth_id = db.Column(db.Integer, primary_key = True)
    # 权限名
    auth_name = db.Column(db.String(128), nullable = False)
    # 权限描述
    auth_desc = db.Column(db.String(1024))
    # url
    url = db.Column(db.String(256), nullable = False)
    # 创建人
    creator = db.Column(db.String(128), nullable = False)
    # 创建时间
    create_time = db.Column(db.DateTime, default = datetime.now)
    # 最后修改人
    last_modify_user = db.Column(db.String(128), nullable = False)
    # 最后修改时间
    last_modify_time = db.Column(db.DateTime, default = datetime.now)
    # 该条记录是否可用，默认为0，可用
    is_del = db.Column(db.SmallInteger, default = 0, nullable = False)
    # 权限角色对应表外键连接
    auth_role_relations = db.relationship('Auth_role_relation', backref = 'auth')

    def __repr__(self):
        return "<Auth %r>" % self.name


# 角色表
class Role(db.Model):
    __tablename__ = "role"
    # id
    role_id = db.Column(db.Integer, primary_key = True)
    # 角色名
    role_name = db.Column(db.String(128), nullable = False)
    # 角色描述
    role_desc = db.Column(db.String(1024))
    # 创建人
    creator = db.Column(db.String(128), nullable = False)
    # 创建时间
    create_time = db.Column(db.DateTime, default = datetime.now)
    # 最后修改人
    last_modify_user = db.Column(db.String(128), nullable = False)
    # 最后修改时间
    last_modify_time = db.Column(db.DateTime, default = datetime.now)
    # 该条记录是否可用，默认为0，可用
    is_del = db.Column(db.SmallInteger, default = 0, nullable = False)
    # 权限角色对应表外键连接
    auth_role_relations = db.relationship('Auth_role_relation', backref = 'role')
    # 管理员角色对应表外键连接
    admin_role_relations = db.relationship('Admin_role_relation', backref = 'role')

    def __repr__(self):
        return "<Role %r>" % self.name


# 权限角色对应表
class Auth_role_relation(db.Model):
    __tablename__ = "auth_role_relation"
    # id
    id = db.Column(db.Integer, primary_key = True)
    # 权限id
    auth_id = db.Column(db.Integer, db.ForeignKey('auth.auth_id'))
    # 权限名
    auth_name = db.Column(db.String(128), nullable = False)
    # 角色id
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'))
    # 角色名
    role_name = db.Column(db.String(128), nullable = False)
    # 创建人
    creator = db.Column(db.String(128), nullable = False)
    # 创建时间
    create_time = db.Column(db.DateTime, default = datetime.now)
    # 最后修改人
    last_modify_user = db.Column(db.String(128), nullable = False)
    # 最后修改时间
    last_modify_time = db.Column(db.DateTime, default = datetime.now)
    # 该条记录是否可用，默认为0，可用
    is_del = db.Column(db.SmallInteger, default = 0, nullable = False)

    def __repr__(self):
        return "<Auth_role_relation %r>" % self.name


# 管理员角色对应表
class Admin_role_relation(db.Model):
    __tablename__ = "admin_role_relation"
    # id
    id = db.Column(db.Integer, primary_key = True)
    # 管理员id
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.admin_id'))
    # 管理员账号名
    admin_name = db.Column(db.String(128), nullable = False)
    # 角色id
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'))
    # 角色名
    role_name = db.Column(db.String(128), nullable = False)
    # 创建人
    creator = db.Column(db.String(128), nullable = False)
    # 创建时间
    create_time = db.Column(db.DateTime, default = datetime.now)
    # 最后修改人
    last_modify_user = db.Column(db.String(128), nullable = False)
    # 最后修改时间
    last_modify_time = db.Column(db.DateTime, default = datetime.now)
    # 该条记录是否可用，默认为0，可用
    is_del = db.Column(db.SmallInteger, default = 0, nullable = False)

    def __repr__(self):
        return "<Admin_role_relation %r>" % self.name


class Keyword_bus(db.Model):
    __tablename__ = "keyword_bus"
    # id
    id = db.Column(db.Integer, primary_key = True)
    # 业务关键字名称
    keyword_bus_name = db.Column(db.String(256), nullable = False)
    # 问题id
    ques_id = db.Column(db.Integer, db.ForeignKey('question_base.ques_id'), nullable = False)
    # 创建人
    creator = db.Column(db.String(128), nullable = False)
    # 创建时间
    create_time = db.Column(db.DateTime, default = datetime.now)
    # 最后修改人
    last_modify_user = db.Column(db.String(128), nullable = False)
    # 最后修改时间
    last_modify_time = db.Column(db.DateTime, default = datetime.now)
    # 该条记录是否可用，默认为0，可用
    is_del = db.Column(db.SmallInteger, default = 0, nullable = False)

    def __repr__(self):
        return "<Keyword_bus %r>" % self.name


class Search_log(db.Model):
    __tablename__ = "search_log"
    # id
    id = db.Column(db.Integer, primary_key = True)
    # 所选功能点分类
    func_id = db.Column(db.Integer, nullable = False)
    # 查询内容
    search_text = db.Column(db.String(1000), nullable = False)
    # 返回问题排序
    ques_sort = db.Column(db.String(2000))
    # 查询时间
    create_time = db.Column(db.DateTime, default = datetime.now())
    # 查询ip
    ip = db.Column(db.String(128))


# 查询结果临时存储表
class Temp(db.Model):
    __tablename__ = "temp"
    id = db.Column(db.Integer, primary_key = True)
    ques_id = db.Column(db.Integer, nullable = False)
    ques_title = db.Column(db.String(1000))
    func_type = db.Column(db.Integer, nullable = False)
    func_name = db.Column(db.String(1000))
    # 创建时间
    create_time = db.Column(db.DateTime, default = datetime.now)

    def __repr__(self):
        return "<Temp %r>" % self.name

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

    # def __repr__(self):
        # return "<Stu_road %r>" % self.name

# if __name__ == "__main__":
    # 创建数据库表
    # db.create_all()

    # 插入一条记录
    '''
    user = User(
        name = 'qixuanye'
    )
    db.session.add(user)
    db.session.commit()
    '''
    # 删除数据库表
    # db.drop_all()
