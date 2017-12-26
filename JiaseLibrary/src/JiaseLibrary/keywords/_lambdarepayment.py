 # -*- coding:utf-8 -*-
import json
from robot.api import logger
from _lambdasysauth import _LambdaSysAuthKeywords

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
    # lend_code:借据号IOU2017110300013 IOU2017110300017 IOU2017110300018 IOU2017110300019 IOU2017110300020  IOU2017111300006
    #lendCode=IOU2017110300021
    #IOU2017111300003  IOU2017110300018  IOU2017110300020  IOU2017110300017   IOU2017103000004


    def _query_iou_info(self,lend_code):
        url = '%s/repayment/prepay/apply/listIou'  % self._lambda_url
        params = {"lendCode":lend_code}
        res = self._request.get(url,params=params)
        response = res.content.decode()
        for i in json.loads(response).get("list"):
            for key,value in i.items():
                if key == "lendCode" and value == lend_code:
                    return i.get("custId"),i.get("dueCapital")

    #新建提还申请，用于判断借据是否满足可提还
    def create_prepay_apply(self,lend_code):
        url = '%s/repayment/prepay/apply/create' % self._lambda_url
        payload = {
            "lendCode":lend_code
        }
        res = self._request.post(url,data=payload)
        response = res.content.decode('utf-8')
        statusCode = json.loads(response).get('statusCode')
        statusDesc = json.loads(response).get('statusDesc')
        if statusCode == '0':
            logger.info("新建提还申请成功——"+statusDesc)
            prepay_id = json.loads(response).get('data')
            return prepay_id
        else:
            logger.info(statusDesc)
            raise AssertionError(statusDesc)

    #通过提还类型和提还日期来判断是否能提交提还申请
    def _dueQuery(self,prepayment_type,acc_entry_date,lend_code,prepayment_capital):
        iou_info = self._query_iou_info(lend_code)
        url = '%s/repayment/prepay/apply/dueQuery' % self._lambda_url
        if prepayment_type == 'TQJQ':
            payloads = {
                "accEntryDate":acc_entry_date,
                "prepaymentType" :prepayment_type,
                "custId":iou_info[0],
                "lendCode":lend_code,
                "prepaymentCapital":iou_info[1]
            }
        else:
            payloads = {
                "accEntryDate": acc_entry_date,
                "prepaymentType": prepayment_type,
                "custId": iou_info[0],
                "lendCode": lend_code,
                "prepaymentCapital": prepayment_capital
            }
        res = self._request.post(url, headers=self._headers, data=json.dumps(payloads))
        #res = self._request.post(url,payloads=json.dumps(payloads))
        response = res.content.decode()
        status = json.loads(response).get("statusCode")
        statusDesc = json.loads(response).get("statusDesc")
        if status == '0':
            data = json.loads(response).get("data")
            return status,data.get("residueCapital"),data.get("dueInterest"),data.get("dueMngtCharge"),data.get("dueFree"),iou_info[1]
            #返回应还违约金、应还利息、应还管理费
        else:
            logger.info(statusDesc)
            raise AssertionError(statusDesc)

    # 保存提前还款申请
    # --->暂时不用保存，直接提交提还申请
    # def _save_prepay_apply(self,prepay_id,exemptInterestAmt,exemptLateFeeAmt,exemptMngtAmt):
    #     url = '%srepayment/prepay/apply/save' % self._lambda_url
    #     payloads = {
    #         "exemptInterestAmt" :exemptInterestAmt,
    #         "exemptLateFeeAmt":exemptLateFeeAmt,
    #         "exemptMngtAmt" :exemptMngtAmt,
    #         "id" :prepay_id
    #     }
    #     res = self._request.post(url,headers=self.headers,payloads=json.dumps(payloads))
    #     response = res.content.decode()
    #     status = json.loads(response).get("statusCode")
    #     statusDesc = json.loads(response).get("statusDesc")
    #     if status == 0:
    #         logger.info("保存成功")
    #     else:
    #         logger.info(statusDesc)


    # 提交提前还款申请
    # lend_code:借据号
    #acc_entry_date:提前还款日期
    #prepayment_type="TQJQ":提前还款类型（默认全部结清）
    #exemptCapitalAmt:减免本金
    #exemptInterestAmt:减免利息
    #exemptLateFeeAmt:减免违约金
    #exemptMngtAmt:减免管理费
    #暂不考虑减免罚息exemptPenaltyAmt
    #暂不考虑使用借款方账户余额、质保金
    #return   prepayTotalAmt ,
    def submit_prepay_apply(self,lend_code,acc_entry_date,prepayment_type="TQJQ",prepayment_capital=0,exemptCapitalAmt=0,exemptInterestAmt=0,exemptLateFeeAmt=0,exemptMngtAmt=0):
        url = '%s/repayment/prepay/apply/submit' % self._lambda_url
        prepay_id = self.create_prepay_apply(lend_code)
        due_info = self._dueQuery(prepayment_type,acc_entry_date,lend_code, prepayment_capital)
        realCapitalAmt = due_info[1] - exemptCapitalAmt
        realInterestAmt = due_info[2] - exemptInterestAmt
        realMngtAmt = due_info[3] - exemptMngtAmt
        realLateFeeAmt = due_info[4] - exemptLateFeeAmt
        prepayTotalAmt = realCapitalAmt + realInterestAmt + realMngtAmt + realLateFeeAmt
        acc_entry_date = acc_entry_date - 1
        if due_info[0] == '0':
            payloads = {
                "exemptInterestAmt": exemptInterestAmt,
                "exemptLateFeeAmt": exemptLateFeeAmt,
                "exemptMngtAmt": exemptMngtAmt,
                "exemptCapitalAmt":exemptCapitalAmt,
                "id": prepay_id,
                "version": "0",
                "prepayType": prepayment_type,
                "prepayAmt": due_info[5],
                "prepayTime": acc_entry_date,
                "realCapitalAmt": realCapitalAmt,
                "realInterestAmt": realInterestAmt,
                "realMngtAmt": realMngtAmt,
                "realLateFeeAmt":realLateFeeAmt,
                "exemptPenaltyAmt": "0",
                "realPenaltyAmt": "0",
                "useDepositAmt": "0",
                "useBalanceAmt": "0",
                "prepayTotalAmt": prepayTotalAmt,
                "mustReceiveAmt": prepayTotalAmt,
                "remainIssue": "0",
                "remark": ""
            }
            #res = self._request.post(url, payloads=json.dumps(payloads))
            res = self._request.post(url, headers=self._headers, data=json.dumps(payloads))
            response = res.content.decode()
            status = json.loads(response).get("statusCode")
            statusDesc = json.loads(response).get("statusDesc")
            if status == '0':
                logger.info("提还提交成功")
                return prepayTotalAmt,acc_entry_date
            else:
                logger.info(statusDesc)
                raise AssertionError(statusDesc)



    #提还审批过程

    def _get_prepay_task_list(self,page_no=1,page_size=100):
        url = '%s/workbench/prepayApply/todoList' % self._lambda_url
        payload = {
            "pageNo":page_no,
            "pageSize": page_size
        }
        res = self._request.post(url, headers=self._headers, data=json.dumps(payload))
        response = res.content.decode()
        if json.loads(response).get("statusCode")=='0':
            logger.info("提还任务列表查询成功")
            return json.loads(response).get("list")
        else:
            raise AssertionError('提还任务列表查询失败,错误码:%s,错误信息:%s' % (response.get('statusCode'), response.get('statusDesc')))

    def _get_prepay_task_id(self,prepay_id):
        prepay_task_list = self._get_prepay_task_list()
        for prepay_task in prepay_task_list:
            if str(prepay_task.get("id")) == str(prepay_id):
                prepay_task_id = prepay_task.get("taskId")
                break
        else:
            raise AssertionError("提还任务列表中找不到对应的提还id，提还id:%s" % prepay_id)
        return prepay_task_id


    def _prepay_task_claim(self,prepay_id):
        prepay_task_id = self._get_prepay_task_id(prepay_id)
        url = '%s/workbench/prepayApply/claim' % self._lambda_url
        payload = {
            "taskId":prepay_task_id
        }
        res = self._request.post(url,data=payload)
        response = res.content.decode()
        status = json.loads(response).get("statusCode")
        statusDesc = json.loads(response).get("statusDesc")
        if status == '0':
            logger.info("领取提还任务成功")
        else:
            raise AssertionError("领取提还任务失败——"+statusDesc)

    def _prepay_task_unclaim(self,prepay_id):
        prepay_task_id = self._get_prepay_task_id(prepay_id)
        url = '%s/workbench/prepayApply/unclaim' % self._lambda_url
        payload = {
            "taskId": prepay_task_id
        }
        res = self._request.post(url, data=payload)
        response = res.content.decode()
        status = json.loads(response).get("statusCode")
        statusDesc = json.loads(response).get("statusDesc")
        if status == '0':
            logger.info("放回提还任务成功")
        else:
            raise AssertionError("放回提还任务失败——" + statusDesc)


    # 提前还款申请审批通过
    # prepay_id: 提前还款申请id
    def prepay_apply_aduit_pass(self,prepay_id,is_claim,lambda_role,real_prepay_total_amt=None,acc_entry_date=None,prepay_order="FX-GLF-LX-BJ"):

        task_id = self._get_prepay_task_id(prepay_id)

        #领取任务
        if is_claim == 'Y' or is_claim == 'y':
            self._prepay_task_claim(prepay_id)

        #审核
        url = '%s/repayment/prepay/audit/pass' % self._lambda_url

        if lambda_role == 'lambda_fund_clearing_post' or lambda_role == 'lambda_financial_review_audit':
            payload = {
                "id": prepay_id,
                "taskId": task_id,
                "realPrepayTotalAmt":real_prepay_total_amt,
                "realReceivedTime": acc_entry_date,
                "prepayOrder": prepay_order,
                "opinion": "",
                "version": "0",
                "useDepositAmt": "0"
            }

        else:
            payload = {
                "id":prepay_id,
                "taskId":task_id
            }
        res = self._request.post(url, headers=self._headers, data=json.dumps(payload))
        response = res.content.decode()
        status = json.loads(response).get("statusCode")
        statusDesc = json.loads(response).get("statusDesc")
        if status == '0':
            logger.info("提还申请通过" )
        else:
            logger.info(statusDesc)
            raise AssertionError(statusDesc)
    
    # 提前还款申请审批拒绝
    # prepay_id: 提前还款申请的id
    def prepay_apply_aduit_reject(self,prepay_id,is_claim):

        task_id = self._get_prepay_task_id(prepay_id)

        # 领取任务
        if is_claim == 'Y' or is_claim == 'y':
            self._prepay_task_claim(prepay_id)

        # 审核
        url = '%s/repayment/prepay/audit/reject'  % self._lambda_url
        payload = {
            "id": prepay_id,
            "taskId": task_id
        }
        res = self._request.post(url, headers=self._headers, data=json.dumps(payload))
        response = res.content.decode()
        status = json.loads(response).get("statusCode")
        statusDesc = json.loads(response).get("statusDesc")
        if status == '0':
            logger.info("提还申请拒绝—"  )
        else:
            logger.info(statusDesc)
            raise AssertionError(statusDesc)

        
    # 提前还款申请审批回退
    # prepay_id: 提前还款申请的id
    # back_role:回退节点
    def prepay_apply_aduit_back(self,prepay_id,is_claim):

        task_id = self._get_prepay_task_id(prepay_id)

        # 领取任务
        if is_claim == 'Y' or is_claim == 'y':
            self._prepay_task_claim(prepay_id)

        # 审核
        url = '%s/repayment/prepay/audit/back'  % self._lambda_url
        payload = {
            "id":prepay_id,
            "taskId" : task_id
        }
        res = self._request.post(url,headers=self._headers,data=json.dumps(payload))
        response = res.content.decode()
        status = json.loads(response).get("statusCode")
        statusDesc = json.loads(response).get("statusDesc")
        if status == '0':
            logger.info("提还申请已打回至投资经理")
        else:
            logger.info(statusDesc)
            raise AssertionError(statusDesc)

    # 提前还款申请审批撤销
    # prepay_id: 提前还款申请的id
    def prepay_apply_aduit_cancel(self,prepay_id):
        url = '%s/repayment/prepay/apply/cancel' %self._lambda_url
        payload = {
            "id":prepay_id
        }
        res = self._request.post(url,headers=self._headers,data=json.dumps(payload))
        response = res.content.decode()
        status = json.loads(response).get("statusCode")
        statusDesc = json.loads(response).get("statusDesc")
        if status == '0':
            logger.info("提还申请已撤销")
        else:
            logger.info(statusDesc)
            raise AssertionError(statusDesc)



"""



    #申请审批流程
    def prepay_approval_workflow(self,lend_code, acc_entry_date, prepayment_type="TQJQ", prepayment_capital=0,\
                                exemptCapitalAmt=0, exemptInterestAmt=0, exemptLateFeeAmt=0, exemptMngtAmt=0):

        prepay_id = self.create_prepay_apply(lend_code)

        # 提前还款申请：
        self.login_lambda(role='lambda_invest_manager')
        prepay_info = self.submit_prepay_apply(lend_code,acc_entry_date,prepayment_type, prepayment_capital,\
                                exemptCapitalAmt, exemptInterestAmt, exemptLateFeeAmt, exemptMngtAmt)


        #投资总监审批：
        self.login_lambda(role='lambda_invest_major')
        self.prepay_apply_aduit_pass(prepay_id, "Y")

        #投发部负责人审批：
        self.login_lambda(role='lambda_invest_develop')
        self.prepay_apply_aduit_pass(prepay_id, "Y")


        #减免利息、减免管理费
        if exemptInterestAmt > 0 or exemptMngtAmt > 0:
            self.login_lambda(role='lambda_financial_clearing_director')
            self.prepay_apply_aduit_pass(prepay_id, "Y")
            self.login_lambda(role='lambda_chief_financial_officer')
            self.prepay_apply_aduit_pass(prepay_id, "Y")

        #减免违约金
        if exemptLateFeeAmt > 0:
            self.login_lambda(role='lambda_management_after_loan_major')
            self.prepay_apply_aduit_pass(prepay_id, "Y",prepay_info[0],prepay_info[1])
            self.login_lambda(role='lambda_risk_management')
            self.prepay_apply_aduit_pass(prepay_id, "Y")

        #资金清算岗
        self.login_lambda(role='lambda_fund_clearing_post')
        self.prepay_apply_aduit_pass(prepay_id, "Y",'lambda_fund_clearing_post',prepay_info[0],prepay_info[1])
        #财务复核岗
        self.login_lambda(role='lambda_financial_review_audit')
        self.prepay_apply_aduit_pass(prepay_id, "Y", 'lambda_financial_review_audit', prepay_info[0], prepay_info[1])





"""
    #提还没有业务回收
    #def prepay_apply_aduit_retreat(self,prepay_id):
        #pass
    