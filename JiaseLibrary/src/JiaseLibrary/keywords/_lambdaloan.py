 # -*- coding:utf-8 -*-
import json
from robot.api import logger

class _LambdaLoanKeywords():
    
    def __init__(self):        
        pass
    

    # 提交贷款申请
    # cust_id:借款客户的id
    # 返回loan_id 后续其他接口会用到
    def submit_loan_apply(self,cust_id=None):
        self._get_cust_info_by_id(cust_id)
        return loan_id
    
    # 贷款申请审批通过
    # loan_id:授信申请id
    def loan_apply_aduit_pass(self,loan_id):
        pass 
    
    # 贷款申请审批拒绝
    # loan_id:授信申请id
    def loan_apply_aduit_reject(self,loan_id):
        pass
        
    # 贷款申请审批回退
    # loan_id:授信申请id
    # back_role:回退节点
    def loan_apply_aduit_back(self,loan_id,back_role):
        pass
        
    # 贷款申请审批撤销
    # loan_id:授信申请id
    def loan_apply_aduit_cancel(self,loan_id):
        pass
        
    # 贷款申请审批回收
    # loan_id:授信申请id
    def loan_apply_aduit_retreat(self,loan_id):
        pass