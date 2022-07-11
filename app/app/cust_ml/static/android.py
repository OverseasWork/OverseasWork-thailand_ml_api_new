import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import json
import joblib
from app_utils import getuserinstallupdateappcategory,cal_add_feat


def is_daichao(df):
    if (df.db_name==1 and df.CORP_NO==21) or (df.db_name==2 and df.CORP_NO in [20,21]) or (df.db_name==3 and df.CORP_NO==20) or (df.db_name==4 and df.CORP_NO in [20,21,22]):
        return 1
    else:
        return 0


def cal_ram_rom(df):
    ram_rom = []
    try:
        for i in str(df.RAM).split('/'):
            if i.endswith('MB'):
                ram_rom.append(float(i.replace('MB', '')) / 1024)
            elif i.endswith('GB'):
                ram_rom.append(float(i.replace('GB', '')))
            else:
                ram_rom.extend([float(i), -999])
        return ram_rom
    except Exception as e:
        return [0, 0]


def prob2score(prob,basePoint=600,PDO=50,odds=20):
    # 将概率转化成分数且为正整数
    y = np.log(prob/(1-prob))
    a = basePoint - y * np.log(odds)
    y2 = a - PDO/np.log(2)*(y)
    score = y2.astype('int')
    return score


if __name__=="__main__":
    # 加载所需文件
    lgb_model=joblib.load('newModel_0704.pkl')
    feat_cols=[i.strip() for i in open('feat_0704.txt','r',encoding='utf8').readlines()]
    category_cols=[i.strip() for i in open('cat_feat_0704.txt','r',encoding='utf8').readlines()]
    with open("mobile_brand_map_and.json", 'r', encoding='utf-8') as fw:
        mobile_brand_map = json.load(fw)
    comp = pd.read_excel('comp.xlsx')
    # 读取测试数据
    # data=pd.read_csv('1020220604223603000258016.csv')
    # data = pd.read_csv('1020211228085551000002187.csv')
    data = pd.read_csv('1020211230125657000004355.csv')


    #计算app，add
    app_df=pd.DataFrame(json.loads(data['APPLIST'].values[0]))
    add_df=pd.DataFrame(json.loads(data['OTHER'].values[0]))

    appfeat=getuserinstallupdateappcategory(app_df,data['CREATE_TIME'].values[0],comp)
    addfeat=cal_add_feat(add_df,data['CREATE_TIME'].values[0])

    #特征处理
    data['手机版本号']=data['手机版本号'].apply(lambda x: int(str(x)[0]))
    data[['ramx','ramy']]=data.apply(cal_ram_rom, result_type="expand", axis=1)
    data['age']=data.apply(lambda x:-9999 if 2022-int(x['出生日期'][:4])<0 or 2022-int(x['出生日期'][:4])>=100 else 2022-int(x['出生日期'][:4]),axis=1)
    data['mobile_brand']=data.apply(lambda x: mobile_brand_map.get('-'.join([str(x['手机品牌']).lower(),str(x['手机型号']).lower()]),-999),axis=1)
    data.replace('NO_HIT',0,inplace=True)
    data.fillna(0,inplace=True)
    data2=pd.concat([data,appfeat,addfeat],axis=1)
    for i in feat_cols:
        if i not in data2.columns:
            print(i)
            data2[i]=0
    #入模数据
    res_data=data2[feat_cols]
    #预测
    lgb_prob = np.mean([i.predict(res_data) for i in lgb_model], axis=0)[0]
    print(lgb_prob)
    score=prob2score(lgb_prob,600,40,1)
    print(score)