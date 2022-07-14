# -*- coding: utf-8 -*-
# @Time    : 2021/11/8 3:58 下午
# @Author  : HuangSir
# @FileName: data_model.py
# @Software: PyCharm
# @Desc:

from pydantic import BaseModel, Field
from typing import List
from app.app.applist_ml.core import AppList, AddList, appListExample, addListExample


class IosCustData(BaseModel):
    # Ios客户数据模型
    busi_id: str = Field(default='1020210717125639000083595', title='交易订单号')
    housing_type: int = Field(default=None, title='住房类型', example=1,
                           description='1：租房、 2：贷款中的自有住房 、3：没有贷款的自有住房、 4：和父母住在一起、 5：单位提供、 6：其他')
    his_sum_rej_cnt: int = Field(default=None, title='历史累计拒绝次数', example=0)
    marriage: int = Field(default=None, title='婚姻', example=1,
                           description='1 ：单身、 2： 已婚 、3 ：离婚 、4： 丧偶')
    current_debt_amount: float = Field(default=None, title='当前共债金额', example=1000.0)
    gender: int = Field(default=None, title='性别', example=1, description='1:男;2女')
    income: int = Field(default=None, title='收入', example=1, description='1:8000以下;2;在8000和15000之间;3;15000以上;')
    education: int = Field(default=None, title='教育程度', example=5,
                           description='1:小学、2:初中、3:高中 4:大专、 5:本科、6:其他')
    customer_type: int = Field(default=None, title='用户类型', example=2,
                           description='1： 私营业主、 2：上班族、 3：自由职业（摩的司机/农民/渔夫等、）4：退休/待业/无业/家庭主妇')
    emergency_contact_cor_customer_num: int = Field(default=None, title='紧急联系人关联用户数量', example=0,
                                                    description='0,1,2,3 ...')
    work_type: int = Field(default=None, title='职位', example=1,
                           description='1:正式员工(2年以下); 2:正式员工(2年以上); 3:经理; 4:高管; 5:外包; 6:临时合同工')
    industry: int = Field(default=None, title='行业', example=59, description='50:it;51:医师;52:养殖员;53:农民;54:建筑师;'
                                                                            '55:司机;56:售货员;57:学生;58:会计;59:生意人;'
                                                                            '60:警察;61:渔民;62:商贩;63:教师;64:公务员;'
                                                                            '65:律师;66:军人;67:金融机构;68:餐饮;69:其他;')
    device_cor_name_num: int = Field(default=None, title='设备关联姓名数量', example=2)
    identity_cor_name_num: int = Field(default=None, title='身份证关联姓名数量', example=2)
    identity_cor_mobile_num: int = Field(default=None, title='身份证关联手机号数量', example=2)
    identity_register_product: int = Field(default=None, title='身份证注册过的产品数量', example=1)
    re_7d_apply_num: int = Field(default=0, title='近7天申请次数', example=0, description='0,1,2,3 ...')
    date_of_birth: str = Field(default=None, title='出生日期', example='2002-01-06',
                            description='yyyy-mm-dd')
    OTHER: List[AddList] = Field(default=..., example=addListExample, title='通讯录', description='通讯录详情')
    create_time: str = Field(default=None, title='订单时间', example='2022-01-06 09:39:24',
                             description='yyyy-mm-dd HH:MM:SS')
    mobile_brand: str = Field(default=None, title='手机品牌', example='iPhone')
    mobile_model: str = Field(default=None, title='手机型号', example='iPhone 12 Pro')
    RAM: str = Field(default=None, title='RAM', example='564 MB/2.77 GB')
    db_name: int = Field(default=None, title='库名', example=5, description='4表示jf29,5表示jf40,0表示其他')


class AndCustData(BaseModel):
    # 安卓客户数据模型
    busi_id: str = Field(default='1020210717125639000083595', title='交易订单号')
    his_sum_rej_cnt: int = Field(default=None, title='历史累计拒绝次数', example=0)
    marriage: int = Field(default=None, title='婚姻', example=1,
                          description='1 ：单身、 2： 已婚 、3 ：离婚 、4： 丧偶')
    phone_version_num: int = Field(default=None, title='手机版本号', example=10)
    income: int = Field(default=None, title='收入', example=1, description='1:8000以下;2;在8000和15000之间;3;15000以上;')
    education: int = Field(default=None, title='教育程度', example=5,
                           description='1:小学、2:初中、3:高中 4:大专、 5:本科、6:其他')
    customer_type: int = Field(default=None, title='用户类型', example=2,
                               description='1： 私营业主、 2：上班族、 3：自由职业（摩的司机/农民/渔夫等、）4：退休/待业/无业/家庭主妇')
    emergency_contact_cor_customer_num: int = Field(default=None, title='紧急联系人关联用户数量', example=0,
                                                    description='0,1,2,3 ...')
    work_type: int = Field(default=None, title='职位', example=1,
                           description='1:正式员工(2年以下); 2:正式员工(2年以上); 3:经理; 4:高管; 5:外包; 6:临时合同工')
    industry: int = Field(default=None, title='行业', example=59, description='50:it;51:医师;52:养殖员;53:农民;54:建筑师;'
                                                                            '55:司机;56:售货员;57:学生;58:会计;59:生意人;'
                                                                            '60:警察;61:渔民;62:商贩;63:教师;64:公务员;'
                                                                            '65:律师;66:军人;67:金融机构;68:餐饮;69:其他;')
    re_24h_apply_num: int = Field(default=None, title='近24小时申请次数', example=0, description='0,1,2,3 ...')
    re_7d_apply_num: int = Field(default=0, title='近7天申请次数', example=0, description='0,1,2,3 ...')
    db_name: int = Field(default=None, title='库名', example=5, description='1表示jf09，2表示jf10，3表示jf15，4表示jf29，5表示jf40, 0表示其他')
    is_daichao: int = Field(default=None, title='是否贷超', example=1, description='1表示贷超，0表示非贷超')
    RAM: str = Field(default=None, title='RAM', example='564 MB/2.77 GB')
    date_of_birth: str = Field(default=None, title='出生日期', example='2002-01-06',
                               description='yyyy-mm-dd')
    APPLIST: List[AppList] = Field(default=..., example=appListExample, title='appList', description='applist详情')
    OTHER: List[AddList] = Field(default=..., example=addListExample, title='通讯录', description='通讯录详情')
    create_time: str = Field(default=None, title='订单时间', example='2022-01-06 09:39:24',
                            description='yyyy-mm-dd HH:MM:SS')
    mobile_brand: str = Field(default=None, title='手机品牌', example='samsung')
    mobile_model: str = Field(default=None, title='手机型号', example='SM-A920F')

