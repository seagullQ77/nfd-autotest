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
        self._lambda_invest_develop         = cf.get('lambda_roles', 'lambda_invest_develop')
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

    #合同签订
    # jiase.login_lambda(role='lambda_invest_manager')#投资经理登录
    #jiase.sign_loan_contract(88)

    """
    #提前还款申请
    jiase.login_lambda(role='lambda_invest_manager')#投资经理登录
    jiase.submit_prepay_apply(lend_code='IOU2017110300021',acc_entry_date='2017/12/30')

    #提前还款审批
    jiase.login_lambda(role='lambda_invest_major')
    jiase.prepay_apply_aduit_pass(71,"Y")
    #jiase.prepay_apply_aduit_back(71, "Y")

    jiase.login_lambda(role='lambda_invest_develop')
    jiase.prepay_apply_aduit_pass(71, "Y")
    #jiase.prepay_apply_aduit_back(71,"Y")
    
    """
    #减免利息:财务清算总监——>财务总监
    jiase.login_lambda(role='lambda_financial_clearing_director')
    jiase.prepay_apply_aduit_pass(71,"Y")
    #jiase.prepay_apply_aduit_back(71, "Y")
    jiase.login_lambda(role='lambda_chief_financial_officer')
    jiase.prepay_apply_aduit_pass(71,"Y")
    #jiase.prepay_apply_aduit_back(71, "Y")

    #减免违约金：贷后管理部总监——>风险管理部负责人
    jiase.login_lambda(role='lambda_management_after_loan_major')
    jiase.prepay_apply_aduit_pass(71, "Y")
    #jiase.prepay_apply_aduit_back(71, "Y")
    jiase.login_lambda(role='lambda_risk_management')
    jiase.prepay_apply_aduit_pass(71, "Y")
    #jiase.prepay_apply_aduit_back(71, "Y")

    #资金清算岗——>财务复核岗
    jiase.login_lambda(role='lambda_fund_clearing_post')
    #self.prepay_apply_aduit_pass(71, "Y", 'lambda_fund_clearing_post', prepay_info[0], prepay_info[1])
    #jiase.prepay_apply_aduit_back(71, "Y")
    #self.prepay_apply_aduit_pass(71, "Y", 'lambda_financial_review_audit', prepay_info[0], prepay_info[1])
    jiase.prepay_apply_aduit_pass(71, "Y")
    #jiase.prepay_apply_aduit_back(71, "Y")







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


    #jiase.login_lambda(role='lambda_invest_manager')

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



