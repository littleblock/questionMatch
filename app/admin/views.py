# !/user/bin/env/python
# -*- coding:utf-8 -*-
# Author: qixuanye
# Time: 2019/11/14 14:25


from . import admin
from flask import Flask, render_template, redirect, url_for, flash, session, Response, request
from .forms import login_form, question_add_form, function_add_form, question_edit_form
from app.models import Admin, Admin_log, db, Question_base, Answer_base, Keyword_bus, Function_list, Func_ques_relation, \
    Search_log, Answer_log
from functools import wraps
from werkzeug.utils import secure_filename
from datetime import datetime
from sqlalchemy import func
import json
import os
import uuid
import re


@admin.route("/")
def index():
    return "<h1 style = 'color: red '>this is admin</h1>"


# 登录装饰器
def user_login_req(f):
    @wraps(f)
    def login_req(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("admin.login", next = request.url))
        return f(*args, **kwargs)

    return login_req


# 登录
@admin.route("/login", methods = ['GET', 'POST'])
def login():
    form = login_form()
    if form.validate_on_submit():
        data = form.data
        session["user"] = data["name"]
        # 登录成功，跳转到问题列表
        flash("登录成功！", "ok")
        return redirect("question_base/list/1")
        # return redirect(url_for("admin.question_list") + "/1")
    '''
    该跳转会无限次循环，但不知道原因
    else:
        flash("登录失败，请重新登录", "err")
        return redirect(url_for("admin.login"))
    '''
    return render_template("admin/login.html", title = "鲁班智能答疑后台", form = form)


# 注册
@admin.route("/register", methods = ['GET', 'POST'])
def register():
    return render_template("admin/register.html")


# 退出，直接跳转到登录页面
@admin.route("/logout", methods = ['GET'])
@user_login_req
def logout():
    session.pop("user", None)
    return redirect(url_for("admin.login"))


# 添加功能点
@admin.route("/function/add", methods = ['GET', 'POST'])
@user_login_req
def function_add():
    form = function_add_form()
    if form.validate_on_submit():
        data = form.data
        # 获取用户名
        user = session["user"]
        # 保存function_list数据
        function = Function_list(
            func_code = data["code"],
            func_name = data["name"],
            # 暂时写死资源名称
            res_id = 1,
            res_type_name = "GS电子采购平台",
            creator = user,
            create_time = datetime.now(),
            last_modify_user = user,
            last_modify_time = datetime.now(),
            is_del = 0
        )
        db.session.add(function)
        db.session.commit()
        flash("发布成功！", "ok")
    return render_template("/admin/function_add.html", title = "新增功能点", form = form)


# 功能点列表
@admin.route("/function/list/<int:page>", methods = ['GET'])
@user_login_req
def function_list(page = None):
    if page is None:
        page = 1
    page_datas = Function_list.query.filter_by(is_del = 0).paginate(page = page, per_page = 7)
    return render_template("/admin/function_list.html", title = "功能点列表", page_data = page_datas)


# 删除功能点
@admin.route("/function/del/<id>", methods = ['GET', 'POST'])
@user_login_req
def function_del(id):
    # 删除function_list记录
    function = Function_list.query.get_or_404(int(id))
    function.is_del = 1
    db.session.add(function)
    # 删除func_ques_relation记录
    function_ques_relations = Func_ques_relation.query.filter_by(func_id = int(id)).all()
    for v in function_ques_relations:
        v.is_del = 1
        db.session.add(v)
        # 删除question_base记录
        question = Question_base.query.filter_by(ques_id = v.ques_id).first()
        question.is_del = 1
        db.session.add(question)
        # 删除answer_base记录
        answers = Answer_base.query.filter_by(ques_id = v.ques_id).all()
        for x in answers:
            x.is_del = 1
            db.session.add(x)
        # 删除keyword_bus
        bus_keywords = Keyword_bus.query.filter_by(ques_id = v.ques_id).all()
        for y in bus_keywords:
            y.is_del = 1
            db.session.add(y)
    db.session.commit()
    flash("删除“%s”成功！" % function.func_name, "ok")
    return redirect("/admin/function/list/1")


# 修改文件名称
def change_name(name):
    info = os.path.splitext(name)
    # 文件名： 时间格式字符串+唯一字符串+后缀名
    name = datetime.now().strftime('%Y%m%d%H%M%S') + "_" + str(uuid.uuid4().hex) + info[-1]
    return name


# 添加问题
@admin.route("/question_base/add", methods = ['GET', 'POST'])
@user_login_req
def question_add():
    form = question_add_form()
    form.function_type.choices = [(v.func_id, v.func_name) for v in Function_list.query.filter_by(is_del = 0)]
    if form.validate_on_submit():
        data = form.data

        # 上传文件
        # file = secure_filename(form.imagine.data.filename)
        # imagine = change_name(file)
        # 保存文件
        # form.imagine.data.save(os.path.dirname(os.path.dirname(__file__)) + "/static/uploads/" + imagine)
        # 获取用户名
        user = session["user"]
        # 保存question_base数据
        question = Question_base(
            ques_title = data["title"],
            creator = user,
            create_time = datetime.now(),
            last_modify_user = user,
            last_modify_time = datetime.now(),
            is_del = 0
        )
        db.session.add(question)
        # 返回新增的id
        db.session.flush()
        question_id = question.ques_id
        # 保存answer_base数据
        answer = Answer_base(
            answer_text = data["content"],
            ques_id = question_id,
            creator = user,
            create_time = datetime.now(),
            # 发布人先写死，后面记得修改
            publish_user = 'qixuanye',
            publish_time = datetime.now(),
            last_modify_user = user,
            last_modify_time = datetime.now(),
            is_del = 0
        )
        db.session.add(answer)
        # 保存功能点分类
        func_id = data["function_type"]
        func_name = Function_list.query.filter_by(func_id = func_id).first()
        func_ques_relation = Func_ques_relation(
            func_id = data["function_type"],
            func_name = func_name.func_name,
            ques_id = question_id,
            ques_title = data["title"],
            creator = user,
            create_time = datetime.now(),
            last_modify_user = user,
            last_modify_time = datetime.now(),
            is_del = 0
        )
        db.session.add(func_ques_relation)
        # 保存业务关键字
        bus_keyword = re.split(r'[;；]', data["bus_keyword"])
        for v in bus_keyword:
            bus_keyword_object = Keyword_bus(
                keyword_bus_name = v,
                ques_id = question_id,
                creator = user,
                create_time = datetime.now(),
                last_modify_user = user,
                last_modify_time = datetime.now(),
                is_del = 0
            )
            db.session.add(bus_keyword_object)
        db.session.commit()
        flash("发布成功！", "ok")
    return render_template("admin/question_add.html", title = "问题发布", form = form)


# 编辑问题
@admin.route("/question_base/edit/<id>", methods = ["GET", "POST"])
@user_login_req
def question_edit(id):
    form = question_edit_form()
    # 根据id获取question_base的信息
    question = Question_base.query.get_or_404(int(id))
    # 根据id获取func_ques_relation的信息
    function_type = Func_ques_relation.query.filter_by(ques_id = int(id), is_del = 0).first()
    # 根据id获取answer_base的信息
    answer = Answer_base.query.filter_by(ques_id = int(id), is_del = 0).first()
    # 根据id获取业务关键字
    bus_keys = Keyword_bus.query.filter_by(ques_id = int(id), is_del = 0)
    # 对业务关键字进行拼接
    bus_key_text = ""
    for v in bus_keys:
        bus_key_text = bus_key_text + v.keyword_bus_name + ';'
    bus_key_text = bus_key_text[:-1]
    # 读取待编辑内容
    if request.method == "GET":
        form.function_type.data = function_type.func_id
        form.bus_keyword.data = bus_key_text
        form.content.data = answer.answer_text
    if form.validate_on_submit():
        data = form.data
        user = session["user"]
        # 编辑question_base
        question.ques_title = data["title"]
        question.last_modify_user = user
        question.last_modify_time = datetime.now()
        db.session.add(question)
        # 编辑功能点分类
        function_type.func_id = data["function_type"]
        function_type.func_name = Function_list.query.filter_by(func_id = data["function_type"],
                                                                is_del = 0).first().func_name
        function_type.last_modify_user = user
        function_type.last_modify_time = datetime.now()
        db.session.add(function_type)
        # 删除旧的业务关键字
        for v in bus_keys:
            v.is_del = 1
            v.last_modify_user = user
            v.last_modify_time = datetime.now()
            db.session.add(v)
        # 保存业务关键字
        new_bus_keyword = re.split(r'[;；]', data["bus_keyword"])
        for v in new_bus_keyword:
            bus_keyword_object = Keyword_bus(
                keyword_bus_name = v,
                ques_id = int(id),
                last_modify_user = user,
                last_modify_time = datetime.now(),
                is_del = 0
            )
            db.session.add(bus_keyword_object)
        # 编辑答案内容
        answer.answer_text = data["content"]
        answer.last_modify_user = user
        answer.last_modify_time = datetime.now()
        db.session.add(answer)
        db.session.commit()
        flash("编辑问题成功", "ok")
    return render_template("admin/question_edit.html", title = "编辑问题", form = form, question_data = question)


# 删除问题
@admin.route("/question_base/del/<id>", methods = ["GET", "POST"])
@user_login_req
def question_del(id):
    question = Question_base.query.get_or_404(int(id))
    # 删除question_base
    question.is_del = 1
    db.session.add(question)
    # 删除answer_base
    answers = Answer_base.query.filter_by(ques_id = question.ques_id).all()
    for v in answers:
        v.is_del = 1
        db.session.add(v)
    # 删除keyword_bus
    bus_keywords = Keyword_bus.query.filter_by(ques_id = question.ques_id).all()
    for x in bus_keywords:
        x.is_del = 1
        db.session.add(x)
    # 删除func_ques_relation
    func_ques_relation = Func_ques_relation.query.filter_by(ques_id = question.ques_id).first()
    func_ques_relation.is_del = 1
    db.session.add(func_ques_relation)
    db.session.commit()
    return redirect("/admin/question_base/list/1")


# 问题列表
@admin.route("/question_base/list/<int:page>", methods = ['GET'])
@user_login_req
def question_list(page = None):
    if page is None:
        page = 1
    page_data = Question_base.query.join(
        Answer_base
    ).join(
        Func_ques_relation
        # join(Keyword_bus).
    ).filter(
        Answer_base.ques_id == Question_base.ques_id,
        Func_ques_relation.ques_id == Question_base.ques_id,
        # Keyword_bus.ques_id == Question_base.ques_id,
        Question_base.is_del == 0,
        Answer_base.is_del == 0,
        Func_ques_relation.is_del == 0,
        # Keyword_bus.is_del == 0
    ).order_by(
        Question_base.last_modify_time.desc()
    ).paginate(page = page, per_page = 10)

    return render_template("admin/question_list.html", title = "问题列表", page_data = page_data)


# 功能点访问统计
@admin.route("/charts/func_chart", methods = ["GET"])
@user_login_req
def func_chart():
    search_datas = Search_log.query.group_by(Search_log.func_id)
    chart_names = []
    chart_values = []
    for v in search_datas:
        count = len(Search_log.query.filter_by(func_id = v.func_id).all())
        name = Function_list.query.filter_by(func_id = v.func_id, is_del = 0).first()
        if not name:
            continue
        chart_names.append(name.func_name)
        chart_values.append(count)

    return render_template("admin/func_chart.html",
                           chart_datas = json.dumps({'name': chart_names, 'value': chart_values}, ensure_ascii = False))

# 问题访问统计
@admin.route("/charts/answer_chart", methods = ["GET"])
@user_login_req
def answer_chart():
    search_datas = Answer_log.query.group_by(Answer_log.ques_id)
    search_dict = {}
    # 统计每个问题的搜索次数
    for v in search_datas:
        count = len(Answer_log.query.filter_by(ques_id = v.ques_id).all())
        search_dict[v.ques_id] = count
    # 对查询结果排序成倒序
    search_sort = sorted(search_dict.items(), key = lambda search_sort: search_sort[1], reverse = True)
    # 获取访问次数最多的五个问题
    max_list = search_sort[:5]
    # 获取相应的问题名称和问题访问数量
    chart_names = []
    chart_values = []
    for v in max_list:
        ques_title = Question_base.query.filter_by(ques_id = v[0], is_del = 0).first().ques_title
        chart_names.append(ques_title)
        chart_values.append(v[1])

    return render_template("admin/answer_chart.html",
                           chart_datas = json.dumps({'name': chart_names, 'value': chart_values}, ensure_ascii = False))
