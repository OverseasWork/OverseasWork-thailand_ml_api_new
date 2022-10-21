# -*- coding: utf-8 -*-
# @Time    : 2020/10/29 5:08 下午
# @Author  : HuangSir
# @FileName: ml_utils.py
# @Software: PyCharm
# @Desc:

import numpy as np
import pandas as pd
import json, re, gc
import datetime
import itertools


path = 'app/app/cust_ml/static/'


def cal_ram_rom(df):
    ram_rom = []
    try:
        for i in str(df.RAM).split('/'):
            if i.endswith('MB'):
                ram_rom = [float(i.replace('MB', '')) / 1024,0]
            elif i.endswith('GB'):
                ram_rom = [float(i.replace('GB', '')),0]
            else:
                ram_rom = [float(i), -999]
        return ram_rom
    except Exception as e:
        return [0, 0]


def prob2score(prob,basePoint=600, PDO=50, odds=20):
    # 将概率转化成分数且为正整数
    y = np.log(prob/(1-prob))
    a = basePoint - y * np.log(odds)
    y2 = a - PDO/np.log(2)*(y)
    score = y2.astype('int')
    return score


def is_daichao(df):
    if (df.db_name==1 and df.CORP_NO==21) or (df.db_name==2 and df.CORP_NO in [20,21]) or (df.db_name==3 and df.CORP_NO==20) or (df.db_name==4 and df.CORP_NO in [20,21,22]):
        return 1
    else:
        return 0


def CalTwotimeStampDiffDays(datetime1,datetime2,deltamin=0):
    return (datetime2-datetime1).days+round((datetime2-datetime1).seconds/3600/24,4)+round(deltamin/60/24,4)


def TransformTimeStampToDatetime(timestamps):
    return datetime.datetime.fromtimestamp(timestamps)


def TwoNumDivision(x,y):
    if x==0 and y==0:
        return 0
    else:
        if (y==0 and x!=0) or (y!=y) or (x!=x):
            return np.nan
        else:
            return round(x/y, 4)


def getuserinstallupdateappcategory(applist_df, apply_times,comp):
    apptotalcates = comp.app_type.unique().tolist()
    times_map = {1: '1d', 3: '3d', 7: '1w', 14: '2w', 21: '3w', 30: '1m', 60: '2m', 90: '3m'}
    prefixtimes = ['firstTime', 'lastTime']
    prefixtimes1 = [x for x in times_map.values()]
    prefixtail1 = ['apptotalnums', 'sysappnums', 'nosysappnums', 'sysappnumspct', 'nosysappnumspct']
    prefixtail2 = ['appnums', 'appnumstoall', 'nosysappnums', 'nosysappnumstoall', 'catpct', 'catpct_all']

    columnslist1 = ['{0}_{1}_{2}'.format(x[0], x[1], x[2]) for x in
                    itertools.product(prefixtimes1, prefixtimes, prefixtail1)]
    columnslist2 = ['{0}_{1}_{2}_{3}'.format(x[0], x[1], x[2], x[3]) for x in
                    itertools.product(prefixtimes1, prefixtimes, apptotalcates, prefixtail2)]

    columnslist3 = ['{0}_{1}_{2}_{3}'.format(x[0], x[1], x[2], x[3]) for x in
                    itertools.product(prefixtimes1, ['firsted', 'lasted'], apptotalcates, prefixtail2)]

    columnslisttotal = columnslist1 + columnslist2 + columnslist3
    zerodictdf = pd.DataFrame(0, index=[0],columns=columnslisttotal)

    apply_times = pd.to_datetime(apply_times)
    total_num = applist_df.shape[0]
    if applist_df.empty:
        return zerodictdf
    prefix1 = ['firstTime', 'lastTime']
    prefix2 = [x for x in times_map.keys()]
    prefix_combination = [x for x in itertools.product(prefix2, prefix1)]
    featurelist = {}
    for x in prefix_combination:
        days = x[0]
        timename = x[1]
        installupdatprefix = timename.replace('Time', '') + 'ed'
        daysprefix = times_map[days]
        applist_df[timename] = pd.to_datetime(applist_df[timename])  # .astype('int')
        applist_df['{}_apply_internal'.format(installupdatprefix)] = applist_df[timename].apply(
            lambda x: np.nan if x != x else CalTwotimeStampDiffDays(x, apply_times))
        applist_temp = applist_df[(applist_df['{}_apply_internal'.format(installupdatprefix)] >= 0) & (
                    applist_df['{}_apply_internal'.format(installupdatprefix)] <= days)]
        pkgnamelist = list(set(applist_temp['packageName'].values.tolist()))
        apptotalnum = len(pkgnamelist)
        if 'systemApp' in applist_temp.columns.tolist():
            # 计算系统性APP与非系统性APP对应的数量与占比
            sysappnum = applist_temp[(applist_temp['systemApp'] == 1)]['packageName'].nunique()
            nosysappnum = applist_temp[(applist_temp['systemApp'] == 2)]['packageName'].nunique()
            #             nosysappnum = len(nosyspkgnamelist)
            #             sysappnum = len(syspkgnamelist)
            sysappnumpct = TwoNumDivision(sysappnum, apptotalnum)
            nosysappnumpct = TwoNumDivision(nosysappnum, apptotalnum)
        else:
            nosysappnum = np.nan
            sysappnum = np.nan
            sysappnumpct = np.nan
            nosysappnumpct = np.nan
        featurelist['{0}_{1}_apptotalnums'.format(daysprefix, installupdatprefix)] = [apptotalnum]
        featurelist['{0}_{1}_sysappnums'.format(daysprefix, installupdatprefix)] = [sysappnum]
        featurelist['{0}_{1}_nosysappnums'.format(daysprefix, installupdatprefix)] = [nosysappnum]
        featurelist['{0}_{1}_sysappnumspct'.format(daysprefix, installupdatprefix)] = [sysappnumpct]
        featurelist['{0}_{1}_nosysappnumspct'.format(daysprefix, installupdatprefix)] = [nosysappnumpct]
        # 获取所有安装或更新的APP在APP分类列表中能够找到的结果
        comp_df = comp[(comp['package'].isin(pkgnamelist))]
        for cate in apptotalcates:
            # 获取某个分类下的包名，并计算相应的所有包，计算列表长度作为新增的APP数据
            comp_df1 = comp_df[(comp_df['app_type'] == cate)]
            cateapps = list(set(comp_df1['package'].values.tolist()))
            # 计算单个分类下的APP占安装的APP总数的比例
            cateappnums = len(cateapps)
            cateappnumspct = TwoNumDivision(cateappnums, apptotalnum)
            cateallpct = TwoNumDivision(cateappnums,total_num)
            # 计算其中的系统与非系统APP对应的总数以及在整体中的占比情况
            applist_temp_1 = applist_temp[(applist_temp['packageName'].isin(cateapps))]
            if 'systemApp' in applist_temp_1.columns.tolist():
                nosyscateappnums = applist_temp_1[(applist_temp_1['systemApp'] == 2)]['packageName'].nunique()
                nosyscateappnumstoall = TwoNumDivision(nosyscateappnums, nosysappnum)
            else:
                nosyscateappnums = np.nan
                nosyscateappnumstoall = np.nan
            featurelist['{0}_{1}_{2}_appnums'.format(daysprefix, installupdatprefix, cate)] = [cateappnums]
            featurelist['{0}_{1}_{2}_appnumstoall'.format(daysprefix, installupdatprefix, cate)] = [cateappnumspct]
            featurelist['{0}_{1}_{2}_nosysappnums'.format(daysprefix, installupdatprefix, cate)] = [nosyscateappnums]
            featurelist['{0}_{1}_{2}_nosysappnumstoall'.format(daysprefix, installupdatprefix, cate)] = [nosyscateappnumstoall]
            featurelist['{0}_{1}_{2}_catpct'.format(daysprefix, installupdatprefix, cate)] = [ cateappnumspct]
            featurelist['{0}_{1}_{2}_catpct_all'.format(daysprefix, installupdatprefix, cate)] = [cateallpct]
            del nosyscateappnums, nosyscateappnumstoall, comp_df1, cateappnums, cateappnumspct, cateapps
        del applist_temp, pkgnamelist, apptotalnum, nosysappnum, sysappnum, sysappnumpct, nosysappnumpct, comp_df
        gc.collect()
    return pd.DataFrame.from_dict(featurelist)

def cal_add_feat(addlist_df, apply_times):
    times_map = {1: '1d', 3: '3d', 7: '1w', 14: '2w', 21: '3w', 30: '1m', 60: '2m', 90: '3m'}
    prefixtimes = ['last_time']
    prefixtimes1 = [x for x in times_map.values()]
    prefixtail1 = ['totalnums', 'namenodupnums', 'mobilenodupnums', 'namenoduppct', 'mobilenoduppct']
    columnslisttotal = ['{0}_{1}_{2}'.format(x[0], x[1], x[2]) for x in itertools.product(prefixtimes1, prefixtimes, prefixtail1)]

    columnslisttotal2 = ['{0}_{1}_{2}'.format(x[0], x[1], x[2]) for x in itertools.product(prefixtimes1, ['last_ed'], prefixtail1)]
    # zerodict = {}
    # for x in columnslisttotal:
    #     zerodict[x] = 0
    zerodictdf_add = pd.DataFrame(0, index=[0],columns=columnslisttotal+columnslisttotal2)
    add_total_num = addlist_df.shape[0]
    add_name_no_dup = addlist_df.other_name.nunique()
    add_mobile_no_dup = addlist_df.other_mobile.nunique()
    name_dup_pct = TwoNumDivision(add_name_no_dup, add_total_num)
    mobile_dup_pct = TwoNumDivision(add_mobile_no_dup, add_total_num)

    apply_times = pd.to_datetime(apply_times)
    if addlist_df.empty:
        zerodictdf_add[['add_total_num', 'add_name_no_dup', 'add_mobile_no_dup','name_dup_pct', 'mobile_dup_pct']] = [0, 0,0, 0,0]
        return zerodictdf_add
    elif 'last_time' not in addlist_df.columns or addlist_df['last_time'].nunique() == 1:
        zerodictdf_add[['add_total_num', 'add_name_no_dup', 'add_mobile_no_dup', 'name_dup_pct', 'mobile_dup_pct']] = [
            add_total_num, add_name_no_dup, add_mobile_no_dup, name_dup_pct, mobile_dup_pct]
        return zerodictdf_add
    prefix1 = ['last_time']
    prefix2 = [x for x in times_map.keys()]
    prefix_combination = [x for x in itertools.product(prefix2, prefix1)]
    featurelist = {}
    for x in prefix_combination:
        days = x[0]
        timename = x[1]
        installupdatprefix = timename.replace('time', '') + 'ed'
        daysprefix = times_map[days]
        if str(addlist_df[timename][0]).startswith('1'):
            addlist_df[timename] = addlist_df[timename].apply(
                lambda x: TransformTimeStampToDatetime(int(x) // 1000))  # TransformTimeStampToDatetime
        else:
            addlist_df[timename] = pd.to_datetime(addlist_df[timename])  # .astype('int')
        addlist_df['{}_apply_internal'.format(installupdatprefix)] = addlist_df[timename].apply(
            lambda x: np.nan if x != x else CalTwotimeStampDiffDays(x, apply_times))
        addlist_temp = addlist_df[(addlist_df['{}_apply_internal'.format(installupdatprefix)] >= 0) & (
                addlist_df['{}_apply_internal'.format(installupdatprefix)] <= days)]
        if not addlist_temp.empty:
            totalnums = addlist_temp.shape[0]
            namenodupnums = addlist_temp['other_name'].nunique()
            mobilenodupnums = addlist_temp['other_mobile'].nunique()
            namenoduppct = TwoNumDivision(namenodupnums, totalnums)
            mobilenoduppct = TwoNumDivision(mobilenodupnums, totalnums)
        else:
            totalnums = 0
            namenodupnums = 0
            mobilenodupnums = 0
            namenoduppct = 0
            mobilenoduppct = 0

        featurelist['{0}_{1}_totalnums'.format(daysprefix, installupdatprefix)] = [totalnums]
        featurelist['{0}_{1}_sysappnums'.format(daysprefix, installupdatprefix)] = [namenodupnums]
        featurelist['{0}_{1}_mobilenodupnums'.format(daysprefix, installupdatprefix)] = [mobilenodupnums]
        featurelist['{0}_{1}_namenoduppct'.format(daysprefix, installupdatprefix)] = [namenoduppct]
        featurelist['{0}_{1}_mobilenoduppct'.format(daysprefix, installupdatprefix)] = [mobilenoduppct]
        featurelist_df = pd.DataFrame.from_dict(featurelist)
        featurelist_df[['add_total_num', 'add_name_no_dup', 'add_mobile_no_dup', 'name_dup_pct', 'mobile_dup_pct']] = [
            add_total_num, add_name_no_dup, add_mobile_no_dup, name_dup_pct, mobile_dup_pct]
    return featurelist_df