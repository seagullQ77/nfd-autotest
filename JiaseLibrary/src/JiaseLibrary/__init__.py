# -*- coding:utf-8 -*-

import os
import requests
import configparser
from JiaseLibrary.keywords._lambdasysauth import _LambdaSysAuthKeywords
from JiaseLibrary.keywords._lambdasysorganize import _LambdaSysOrganizeKeywords
from JiaseLibrary.keywords._lambdasysuser import _LambdaSysUserKeywords
from JiaseLibrary.keywords._lambdacustomer import _LambdaCustomerKeywords
from JiaseLibrary.keywords._lambdaloan import _LambdaLoanKeywords
from JiaseLibrary.keywords._lambdacontract  import _LambdaContractKeywords
from JiaseLibrary.keywords._lambdawithdrawal import _LambdaWithdrawalKeywords
from JiaseLibrary.keywords._lambdarepayment import _LambdaRepaymentKeywords
from JiaseLibrary.keywords._lambdaproduct import _LambdaProductKeywords
from JiaseLibrary.keywords._lambdatransfer import _LambdaTransferKeywords
from JiaseLibrary.utils.lambda_db import LambdaDbCon
from JiaseLibrary.utils.lambda_encrpt import LambdaEncrpt
from JiaseLibrary.version import VERSION
from faker.factory import Factory

from JiaseLibrary.keywords.common.faker import FakerKeywords
from JiaseLibrary.keywords.kappa.mp import KappaMpLibrary

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
    _LambdaRepaymentKeywords,
    _LambdaProductKeywords,
    _LambdaTransferKeywords,
):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self, lambda_host = None, lambda_port = None, lambda_db_host = None):
        self._init_request_arg()
        from faker_nfd import NfdCompanyProvider
        from faker_nfd import NfdCreditCardProvide
        from faker_nfd import NfdDatatimeProvider
        from faker_nfd import NfdLoremProvider
        from faker_nfd import NfdPersonProvider
        from faker_nfd import NfdAddressProvider
        self._faker   = Factory.create(locale='zh_CN')
        self._faker.add_provider(NfdCompanyProvider)
        self._faker.add_provider(NfdCreditCardProvide)
        self._faker.add_provider(NfdDatatimeProvider)
        self._faker.add_provider(NfdLoremProvider)
        self._faker.add_provider(NfdPersonProvider)
        self._faker.add_provider(NfdAddressProvider)
        self.lambda_host = lambda_host
        self.lambda_port = lambda_port
        self.lambda_db_host = lambda_db_host
        self._get_config_lambda()
        self.db = LambdaDbCon(self._lambda_db_host,self._lambda_db_user,self._lambda_db_passwd,self._lambda_db_port,self._lambda_db_charset)

    def _get_config_lambda(self):
        cf = configparser.ConfigParser()
        cf.read(CONF_PATH,encoding='utf-8')
        self._lambda_host                   = self.lambda_host or cf.get('lambda_web','lambda_host')
        self._lambda_port                   = self.lambda_port or cf.get('lambda_web','lambda_port')
        self._lambda_url                    = 'http://%s:%s' %(self._lambda_host,self._lambda_port)


        self._lambda_db_host                = self.lambda_db_host or cf.get('lambda_db','lambda_db_host')

        self._lambda_server_port = cf.get('lambda_web', 'lambda_server_port')
        self._lambda_server_url = 'http://%s:%s' % (self._lambda_host, self._lambda_server_port)

        self._delta_port = cf.get('lambda_web', 'delta_port')
        self._delta_url = 'http://%s:%s' % (self._lambda_host, self._delta_port)

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
        self._lambda_invest_develop         = cf.get('lambda_roles', 'lambda_invest_develop')
        self._lambda_file_transfer          = cf.get('lambda_roles', 'lambda_file_transfer')
        self._lambda_inner_audit            = cf.get('lambda_roles','lambda_inner_audit')           
        self._lambda_audit_1                = cf.get('lambda_roles','lambda_audit_1')               
        self._lambda_audit_2                = cf.get('lambda_roles','lambda_audit_2')               
        self._lambda_audit_3                = cf.get('lambda_roles','lambda_audit_3')               
        self._lambda_financial_review_audit = cf.get('lambda_roles','lambda_financial_review_audit')
        self._lambda_loans_a                = cf.get('lambda_roles','lambda_loans_a')               
        self._lambda_loans_b                = cf.get('lambda_roles','lambda_loans_b')
        #self._lambda_finance_director       = cf.get('lambda_roles','lambda_finance_director')
        self._lambda_repay_match            = cf.get('lambda_roles','lambda_repay_match')           
        self._lambda_meeting_audit          = cf.get('lambda_roles','lambda_meeting_audit')
        self._lambda_db_env                 = cf.get('lambda_db_decryption', 'lambda_db_env')

        self._lambda_management_after_loan_major        = cf.get('lambda_roles', 'lambda_management_after_loan_major')
        self._lambda_risk_management                    = cf.get('lambda_roles', 'lambda_risk_management')
        self._lambda_financial_clearing_director        = cf.get('lambda_roles', 'lambda_financial_clearing_director')
        self._lambda_chief_financial_officer            = cf.get('lambda_roles', 'lambda_chief_financial_officer')
        self._lambda_fund_clearing_post                 = cf.get('lambda_roles', 'lambda_fund_clearing_post')


    def _init_request_arg(self):
        self._request = requests.session()
        self._headers = {"Content-Type": "application/json"}

if __name__ == '__main__':

    jiase = JiaseLibrary()
    jiase.login_lambda(role='lambda_invest_manager')
    #jiase.loan_apply_pass_workflow(loan_apply_id= 7, loan_amount=1000)

    cust_personal_id0 = jiase.custom_personal_create(cust_name='mptest2geren6')
    cust_enterprise_id1 = jiase.custom_enterprise_create(cust_personal_id0, cust_name='mptest2qiye6')





    # 生成授信
    #loan_apply_id = jiase.loan_apply_create(cust_personal_id)

    # 生成授信明细
    # loan_detail_id1 = jiase.loan_apply_prepare_create(loan_apply_id)
    # jiase.loan_detail_self_save(loan_apply_id, loan_detail_id1,'种植贷',self_limit='1000000')
    # jiase.loan_detail_guarantor_save(loan_apply_id, loan_detail_id1,'种植贷',guarantee_limit='50000')
    #
    # # 添加担保方
    # jiase.loan_guarantors_create(loan_detail_id1, 440)
    #
    # # 投资经理提交授信申请
    # jiase.loan_apply_submit(loan_apply_id)

    '''

    # 投资总监处理
    jiase.login_lambda(role='lambda_invest_major')
    jiase.loan_apply_pass(loan_apply_id,is_claim='Y')

    # 内审处理
    jiase.login_lambda(role='lambda_inner_audit')
    jiase.loan_apply_pass(loan_apply_id,is_claim='Y',candidate_group = ['一级审批岗'])

    # 一级审批处理
    jiase.login_lambda(role='lambda_audit_1')
    jiase.loan_apply_back(loan_apply_id,back_position='申请',is_claim='Y')

    # 投资经理提交授信申请
    jiase.login_lambda(role='lambda_invest_manager')
    jiase.loan_apply_submit(loan_apply_id,is_next='N')

    # 一级审批处理
    jiase.login_lambda(role='lambda_audit_1')
    jiase.loan_apply_back(loan_apply_id,back_position='申请',is_claim='Y')

    # 投资经理提交授信申请
    jiase.login_lambda(role='lambda_invest_manager')
    jiase.loan_apply_submit(loan_apply_id,is_next='Y')
    
    '''

'''

        jiase.login_lambda(role='lambda_invest_manager')

        cust_personal_id = jiase.custom_personal_create(cust_name='莫新金')


        group_id1 = jiase.custom_group_create(cust_personal_id1)
        jiase.custom_group_add_member(group_id1,cust_personal_id2)
        jiase.custom_group_update_main_borrower(group_id1,cust_personal_id2)
        jiase.custom_group_delete_member(group_id1,cust_personal_id1)
        jiase.custom_group_delete_member(group_id1,cust_personal_id2)
        jiase.custom_group_add_member(group_id1, cust_personal_id1)
        jiase.custom_group_add_member(group_id1, cust_personal_id2)

        group_id2 = jiase.custom_group_create(cust_personal_id3)
        jiase.custom_group_add_member(group_id2,cust_personal_id4)
        jiase.custom_group_freeze(group_id1,group_id2)
        jiase.custom_group_unfreeze(group_id2, group_id2)

        jiase.custom_group_delete_member(group_id1,cust_personal_id1)
        jiase.custom_group_delete_member(group_id1,cust_personal_id2)
        jiase.custom_group_delete_member(group_id2,cust_personal_id3)
        jiase.custom_group_delete_member(group_id2,cust_personal_id4)

        cust_personal_id = jiase.custom_personal_create(cust_name='test10个人')
        cust_enterprise_id = jiase.custom_enterprise_create(cust_personal_id,cust_name='test10企业')
      '''









