 # -*- coding:utf-8 -*-
import json
from robot.api import logger

class _LambdaWithdrawalKeywords():
    
    def __init__(self):        
        pass
    

    # 新建提款申请
    # cust_id:借款客户的id
    # 返回 withdrawal_id 后续其他接口会用到
    def _create_withdrawal_apply(self,cust_id=None):
        self._get_cust_info_by_id(cust_id)
        return withdrawal_id
    
    # 新建支付对象
    def _creat_withdrawal_apply_bank_account(self,withdrawal_id):
        pass
        
    # 保存提款申请
    # withdrawal_id 提款申请的id
    def _save_withdrawal_apply(self,withdrawal_id):
        pass
    
    # 根据提款申请id返回对应的借据号,以供还款模块对应的方法使用 
    # 可能存在拆借据的情况,一个提款申请可能对应多个借据号,因此以列表形式返回    
    def _get_lend_code_by_withdrawal_id(self,withdrawal_id):
        lend_list = []
        return lend_list
    
    # 提交提款申请
    # cust_id:借款客户的id
    # 返回 withdrawal_id 后续其他接口会用到
    def submit_withdrawal_apply(self,cust_id=None):
        withdrawal_id = self._create_withdrawal_apply(cust_id)
        self._creat_withdrawal_apply_bank_account(withdrawal_id)
        self._save_withdrawal_apply(withdrawal_id)
        return withdrawal_id
    
    
    # 提款申请审批通过
    # withdrawal_id: 提款申请id
    def withdrawal_apply_aduit_pass(self,withdrawal_id):
        pass
    
    # 提款申请审批拒绝
    # withdrawal_id: 提款申请id
    def withdrawal_apply_aduit_reject(self,withdrawal_id):
        pass
        
    # 提款申请审批回退
    # withdrawal_id: 提款申请id
    # back_role:回退节点
    def withdrawal_apply_aduit_back(self,withdrawal_id,back_role):
        pass
        
    # 提款申请审批撤销
    # withdrawal_id: 提款申请id
    def withdrawal_apply_aduit_cancel(self,withdrawal_id):
        pass
        
    # 提款申请审批回收
    # withdrawal_id: 提款申请id
    def withdrawal_apply_aduit_retreat(self,withdrawal_id):
        pass