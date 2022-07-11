# -*- coding: utf-8 -*-
# @Time    : 2022/03/17 5:12 下午
# @Author  : HuangSir
# @FileName: api.py
# @Software: PyCharm
# @Desc: 风险评分

from .risk_score import ios_risk_score, and_risk_score


def ios_risk_main(data: dict):
    res = ios_risk_score(data)
    return res


def and_risk_main(data: dict):
    res = and_risk_score(data)
    return res
