 # -*- coding:utf-8 -*-
import json
from robot.api import logger

class _LambdaRepaymentKeywords():
    
    def __init__(self):        
        pass
    

    # 新增还款申请
    # lend_code:借据号
    # issue:期数
    def _create_repayment_apply(self,lend_code=None,issue=None):
        return repayment_id
    
    # 保存还款申请
    # repayment_id 还款申请的id
    def _save_repayment_apply(self,repayment_id):
        pass
    
    # 提交还款申请
    # lend_code:借据号
    # issue:期数
    # repayment_order:入账顺序
    # amount:还款金额
    # 返回 repayment_id
    def submit_repayment_apply(self,lend_code=None,issue=None,repayment_order=None,amount=None):
        return repayment_id
    
    
    # 还款申请审批通过
    # repayment_id: 还款申请id
    def repayment_apply_aduit_pass(self,repayment_id):
        pass
    
    # 还款申请审批拒绝
    # repayment_id: 还款申请的id
    def repayment_apply_aduit_reject(self,repayment_id):
        pass
        
    # 还款申请审批回退
    # repayment_id: 还款申请的id
    # back_role:回退节点
    def repayment_apply_aduit_back(self,repayment_id,back_role):
        pass
        
    # 还款申请审批撤销
    # repayment_id: 还款申请的id
    def repayment_apply_aduit_cancel(self,repayment_id):
        pass
        
    # 还款申请审批回收
    # repayment_id: 还款申请的id
    def repayment_apply_aduit_retreat(self,repayment_id):
        pass
        
    
    
    
    
    # 新增提前还款申请
    # lend_code:借据号
    # issue:期数
    def _create_prepay_apply(self,lend_code=None):
        return prepay_id
    
    # 保存提前还款申请
    # prepay_id 提前还款申请的id
    def _save_prepay_apply(self,prepay_id):
        pass
    
    # 提交提前还款申请
    # lend_code:借据号
    # issue:期数
    # prepay_order:入账顺序
    # amount:还款金额
    # 返回 prepay_id
    def submit_prepay_apply(self,lend_code=None,prepay_type=None,prepay_order=None,amount=None):
        return prepay_id
        
    # 提前还款申请审批通过
    # prepay_id: 提前还款申请id
    def prepay_apply_aduit_pass(self,prepay_id):
        pass
    
    # 提前还款申请审批拒绝
    # prepay_id: 提前还款申请的id
    def prepay_apply_aduit_reject(self,prepay_id):
        pass
        
    # 提前还款申请审批回退
    # prepay_id: 提前还款申请的id
    # back_role:回退节点
    def prepay_apply_aduit_back(self,prepay_id,back_role):
        pass
        
    # 提前还款申请审批撤销
    # prepay_id: 提前还款申请的id
    def prepay_apply_aduit_cancel(self,prepay_id):
        pass
        
    # 提前还款申请审批回收
    # prepay_id: 提前还款申请的id
    def prepay_apply_aduit_retreat(self,prepay_id):
        pass
    