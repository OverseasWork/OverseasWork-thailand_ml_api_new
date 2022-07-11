# -*- coding: utf-8 -*-
# @Time    : 2021/11/6 11:35 下午
# @Author  : HuangSir
# @FileName: ml_router.py
# @Software: PyCharm
# @Desc: 新老客模型路由


from fastapi import APIRouter

from app.app.cust_ml.core import IosCustData, AndCustData
from app.app.cust_ml import ios_risk_score, and_risk_score


ml_router = APIRouter()


@ml_router.post('/customer/score/ios', tags=['IOS客户信用评分'])
async def ios_cust_risk_score(data: IosCustData):
    data = data.dict()
    res = ios_risk_score(data)
    return res


@ml_router.post('/customer/score/android', tags=['安卓客户信用评分'])
async def and_cust_risk_score(data: AndCustData):
    data = data.dict()
    res = and_risk_score(data)
    return res
