 # -*- coding:utf-8 -*-
import json
from robot.api import logger
import datetime
from datetime import date



class _LambdaRepaymentKeywords():
    
    def __init__(self):
        pass

    # 新增还款申请
    # lend_code:借据号IOU2017112300002
    # issue:期数
    def _create_repayment_apply(self, lend_code, custId, custKind):
         url = '%s/repayment/apply/create' % self._lambda_url
         param = {
             "lend_code": lend_code,
             "custId": custId,
             "custKind" : custKind
         }
         res = self._request.post(url, headers=self._headers, data=json.dumps(param))
         response = res.content.decode('utf-8')
         # 把服务器返回的内容转换为python的字典
         reply_json_dict = json.loads(response)
         # 通过字典获取状态码
         statusCode = reply_json_dict['statusCode']
         statusDesc = reply_json_dict['statusDesc']

         if statusCode == '0':
             id = reply_json_dict['data']['id']
             return id
         else:
             logger.info(statusDesc)
             raise AssertionError('新增还款失败,错误码:%s,错误信息:%s' %  (reply_json_dict.get('statusCode'), reply_json_dict.get('statusDesc')))


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

    def _repay_detail(self, prepay_id):

        '''
                     获取提还申请详细信息
                     :param prepay_id:提还id
                     :return:custId:客户id
                     :return:prepayAmt:提还金额
        '''

        url = '%s/repayment/prepay/apply/view' % self._lambda_url
        params = {"prepayApplyId": prepay_id}
        res = self._request.get(url, params=params, headers=self._headers)
        response = json.loads(res.content.decode())
        if response.get("statusCode")=='0':
            logger.info("提还申请详情页面查询成功")
            return response.get("data").get("custId"),response.get("data").get("prepayAmt")
        else:
            raise AssertionError("提还申请详情页面查询失败——"+json.loads(response).get("stautsDesc"))


    #新建提还申请，用于判断借据是否满足可提还
    def _create_prepay_apply(self,lend_code):

        '''
                  新建提还申请
                  :param lend_code:借据号
                  :return:prepay_id:提还id

        '''

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
    def _dueQuery(self,prepayment_type,acc_entry_date,lend_code,prepay_id,prepayment_capital):

        '''
                财务查询
                :param prepayment_type:提还类型
                :param acc_entry_date:提还日期
                :param lend_code:借据号
                :param prepay_id:提还id
                :param prepayment_capital:提还金额
                :return:residueCapital:剩余本金
                :return:dueInterest:应还利息
                :return:dueMngtCharge:应还管理费
                :return:dueFree:应还违约金
                :return:iou_info[1]:提还本金

        '''

        iou_info = self._repay_detail(prepay_id)
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

        '''
                提交提还申请
                :param lend_code:借据
                :param acc_entry_date:提前还款日期
                :param prepayment_type:提还类型
                :param prepayment_capital:提还本金（部分提还时传入）
                :param exemptCapitalAmt:减免本金
                :param exemptInterestAmt:减免利息
                :param exemptLateFeeAmt:减免违约金
                :param exemptMngtAmt:减免管理费
                :return:prepay_id:提还id
                :return:prepayTotalAmt:提还总金额

        '''

        url = '%s/repayment/prepay/apply/submit' % self._lambda_url
        prepay_id = self._create_prepay_apply(lend_code)
        due_info = self._dueQuery(prepayment_type,acc_entry_date,lend_code,prepay_id, prepayment_capital)
        realCapitalAmt = due_info[1] - exemptCapitalAmt
        realInterestAmt = due_info[2] - exemptInterestAmt
        realMngtAmt = due_info[3] - exemptMngtAmt
        realLateFeeAmt = due_info[4] - exemptLateFeeAmt
        prepayTotalAmt = realCapitalAmt + realInterestAmt + realMngtAmt + realLateFeeAmt

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
                return prepay_id,prepayTotalAmt
            else:
                logger.info(statusDesc)
                raise AssertionError(statusDesc)



    #提还审批

    def _get_prepay_task_list(self,page_no=1,page_size=100):

        '''
                       领取任务
                       :param page_no:第几页
                       :param page_size:每页数量
                       :return:list:提还任务列表
        '''

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

        '''
                    领取任务
                    :param prepay_id:提还id
                    :return:taskId:任务id
         '''

        prepay_task_list = self._get_prepay_task_list()
        for prepay_task in prepay_task_list:
            if str(prepay_task.get("id")) == str(prepay_id):
                prepay_task_id = prepay_task.get("taskId")
                break
        else:
            raise AssertionError("提还任务列表中找不到对应的提还id，提还id:%s" % prepay_id)
        return prepay_task_id


    def _prepay_task_claim(self,prepay_id):

        '''
                领取任务
                :param prepay_id:提还id
                :return:
        '''

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

    def prepay_apply_aduit_pass(self,prepay_id,is_claim,lambda_role=None,real_prepay_total_amt=None,acc_entry_date=None,prepay_order="FX-GLF-LX-BJ"):

        '''
               审批通过
               :param prepay_id: 提前还款申请id
               :param is_claim: 是否领取任务,Y:领取
               :param lambda_role: 审批人
               :param real_prepay_total_amt: 提前还款申请id
               :param acc_entry_date: 实际还到账日期
               :param prepay_order: 还款顺序

               '''

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
            logger.info("提还申请通过——审核人：%s" %lambda_role )
        else:
            logger.info(statusDesc)
            raise AssertionError(statusDesc+"——审核人：%s" %lambda_role)
    
    # 提前还款申请审批拒绝
    # prepay_id: 提前还款申请的id
    def prepay_apply_aduit_reject(self,prepay_id,is_claim,lambda_role=None,real_prepay_total_amt=None,acc_entry_date=None,prepay_order="FX-GLF-LX-BJ"):

        task_id = self._get_prepay_task_id(prepay_id)

        # 领取任务
        if is_claim == 'Y' or is_claim == 'y':
            self._prepay_task_claim(prepay_id)

        # 审核
        url = '%s/repayment/prepay/audit/reject'  % self._lambda_url
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
            logger.info("提还申请拒绝——审核人：%s" %lambda_role )
        else:
            logger.info(statusDesc+"——审核人：%s" %lambda_role)
            raise AssertionError(statusDesc)

        
    # 提前还款申请审批回退
    # prepay_id: 提前还款申请的id
    # back_role:回退节点
    def prepay_apply_aduit_back(self,prepay_id,is_claim,lambda_role=None,real_prepay_total_amt=None,acc_entry_date=None,prepay_order="FX-GLF-LX-BJ"):

        task_id = self._get_prepay_task_id(prepay_id)

        # 领取任务
        if is_claim == 'Y' or is_claim == 'y':
            self._prepay_task_claim(prepay_id)

        # 审核
        url = '%s/repayment/prepay/audit/back'  % self._lambda_url
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
        res = self._request.post(url,headers=self._headers,data=json.dumps(payload))
        response = res.content.decode()
        status = json.loads(response).get("statusCode")
        statusDesc = json.loads(response).get("statusDesc")
        if status == '0':
            logger.info("提还申请已打回——审核人：%s" %lambda_role)
        else:
            logger.info(statusDesc)
            raise AssertionError(statusDesc+"——审核人：%s" %lambda_role)

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


    #申请审批流程
    #若部分提还，prepayment_capital传值，否则用默认
    def prepay_approval_workflow(self,lend_code, acc_entry_date, prepayment_type="TQJQ", prepayment_capital=0,\
                                exemptCapitalAmt=0, exemptInterestAmt=0, exemptLateFeeAmt=0, exemptMngtAmt=0):

        '''
                    提交提还申请
                    :param lend_code:借据
                    :param acc_entry_date:提前还款日期
                    :param prepayment_type:提还类型
                    :param prepayment_capital:提还本金（部分提还时传入）
                    :param exemptCapitalAmt:减免本金
                    :param exemptInterestAmt:减免利息
                    :param exemptLateFeeAmt:减免违约金
                    :param exemptMngtAmt:减免管理费

        '''


        # 提前还款申请：
        #prepay_info[0]: 提还id
        #prepay_info[1]: 提还总金额
        self.login_lambda(role='lambda_invest_manager')
        prepay_info = self.submit_prepay_apply(lend_code,acc_entry_date,prepayment_type, prepayment_capital,\
                                exemptCapitalAmt, exemptInterestAmt, exemptLateFeeAmt, exemptMngtAmt)


        #投资总监审批
        self.login_lambda(role='lambda_invest_major')
        self.prepay_apply_aduit_pass(prepay_info[0], "Y",'lambda_invest_major')

        #投发部负责人审批
        self.login_lambda(role='lambda_invest_develop')
        self.prepay_apply_aduit_pass(prepay_info[0], "Y",'lambda_invest_develop')


        #减免利息、减免管理费
        if exemptInterestAmt > 0 or exemptMngtAmt > 0:
            self.login_lambda(role='lambda_financial_clearing_director')
            self.prepay_apply_aduit_pass(prepay_info[0], "Y",'lambda_financial_clearing_director')
            self.login_lambda(role='lambda_chief_financial_officer')
            self.prepay_apply_aduit_pass(prepay_info[0], "Y",'lambda_chief_financial_officer')


        #减免违约金
        if exemptLateFeeAmt > 0:
            self.login_lambda(role='lambda_management_after_loan_major')
            self.prepay_apply_aduit_pass(prepay_info[0], "Y",'lambda_management_after_loan_major')
            self.login_lambda(role='lambda_risk_management')
            self.prepay_apply_aduit_pass(prepay_info[0], "Y",'lambda_risk_management')


        #资金清算岗
        self.login_lambda(role='lambda_fund_clearing_post')
            #实际到账日至少比提还日期提前一天
        acc_entry_date = datetime.datetime.strptime(acc_entry_date, '%Y/%m/%d') - datetime.timedelta(days=1)
        acc_entry_date = acc_entry_date.strftime('%Y/%m/%d')
        #print(acc_entry_date)
        self.prepay_apply_aduit_pass(prepay_info[0], "Y",'lambda_fund_clearing_post',prepay_info[1],acc_entry_date)
        #财务复核岗
        self.login_lambda(role='lambda_financial_review_audit')
        self.prepay_apply_aduit_pass(prepay_info[0], "Y", 'lambda_financial_review_audit', prepay_info[1],acc_entry_date)




    