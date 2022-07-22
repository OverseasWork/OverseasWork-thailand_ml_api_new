import pandas as pd
import numpy as np
import re
import json
import joblib
import datetime
from conf.log_config import log
from utils.load_utils import load_txt_feat
from utils.ml_utils import prob2score, cal_ram_rom, is_daichao, getuserinstallupdateappcategory, cal_add_feat
import warnings
warnings.filterwarnings('ignore')
import sys
sys.path.append('..')


path = 'app/app/cust_ml/static/'


def ios_risk_score(data: dict):
    try:
        busiId = data['busi_id']
    except:
        busiId = None
    if len(data) <= 1 or busiId is None:
        log.logger.warning(f'{busiId}:Data is empty --------------------------------(ios)')
        return {'score': -9999, 'status_code': 101, 'msg': 'success',
                'detail': '参数错误', 'version': '4.0'}
    try:
        # 主函数
        log.logger.info(f'{busiId}: starting run --------------------------------(ios)')
        data['OTHER'] = json.dumps(data['OTHER'])
        a = json.dumps(data)
        data = pd.DataFrame(json.loads(a), index=[0])
        # 加载所需文件
        lgb_model = joblib.load(f'{path}ios_newModel_0704.pkl')
        feat_cols = [i.strip() for i in open(f'{path}ios_feat_0704.txt', 'r', encoding='utf8').readlines()]
        category_cols = [i.strip() for i in open(f'{path}ios_cat_feat_0704.txt', 'r', encoding='utf8').readlines()]
        with open(f"{path}mobile_brand_map_ios.json", 'r', encoding='utf-8') as fw:
            mobile_brand_map = json.load(fw)

        # 计算add
        add_df = pd.DataFrame(json.loads(data['OTHER'].values[0]))
        addfeat = cal_add_feat(add_df, data['create_time'].values[0])

        # 特征处理
        data[['ramx', 'ramy']] = data.apply(cal_ram_rom, result_type="expand", axis=1)
        data['age'] = data.apply(
            lambda x: -9999 if 2022 - int(x['date_of_birth'][:4]) < 0 or 2022 - int(x['date_of_birth'][:4]) >= 100 else 2022 - int(
                x['date_of_birth'][:4]), axis=1)
        data['mobile_brand'] = data['mobile_brand'].fillna('nan')
        data['mobile_brand'] = data.apply(
            lambda x: mobile_brand_map.get('-'.join([str(x['mobile_brand']).lower(), str(x['mobile_model']).lower()]), -999), axis=1)
        data.replace('NO_HIT', 0, inplace=True)
        data.fillna(0, inplace=True)
        data2 = pd.concat([data, addfeat], axis=1)
        for i in feat_cols:
            if i not in data2.columns:
                data2[i] = 0
        # 入模数据
        res_data = data2[feat_cols]
        # 预测
        lgb_prob = np.mean([i.predict(res_data) for i in lgb_model], axis=0)[0]
        score = prob2score(lgb_prob, 600, 40, 1)
        result = {'score': int(score), 'msg': 'success', 'status_code': 100, 'busiId': busiId, 'version': '4.0'}
        log.logger.info(f'{busiId}:finish predict,score:{int(score)} --------------------------------(ios)')
        return result
    except Exception as error:
        log.logger.error(f'{busiId},-----> {str(error)}-----------(ios)')
        return {'busiId': busiId, 'status_code': 102, 'msg': 'fail', 'detail': str(error), 'version': '4.0'}


def and_risk_score(data: dict):
    try:
        busiId = data['busi_id']
    except:
        busiId = None
    if len(data) <= 1 or busiId is None:
        log.logger.warning(f'{busiId}:Data is empty --------------------------------(android)')
        return {'score': -9999, 'status_code': 101, 'msg': 'success',
                'detail': '参数错误', 'version': '4.0'}
    try:
        # 主函数
        log.logger.info(f'{busiId}: starting run --------------------------------(android)')
        data['OTHER'] = json.dumps(data['OTHER'])
        data['APPLIST'] = json.dumps(data['APPLIST'])
        a = json.dumps(data)
        data = pd.DataFrame(json.loads(a), index=[0])
        # 加载所需文件
        lgb_model = joblib.load(f'{path}newModel_0704.pkl')
        feat_cols = [i.strip() for i in open(f'{path}feat_0704.txt', 'r', encoding='utf8').readlines()]
        category_cols = [i.strip() for i in open(f'{path}cat_feat_0704.txt', 'r', encoding='utf8').readlines()]
        with open(f"{path}mobile_brand_map_and.json", 'r', encoding='utf-8') as fw:
            mobile_brand_map = json.load(fw)
        comp = pd.read_excel(f'{path}comp.xlsx')

        # 计算app，add
        app_df = pd.DataFrame(json.loads(data['APPLIST'].values[0]))
        add_df = pd.DataFrame(json.loads(data['OTHER'].values[0]))

        appfeat = getuserinstallupdateappcategory(app_df, data['create_time'].values[0], comp)
        addfeat = cal_add_feat(add_df, data['create_time'].values[0])

        # 特征处理
        data['phone_version_num'] = data['phone_version_num'].apply(lambda x: int(str(x)[0]))
        data[['ramx', 'ramy']] = data.apply(cal_ram_rom, result_type="expand", axis=1)
        data['age'] = data.apply(
            lambda x: -9999 if 2022 - int(x['date_of_birth'][:4]) < 0 or 2022 - int(x['date_of_birth'][:4]) >= 100 else 2022 - int(
                x['date_of_birth'][:4]), axis=1)
        data['mobile_brand'] = data['mobile_brand'].fillna('nan')
        data['mobile_brand'] = data.apply(
            lambda x: mobile_brand_map.get('-'.join([str(x['mobile_brand']).lower(), str(x['mobile_model']).lower()]), -999), axis=1)
        data.replace('NO_HIT', 0, inplace=True)
        data.fillna(0, inplace=True)
        data2 = pd.concat([data, appfeat, addfeat], axis=1)
        for i in feat_cols:
            if i not in data2.columns:
                data2[i] = 0
        # 入模数据
        res_data = data2[feat_cols]
        # 预测
        lgb_prob = np.mean([i.predict(res_data) for i in lgb_model], axis=0)[0]
        score = prob2score(lgb_prob, 600, 40, 1)
        result = {'score': int(score), 'msg': 'success', 'status_code': 100, 'busiId': busiId, 'version': '4.0'}
        log.logger.info(f'{busiId}:finish predict,score:{int(score)} ------------(android)')
        return result
    except Exception as error:
        log.logger.error(f'{busiId},-----> {str(error)}------------(android)')
        return {'busiId': busiId, 'status_code': 102, 'msg': 'fail', 'detail': str(error), 'version': '4.0'}



