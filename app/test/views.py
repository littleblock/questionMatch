# !/user/bin/env/python
# -*- coding:utf-8 -*-
# Author: qixuanye
# Time: 2020/1/21 14:25
from . import test
from app.models import Stu_road, db, Search_log, Function_list
from flask import render_template
import xlrd
import os
import re
import json

@test.route("getData/<id>", methods = ["GET", "POST"])
def getData(id):
    dataList = []
    dataList = reFormat(int(id))
    for x in dataList:
        stuData = Stu_road(
            stu_id = x[0],
            ques_id = id,
            strategy = x[1],
            period1 = x[2],
            period2 = x[3],
            period3 = x[4],
            period4 = x[5],
            is_del = 0
        )
        db.session.add(stuData)
    db.session.commit()
    return "<h1>第</h1>" + id + "<h1>题录入完成</h1>"

# 路径图表
@test.route("八下期末18/<id>", methods = ["GET"])
def dataList(id):
    queryList = Stu_road.query.filter_by(ques_id = id, is_del = 0).all()
    dataList = []
    for x in queryList:
        data = []
        data.append(x.strategy)
        data.append(x.period1)
        data.append(x.period2)
        data.append(x.period3)
        data.append(x.period4)
        dataList.append(data)
    print(dataList)
    return render_template("test/八下期末18题第2问.html", data = dataList)

# 获取excel所有学生数据
def getData():
    filePath = "C:/其他/编码/编码结果/脚本/八下期末18题"
    fileName1 = "八下期末18题.xlsx"
    start = 2
    end = 1002
    data1 = xlrd.open_workbook(os.path.join(filePath, fileName1))
    table1 = data1.sheets()[0]

    data = []
    for x in range(start, end):
        row = table1.row_values(x)
        data.append(row)
    return data

# 重新组装第n道题目,使其变成文本格式
def reFormat(n):
    quesList = []
    for x in getData():
        ques = []
        # 组装学号
        id = str(int(x[0]))
        # 组装策略
        strategy = x[5 * (n - 1) + 1]
        # 组装阶段一
        if not isinstance(x[5 * (n - 1) + 2], str):
            if x[5 * (n - 1) + 2] % 1 == 0.0:
                period1 = str(int(x[5 * (n - 1) + 2]))
            else:
                period1 = str(x[5 * (n - 1) + 2])
        else:
            period1 = x[5 * (n - 1) + 2]
        # 组装阶段二
        if not isinstance(x[5 * (n - 1) + 3], str):
            if x[5 * (n - 1) + 3] % 1 == 0.0:
                period2 = str(int(x[5 * (n - 1) + 3]))
            else:
                period2 = str(x[5 * (n - 1) + 3])
        else:
            period2 = x[5 * (n - 1) + 3]
        # 组装阶段三
        if not isinstance(x[5 * (n - 1) + 4], str):
            if x[5 * (n - 1) + 4] % 1 == 0.0:
                period3 = str(int(x[5 * (n - 1) + 4]))
            else:
                period3 = str(x[5 * (n - 1) + 4])
        else:
            period3 = x[5 * (n - 1) + 4]
        # 组装阶段四
        if not isinstance(x[5 * (n - 1) + 5], str):
            if x[5 * (n - 1) + 5] % 1 == 0.0:
                period4 = str(int(x[5 * (n - 1) + 5]))
            else:
                period4 = str(x[5 * (n - 1) + 5])
        else:
            period4 = x[5 * (n - 1) + 5]
        ques.append(id)
        ques.append(strategy)
        ques.append(period1)
        ques.append(period2)
        ques.append(period3)
        ques.append(period4)
        quesList.append(ques)

    roadList = []
    # 将多个错因整理成单个错因多条路径
    for x in quesList:
        # 若策略为空，设置为z
        if x[1] == "":
            x[1] = 'Z'
        # 按照,分隔
        list1 = re.split(r'[,，]', x[2])
        list2 = re.split(r'[,，]', x[3])
        list3 = re.split(r'[,，]', x[4])
        list4 = re.split(r'[,，]', x[5])
        # 路径拆分
        for a in list1:
            for b in list2:
                for c in list3:
                    for d in list4:
                        road = []
                        road.append(x[0])
                        road.append(x[1])
                        road.append(a)
                        road.append(b)
                        road.append(c)
                        road.append(d)
                        roadList.append(road)
    return roadList

# 进行清洗, 找出不符合业务规范的数据
def dataClean(dataList = []):
    # 8下期末18题清洗
    for x in dataList:
        if x[2] == '0' or x[2] == '21':
            if x[1] != 'Z':
                print(x[0])

