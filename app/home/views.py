# !/user/bin/env/python
# -*- coding:utf-8 -*-
# Author: qixuanye
# Time: 2019/11/14 14:25

# 导入该模块中蓝图对象home
from . import home
from flask import render_template, redirect, request, session, url_for
from .forms import query_form
from app.models import Function_list, Question_base, Answer_base, Func_ques_relation, Search_log, db, Temp, Keyword_bus, \
    Answer_log
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
# 调用百度SDK
from aip import AipNlp
import requests, json, time, threading

URL = "https://aip.baidubce.com/rpc/2.0/nlp/v2/simnet"
ACCESS_TOKEN = '24.39643d723879576481b053c4f67e9c6c.2592000.1581593348.282335-17973538'
# 百度SDK所需参数
APP_ID = '17973538'
API_KEY = 'yZjSKKtG1N5yudQg3Zml9MEh'
SECRET_KEY = 'LAPBsxEXpPHAoX4D3QUUbc2Q86NGSnG7'


# 查询路由
@home.route("/query", methods = ["GET", "POST"])
def query():
    form = query_form()
    if request.method == "GET":
        form.function_type.choices = [(v.func_id, v.func_name) for v in Function_list.query.filter_by(is_del = 0)]
    if form.validate_on_submit():
        data = form.data
        search_record = Search_log(
            func_id = data["function_type"],
            search_text = data["content"],
            ques_sort = 1,
            create_time = datetime.now()
        )
        db.session.add(search_record)
        db.session.commit()
        return redirect(
            url_for('home.query_list', page = 1, type = data["function_type"], content = search_record.search_text))

    return render_template("home/query.html", form = form)

# 查询列表
@home.route("/query/list", methods = ["GET", "POST"])
def query_list():
    # 获取url中的参数值
    page = int(request.args.get("page"))
    type = int(request.args.get("type"))
    content = request.args.get("content")
    # 获取查询分类下的问题信息
    question_datas = Func_ques_relation.query.filter_by(func_id = type, is_del = 0).all()
    # 设置线程池
    threadPool = ThreadPoolExecutor(max_workers = 10)
    ques_id_score = {}
    # 多线程返回结果
    for v in question_datas:
        future1 = threadPool.submit(text_compare, content, v.ques_title, v.ques_id)
        def text(future):
            (ques_id, score) = future.result()
            ques_id_score[ques_id] = score
        future1.add_done_callback(text)
        # score1 = text_compare_sdk(content, v.ques_title)
        # ques_id_score[v.ques_id] = text()
    threadPool.shutdown(wait = True)
    print(ques_id_score)
    # 对查询结果排序成倒序
    ques_id_sort = sorted(ques_id_score.items(), key = lambda ques_id_score: ques_id_score[1], reverse = True)

    for v in ques_id_sort:
        query_item = Question_base.query.join(
            Func_ques_relation
            # join(Keyword_bus).
        ).filter(
            Question_base.ques_id == v[0],
            Question_base.is_del == 0,
            Func_ques_relation.is_del == 0
        ).first()
        temp = Temp(
            ques_id = query_item.ques_id,
            ques_title = query_item.ques_title,
            func_type = query_item.func_ques_relations[0].func_id,
            func_name = query_item.func_ques_relations[0].func_name,
            create_time = datetime.now()
        )
        db.session.add(temp)
    db.session.commit()

    page_data = Temp.query.paginate(page = int(page), per_page = 10)

    delete_data = Temp.query.all()
    for m in delete_data:
        db.session.delete(m)
    db.session.commit()
    return render_template("home/query_list.html", title = "查询列表",
                           page_data = page_data, func_type = type, content_text = content)


# 问题详情
@home.route("query/data/<id>", methods = ["GET"])
def question_content(id):
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
    # 将访问记录放入answer_log中
    answer_log = Answer_log(
        ques_id = question.ques_id,
        # 0-无用，1-有用，2-无记录，3-功能没做完
        is_useful = 3,
        search_text = "这是一个测试",
        create_time = datetime.now(),
        is_del = 0
    )
    db.session.add(answer_log)
    db.session.commit()
    return render_template("home/question_content.html", title = "问题详情", question_data = question,
                           function_data = function_type, answer_data = answer, bus_key = bus_key_text)


# @home.route("/test", methods = ["GET", "POST"])
def test():
    text1 = "需求单位找不到该组织，但是可以再月度产值找到"
    text2 = "在工程信息里新增了项目，编制申购计划时，新增的项目不出来"
    response = text_compare(text1, text2)
    print(response)
    return "test"


# 利用百度api获取短文本比较结果,返回最终比较的值
def text_compare(text1, text2, ques_id):
    params = {'access_token': ACCESS_TOKEN,
              'charset': 'UTF-8'}
    headers = {'Content-Type': 'application/json'}
    # text1 = text[0]
    # text2 = text[1]
    body = {"text_1": text1,
            "text_2": text2}
    response = requests.post(URL, json = body, headers = headers, params = params)
    res_dict = json.loads(response.text)
    print(res_dict['score'])
    return ques_id, float(res_dict['score'])

# 利用百度SDK获取短文本比较结果
def text_compare_sdk(text1, text2, ques_id):
    a = 1
    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
    result = client.simnet(text1, text2)
    score = float(result["score"])
    print(score)
    return ques_id, score