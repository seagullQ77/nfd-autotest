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
        self.db = LambdaDbCon(self._lambda_db_host,self._lambda_db_user,self._lambda_db_passwd,self._lambda_db_port,self._lambda_db_charset)

    def _get_config_lambda(self):
        cf = configparser.ConfigParser()
        cf.read(CONF_PATH,encoding='utf-8')
        self._lambda_host                   = cf.get('lambda_web','lambda_host')
        self._lambda_port                   = cf.get('lambda_web','lambda_port')
        self._lambda_url                    = 'http://%s:%s' %(self._lambda_host,self._lambda_port)

        self._lambda_db_host                = cf.get('lambda_db','lambda_db_host')
        self._lambda_db_user                = cf.get('lambda_db','lambda_db_user')
        self._lambda_db_passwd              = cf.get('lambda_db','lambda_db_passwd')
        self._lambda_db_port                = cf.getint('lambda_db','lambda_db_port')
        self._lambda_db_charset             = cf.get('lambda_db','lambda_db_charset')

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

    jiase.login_lambda(role='lambda_invest_manager')

    # 生成授信
    loan_apply_id = jiase.loan_apply_create('yj_企业9', 'QY')

    # 生成授信明细
    loan_detail_id1 = jiase.loan_apply_prepare_create(loan_apply_id)
    jiase.loan_detail_self_save(loan_apply_id, loan_detail_id1,'yjtest_种植贷',self_limit='100000')
    jiase.loan_detail_guarantor_save(loan_apply_id, loan_detail_id1,'yjtest_种植贷',guarantee_limit='50000')

    # loan_detail_id2 = jiase.loan_apply_prepare_create(loan_apply_id)
    # jiase.loan_detail_self_save(loan_apply_id, loan_detail_id1,'yjtest_经销商贷',self_limit='100000')
    # jiase.loan_detail_guarantor_save(loan_apply_id, loan_detail_id1,'yjtest_经销商贷',guarantee_limit='50000')

    # loan_detail_id3 = jiase.loan_apply_prepare_create(loan_apply_id)
    # jiase.loan_detail_self_save(loan_apply_id, loan_detail_id1,'yjtest_美女贷',self_limit='100000')
    # jiase.loan_detail_guarantor_save(loan_apply_id, loan_detail_id1,'yjtest_美女贷',guarantee_limit='50000')


    # 投资经理提交授信申请
    jiase.loan_apply_submit(loan_apply_id)
    #
    # 投资总监处理
    jiase.login_lambda(role='lambda_invest_major')
    jiase.loan_apply_pass(loan_apply_id,is_claim='Y',is_approved='Y')

    # 内审处理
    jiase.login_lambda(role='lambda_inner_audit')
    jiase.loan_apply_pass(loan_apply_id,is_claim='Y',is_approved='Y',candidate_group=['一级审批岗'])

    # 初审处理
    jiase.login_lambda(role='lambda_audit_1')
    jiase.loan_apply_pass(loan_apply_id,is_claim='Y',is_approved='Y')


