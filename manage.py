# !/user/bin/env/python
# -*- coding:utf-8 -*-
# Author: qixuanye
# Time: 2019/11/14 14:25

from app import app

if __name__ == "__main__":
    # app.run(host = '0.0.0.0', port = 8080)
    app.config["SECRET_KEY"] = "aaaaaa"
    # 设置默认缓存时间
    # app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(seconds = 2)

    app.run(host = '0.0.0.0', debug = True)