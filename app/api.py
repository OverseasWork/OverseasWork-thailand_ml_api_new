# -*- coding: utf-8 -*-
# @Time    : 2020/10/29 8:49 下午
# @Author  : HuangSir
# @FileName: api.py
# @Software: PyCharm
# @Desc:

from .routers import risk_router_init

from fastapi import FastAPI

description = """
* IOS/Android客户评分越高风险越低,评分范围:\t550~850, <br> **-9999**:\t表示无法评分或程序BUG
* IOS模型入参详情:\t**IosCustData**
* Android模型入参详情:\t**AndCustData**
"""


def create_app():
    app = FastAPI(title='风险评分模型', description=description, version='4.0',
                  redoc_url=None)
    risk_router_init(app)
    return app