 # -*- coding:utf-8 -*-
import os
import requests
import ConfigParser
from keywords import *
from version import VERSION
from faker.factory import Factory

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CONF_PATH = BASE_DIR  + "\\JiaseLibrary\\config\\config.cfg"


__version__ = VERSION

class JiaseLibrary(
    _LambdaSysAuthKeywords,
    _LambdaSysOrganizeKeywords,
    _LambdaSysUserKeywords,
    _LambdaCustomerKeywords
):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self):
        self._init_request_arg()
        self._faker   = Factory.create(locale='zh_CN')        
        self._get_config_lambda()
        
    def _get_config_lambda(self):
        cf = ConfigParser.ConfigParser()
        cf.read(CONF_PATH)
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
        
    def _init_request_arg(self):
        self._request = requests.session()
        self._headers = {"Content-Type": "application/json"}


if __name__ == '__main__':
    jiase = JiaseLibrary()
    jiase.login_lambda(role='lambda_invest_manager')
    jiase.add_custom_personal(custKind='DKKH')
    #jiase.add_lambda_user(branch_name=u'投资发展七部',dept_name=u'市场部',position_name=u'投资经理岗',role_name=u'投资经理')
