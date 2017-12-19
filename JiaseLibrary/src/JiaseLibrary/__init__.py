# -*- coding:utf-8 -*-

import os
import requests
import configparser
from keywords import *
from utils import *
from version import VERSION
from faker.factory import Factory

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONF_PATH = BASE_DIR  + "\\JiaseLibrary\\config\\config.cfg"

__version__ = VERSION

class JiaseLibrary(
    _LambdaSysAuthKeywords,
    _LambdaSysOrganizeKeywords,
    _LambdaSysUserKeywords,
    _LambdaCustomerKeywords,
    _LambdaLoanKeywords,
    _LambdaContractKeywords,
    _LambdaWithdrawalKeywords,
    _LambdaRepaymentKeywords
):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self):
        self._init_request_arg()
        self._faker   = Factory.create(locale='zh_CN')        
        self._get_config_lambda()
        
    def _get_config_lambda(self):
        cf = configparser.ConfigParser()
        cf.read(CONF_PATH,encoding='utf-8')
        self._lambda_host                   = cf.get('lambda_web','lambda_host')
        self._lambda_port                   = cf.get('lambda_web','lambda_port')
        self._lambda_url                    = 'http://%s:%s' %(self._lambda_host,self._lambda_port)     
        self._lambda_all_psd                = cf.get('lambda_roles','lambda_all_psd') 
        self._lambda_super_admin            = cf.get('lambda_roles','lambda_super_admin')           
        self._lambda_admin                  = cf.get('lambda_roles','lambda_admin')                 
        self._lambda_invest_manager         = cf.get('lambda_roles','lambda_invest_manager')        
        self._lambda_invest_major           = cf.get('lambda_roles','lambda_invest_major')          
        self._lambda_inner_audit            = cf.get('lambda_roles','lambda_inner_audit')           
        self._lambda_audit_1                = cf.get('lambda_roles','lambda_audit_1')               
        self._lambda_audit_2                = cf.get('lambda_roles','lambda_audit_2')               
        self._lambda_audit_3                = cf.get('lambda_roles','lambda_audit_3')               
        self._lambda_financial_review_audit = cf.get('lambda_roles','lambda_financial_review_audit')
        self._lambda_loans_a                = cf.get('lambda_roles','lambda_loans_a')               
        self._lambda_loans_b                = cf.get('lambda_roles','lambda_loans_b')               
        self._lambda_finance_director       = cf.get('lambda_roles','lambda_finance_director')      
        self._lambda_repay_match            = cf.get('lambda_roles','lambda_repay_match')           
        self._lambda_meeting_audit          = cf.get('lambda_roles','lambda_meeting_audit')
        self._lambda_db_env                 = cf.get('lambda_db_decryption', 'lambda_db_env')

    def _init_request_arg(self):
        self._request = requests.session()
        self._headers = {"Content-Type": "application/json"}



if __name__ == '__main__':
    jiase = JiaseLibrary()


    #jiase.login_lambda(role='lambda_invest_manager')#投资经理登录
    #jiase.sign_loan_contract(88)

    #jiase.add_custom_personal(cust_kind='DKKH')
    #jiase.add_loan()
    """
    # 从提款申请到审核通过，步骤如下：
    withdrawal_detailId, custId = jiase.create_withdrawal_apply('黎华县', 'GR')
    details, bizCode = jiase.withdrawal_apply_view(withdrawal_detailId)
    payAmt = jiase.add_withdrawal_account(details, custId, payName='毛峰尖', payType='GR', payAmt=3000, Duration='5')
    jiase.save_withdrawal_apply(withdrawal_detailId, payAmt)
    withdrawalId = details['withdrawalId']  # 获取提款申请id
    jiase.submit_withdrawal_apply(withdrawalId)
    print("---------------------------------提款申请已经完成，下面进入审核流程---------------------------------")
    #A岗
    jiase.login_lambda(role='lambda_loans_a')   # 放款岗A登录
    taskId = jiase.get_withdrawal_taskId(bizCode)
    jiase.receive_withdrawal_task(taskId)
    jiase.save_withdrawal_apply(withdral_detailId, payAmt)  # 保存提款详情
    jiase.save_withdrawal_advice(taskId, withdrawalId, withdral_detailId)
    # #运行接口发现放款岗没有手动拆借据也可以审核通过
    totalAmt, iou_list = jiase.get_withdrawal_iou(withdrawalId)
    if totalAmt !=0:
        jiase.create_withdrawal_iou(totalAmt,'6',withdrawalId)
    jiase.withdrawal_apply_pass(taskId,withdrawalId)
    #B岗
    jiase.login_lambda(role='lambda_loans_b')   # 放款岗B登录
    taskId = jiase.get_withdrawal_taskId(bizCode)
    jiase.receive_withdrawal_task(taskId)
    jiase.save_withdrawal_apply(withdral_detailId, payAmt)  # 保存提款详情
    jiase.save_withdrawal_advice(taskId, withdrawalId, withdral_detailId)
    # #运行接口发现放款岗没有手动拆借据也可以审核通过
    totalAmt = jiase.get_withdrawal_iou(withdrawalId)
    if totalAmt !=0:
        jiase.create_withdrawal_iou(totalAmt,'6',withdrawalId)
    jiase.withdrawal_apply_pass(taskId,withdrawalId)
    """
    # jiase.add_lambda_user(branch_name=u'投资发展六部',dept_name=u'市场部',position_name=u'投资经理岗',role_name=u'投资经理')
