 # -*- coding:utf-8 -*-
import json
from robot.api import logger
from faker.factory import Factory
myfaker = Factory.create('zh_CN')

text = myfaker.text() #随机生成一段文本
class _LambdaWithdrawalKeywords():
    
    def __init__(self):

        pass

    def withdrawal_get_custid(self,custname,custtype):
        """
        【功能】：获取客户id

        【参数】：

        custname: 客户名称

        custtype: 客户类型——GR/QY

        【返回值】：返回客户id
        """
        #通过custname和custtype获取custid
        if custtype == 'GR':
            url = "%s/cust/infos/personal/list" % self._lambda_url
        if custtype == 'QY':
            url = "%s/cust/infos/enterprise/list" % self._lambda_url

        params = {"custNamey":custname}
        res = self._request.get(url,params=params)
        response = res.content.decode()
        for i in json.loads(response).get('list'):
            baseInfo = i.get('baseInfo')
            name = baseInfo['custName']
            if name == custname:
                return baseInfo.get('id')
        else:
            raise Exception("系统中不存在客户名为 %s 的 %s 客户" %(custname,custtype))

    def _get_contract(self,custid):
        #通过custid获取客户已签订的合同列表
        url = "%s/withdrawal/apply/listContract" % self._lambda_url
        params = {"custId":custid}
        res = self._request.get(url,params = params)
        response = res.content.decode()
        list_contract = json.loads(response).get('list')
        return list_contract

    # 新建提款申请
    # custname:借款客户姓名
    # custtype:客户类型——GR,QY
    # 返回 withdrawal_id 后续其他接口会用到
    def create_withdrawal_apply(self, custname, custtype):
        """
        【功能】：新建提款申请

        【参数】：

        custname: 客户名称

        custtype: 客户类型——GR/QY

        【返回值】：

        返回提款明细id 和custid
        """

        url = "%s/withdrawal/apply/create" % self._lambda_url
        custId = self.withdrawal_get_custid(custname, custtype)
        list_contracts = self._get_contract(custId)

        for lst in list_contracts:
            contractId = lst.get('id')
            contractNo = lst.get('contractNo')
            data = {
                "contractId": contractId,
                "custId": custId
            }
            res = self._request.post(url, data=data)  # webforms格式的参数
            # r = json.loads(res.content.decode())
            status = json.loads(res.content.decode()).get('statusCode')
            if status == '0':
                withdrawal_detailId = json.loads(res.content.decode()).get('data')
                logger.info("对%s新建提款成功，提还明细id为:%s" % (contractNo, withdrawal_detailId))
                # 返回提款详情id和custid
                return withdrawal_detailId, custId
            else:
                statusDesc = json.loads(res.content.decode()).get('statusDesc')
                raise Exception("对%s新建提款失败%s" % (contractNo, statusDesc))

    def withdrawal_apply_view(self,apply_detailId):
        """
        【功能】：获取提款明细的详细信息

        【参数】：

        apply_detailId:提款明细id

        【返回值】：

        返回提款详细信息details和提款编号biz
        """
        #新建提款成功后，获取提款详细信息，参数为提款详情id
        #apply_detailId,custId = apply_create(custname,custtype,contractno) #获取提款明细id和custid
        url = "%s/withdrawal/apply/view" % self._lambda_url
        params = {
            "id":apply_detailId
            }
        res = self._request.get(url,params=params)  #webforms格式的参数
        #r = json.loads(res.content.decode())
        status = json.loads(res.content.decode()).get('statusCode')
        if status =='0':
            details = json.loads(res.content.decode()).get('data').get('audit')
            bizCode=json.loads(res.content.decode()).get('data').get('withdrawalCode')#提款编号withdrawalCode=DRA2017121400001
            return details,bizCode

    def get_delegate_bank(self,withdrawalId,custId=None):
        """
        【功能】：获取提款对应的第三方银行卡列表（过滤掉信息不完善的银行卡）

        【参数】：
         withdrawalId: 提款申请id

         custId: 客户id，默认为空

        【返回值】：返回可用的银行列表
        """
        #获取提款对应的第三方银行卡列表
        url = "%s/withdrawal/delegate/bank/list" % self._lambda_url
        params = {
            "withdrawalApplyId":withdrawalId,
            "custId":custId
            }
        res = self._request.get(url,params = params)
        response = res.content.decode()     
        r =  json.loads(response).get('data') #客户银行列表
        banklist = []
        for i in r:

            if i.get("isCorporateAccount")==False and i.get("bankNumber") != "" and i.get("preIdno") !="":
                #如果是对私账户，需要行号和证件号码不为空
                banklist.append(i)
            if i.get("isCorporateAccount")==True and i.get("bankNumber") != "":
                #如果是对公账户，需要行号不为空
                banklist.append(i)
        return(banklist)

    def create_delegate_bank(self,withdrawalId,custId=None):
        """
        【功能】：创建跟提款关联的第三方银行卡并返回可用的银行卡列表（过滤掉信息不完善的银行卡）

        【参数】：

        withdrawalId:提款申请id

        custId:客户id，默认为空

        【返回值】：无
        """

        url = "%s/withdrawal/delegate/bank/create" % self._lambda_url
        data ={
                "accountName": 'test_new',
                "cardNo": '384750923840293',  # 银行帐号
                "preIdno": '394758092384302955',  # 身份证号码
                "prePhone": "18600000001",  # 银行预留手机号
                "bankCode": '402584009991',
                "bankId": '36',
                "bankName": '深圳农村商业银行',
                "isCorporateAccount": "false",
                "bankDeposit": '深圳龙岗鼎业村镇银行龙华支行',  # 支行
                "bankNumber": '320584000031',  # 行号
                "withdrawalApplyId": withdrawalId,
                "custId": custId,
                "preIdtype": 'GR_SFZ'   # =GR_SFZ
                }
        res = self._request.post(url, headers=self._headers, data=json.dumps(data))
        # response = res.content.decode()
        status = json.loads(res.content.decode()).get('statusCode')
        if status == '0':
            pass
        else:
            statusDesc = json.loads(res.content.decode()).get('statusDesc')
            raise Exception('新增第三方银行卡失败:%s' % statusDesc)
            return

    def get_withdrawal_account(self, withdrawalId):

        """
        【功能】：获取提款对应的支付对象列表数据

        【参数】：

        withdrawalId:提款申请id

        【返回值】：返回提款的支付对象列表数据
        """

        url = "%s/withdrawal/pay/account/list" % self._lambda_url
        params = {
            "id": withdrawalId
            }
        res = self._request.get(url, params=params)  # webforms格式的参数
        status = json.loads(res.content.decode()).get('statusCode')
        if status == '0':
            account_list = json.loads(res.content.decode()).get('data')  # 获取提款的所有支付对象
            return account_list
        else:
            statusDesc = json.loads(res.content.decode()).get('statusDesc')
            raise Exception('获取提款对应的支付对象列表数据失败：%s' %statusDesc)

    def get_custBank(self,custId):
        """
        【功能】：获取客户银行卡列表数据，<接口应该放在客户模块>

        【参数】：客户id

        【返回值】：返回可用的银行卡列表（过滤掉信息不完善的银行卡）
        """
        url = "%s/cust/bank/accounts/list" % self._lambda_url
        """
        params = {"accountype":accountype,
                "custId":custId   
                }
        """
        params = {
                "custId": custId   
                 }  
        res = self._request.get(url,params=params)
        response = res.content.decode()     
        r =  json.loads(response).get('data') #客户银行列表
        banklist = []
        for i in r:

            if i.get("isCorporateAccount")==False and i.get("bankNumber") != "" and i.get("preIdno") !="":
                #如果是对私账户，需要行号和证件号码不为空
                banklist.append(i)
            if i.get("isCorporateAccount")==True and i.get("bankNumber") != "":
                #如果是对公账户，需要行号不为空
                banklist.append(i)

        return(banklist)

    # 新建支付对象
    def add_withdrawal_account(self,details,custId,payName=None,payType=None,payAmt=1000,Duration=None):
        """
        【功能】：为提款新建支付对象

        【参数】：
        payName:支付对象名称，默认为空

        payType:支付对象的客户类型——GR,QY，默认为空

        payAmt：支付金额，默认为1000

        Duration：期限，如果为空，则默认一次付清为120天，其他还款方式为4个月

        【返回值】：返回新添加的支付对象的支付金额
        """
        # 提款申请支付对象提交
        withdrawalId = details['withdrawalId']
        if details['loanPaymentMode'] == 'ZZZF':
            # 如果是自主支付，直接获取客户银行卡列表
            banklist = self.get_custBank(custId)  # 获取客户银行卡列表，接口从客户模块来（待联调）
            # banklist = [{'accountName': '方圆久', 'bankDeposit': '中国工商银行深圳市分行', 'bankName': '中国工商银行', 'cardNo': '3111182159021202', 'preIdtype': 'GR_SFZ', 'omegaId': '', 'updateBy': 'wlh_投资经理1', 'custId': 31, 'id': 32, 'bankNumber': '102584000002', 'bankCode': '102100099996', 'showEdit': True, 'accountNamePy': 'fang,yuan,jiu', 'otherBankName': '', 'updateTime': 1510654948000, 'preIdno': '922825772275372829', 'custName': '方圆', 'omegaTab': '', 'updateById': 2, 'prePhone': '18600000001', 'isCorporateAccount': False, 'bankId': 2, 'createBy': 'wlh_投资经理1', 'createTime': 1510654949000, 'fatorVerify': False, 'withdrawalApplyId': '', 'bankNameAbb': 'ICBC', 'createById': 2}]
            if len(banklist) == 0:
                self.create_custBank(custId) # 自主支付，如果客户银行卡列表为空，则新建银行卡（新建银行卡接口从客户模块来，待联调）
        else:
            if payName is not None:
                if payType == 'GR' or payType == 'QY':
                    custId = self.withdrawal_get_custid(payName,payType)
                    banklist = self.get_delegate_bank(withdrawalId, custId)  # 获取跟提款关联的第三方银行卡列表
                    if len(banklist) == 0:  # 如果第三方银行卡列表为空则新建一张银行卡再重新获取列表
                        self.create_delegate_bank(withdrawalId, custId)
                        banklist = self.get_delegate_bank(withdrawalId, custId)
                else:
                    raise Exception("支付对象payName值不为空，请设置payType参数的值：GR或者QY")
            else:
                banklist = self.get_delegate_bank(withdrawalId)  # 获取跟提款关联的第三方银行卡列表
                if len(banklist) == 0:  # 如果第三方银行卡列表为空则新建一张银行卡再重新获取列表
                    self.create_delegate_bank(withdrawalId)
                    banklist = self.get_delegate_bank(withdrawalId)
        bankid = banklist[0].get('id')
        custName = banklist[0].get('custName')
        if custName == '':
            custName = banklist[0].get('accountName')
        if Duration is None:
            if details['repaymentType'] =="YCFQ":
                Duration = '120'#如果还款方式为一次性还本付息，则期限为120 天
            else:
                Duration = '4'#其他还款方式，期限为4 月

        url = "%s/withdrawal/pay/account/save" % self._lambda_url
        data ={
                "bankId":bankid,
                "custId":custId,#支付对象的custId
                "custName":custName,#支付对象的名字
                "loanDuration":Duration,#期限
                "payAmt":payAmt,#支付金额
                "withdrawalId":withdrawalId
                }
        res = self._request.post(url,data=json.dumps(data),headers=self._headers)
        status = json.loads(res.content.decode()).get('statusCode')
        if status == '0':
            logger.info('新增支付对象成功')
            return data.get("payAmt")#返回支付对象金额
        else:
            statusDesc = json.loads(res.content.decode()).get('statusDesc')
            #print('新增支付对象失败：%s' %statusDesc)
            raise Exception('新增支付对象失败：%s' %statusDesc)
        
    # 保存提款申请
    # withdrawal_id 提款申请的id
    def save_withdrawal_apply(self,detailId,Amt,**kwargs):
        """
        【功能】：保存提款详情

        【参数】：
        **kwargs
        detainPeriod #预扣利息期数,默认0
        adInPayType：预扣利息缴交方式(可填值为FKQ,KCYE)，默认FKQ
        adMgntPayType：预扣管理费缴交方式(可填值为FKQ,KCYE)，默认FKQ
        serPayType：服务费缴交方式(可填值为FKQ,KCYE)，默认FKQ
        depPayType：保证金缴交方式(可填值为FKQ,KCYE)，默认KCYE
        repayType：还款方式,默认XXHB
        chargeOffAct：合同性质(可填值为NJQ,CFNC),默认为CFNC
        depActStatus：保证金到账状态,默认TRUE
        mgtActStatus：管理费到账状态,默认TRUE
        serActStatus：服务费到账状态,默认TRUE
        wInActStatus：预扣利息到账状态,默认TRUE

        【返回值】：无
        """
        #保存提款详情
        #detainPeriod = 0, adInPayType = 'FKQ', adMgnPayType = 'FKQ',
        #SerPayType = 'FKQ', depPayType = 'KCYE', repayType = 'XXHB', chargeOffAct = 'CFNC'
        details = self.withdrawal_apply_view(detailId)[0]
        borrowYearRate = details['borrowYearRate']
        detainPeriod = kwargs.get('detainPeriod',details['detainPeriod'])#预扣利息期数
        adInPayType = kwargs.get('adInPayType','FKQ')#预扣利息缴交方式
        adMgntPayType = kwargs.get('adMgntPayType','FKQ')#预扣管理费缴交方式
        serPayType = kwargs.get('serPayType','FKQ')#服务费缴交方式
        depPayType = kwargs.get('depPayType','KCYE')#保证金缴交方式
        repayType = kwargs.get('repayType',details['repaymentType'])#还款方式
        chargeOffAct = kwargs.get('chargeOffAct','CFNC')#合同性质
        depActStatus = kwargs.get('depActStatus','TRUE')#保证金到账状态
        mgtActStatus = kwargs.get('mgtActStatus','TRUE')#管理费到账状态
        serActStatus = kwargs.get('serActStatus','TRUE')#服务费到账状态
        wInActStatus = kwargs.get('wInActStatus','TRUE')#预扣利息到账状态
        url = "%s/withdrawal/apply/save" % self._lambda_url
        data = {
                "id": detailId,#提款详情id
                "detainPeriod":detainPeriod, #预扣利息期数
                "advanceInterestPaymentType":adInPayType,#预扣利息缴交方式
                "advanceBizMgntPaymentType":adMgntPayType,#预扣管理费缴交方式
                "bizServicePaymentType":serPayType,#服务费缴交方式
                "depositPaymentType":depPayType,#保证金缴交方式
                "repaymentType":repayType,#还款方式
                "chargeOffAct":chargeOffAct,#合同性质
                "depositToActStatus":depActStatus,#保证金到账状态
                "mngtToActStatus":mgtActStatus,#管理费到账状态
                "serviceToActStatus":serActStatus,#服务费到账状态
                "whInterestToActStatus":wInActStatus,#预扣利息到账状态
                "borrowYearRate":borrowYearRate,
                "withdrawalAmt":Amt #提款金额
            }
        res = self._request.post(url,data=json.dumps(data),headers=self._headers)
        status = json.loads(res.content.decode()).get('statusCode')
        if status == '0':
            logger.info('保存提款详情成功')
        else:
            statusDesc = json.loads(res.content.decode()).get('statusDesc')
            #print('保存提款详情失败:%s' %statusDesc)
            raise Exception('保存提款详情失败:%s' %statusDesc)
            #return

    
    def submit_withdrawal_apply(self, withdrawalId):
        """
        【功能】：提交提款申请

        【参数】：
        withdrawalId: 提款申请id

        【返回值】：无
        """
        # 提交提款申请
        url = "%s/withdrawal/apply/submit" % self._lambda_url
        data = {
                "withdrawalApplyId":withdrawalId
            }
        res = self._request.post(url,data=json.dumps(data),headers=self._headers)
        status = json.loads(res.content.decode()).get('statusCode')
        if status == '0':
            logger.info('提交提款成功：%s' %withdrawalId)
        else:
            statusDesc = json.loads(res.content.decode()).get('statusDesc')
            #print('提交提款失败:%s' %statusDesc)
            raise Exception('提交提款失败:%s' %statusDesc)
    
        
    def get_withdrawal_taskId(self,bizCode):
        """
        【功能】：获取提款申请的任务id

        【参数】：

        bizCode: 提款编号

        【返回值】：返回提款任务id
        """
        #通过业务编号获取taskId
        url = "%s/workbench/withdrawalApply/todoList" % self._lambda_url
        data =   {
                    "pageSize":100
                    }
        res = self._request.post(url,data=json.dumps(data),headers=self._headers) #json格式的参数传递
        #r = json.loads(res.content.decode())
        #print(r)
        
        status = json.loads(res.content.decode()).get('statusCode')
        if status =='0':
            lst = json.loads(res.content.decode()).get('list')
            for i in lst:
                code = i['bizCode']
                if code == bizCode:
                    return i.get('taskId'),i.get('id')  #返回taskId和提款明细id
            else:
                raise Exception("此用户名下不存在任务编码为%s的提款任务" %bizCode)
                """
                for key,value in i.items():
                    if key == 'bizCode' and value == bizCode:
                        return i.get('taskId'),i.get('id')  #返回taskId和withdrawal_detailId
                """
        else:
            statusDesc = json.loads(res.content.decode()).get('statusDesc')
            #print('获取taskId失败:%s' %statusDesc)
            raise Exception('获取taskId失败:%s' %statusDesc)

    
    def receive_withdrawal_task(self,taskId):
        """
        【功能】：领取提款任务

        【参数】：

        taskId:任务id

        【返回值】：无
        """
        url = "%s/workbench/withdrawalApply/claim" % self._lambda_url
        
        data = {
                "taskId":taskId
            }
        res = self._request.post(url,data=data)  #webforms格式的参数
        #r = json.loads(res.content.decode())
        status = json.loads(res.content.decode()).get('statusCode')
        if status =='0':
            logger.info("领取任务成功")
        else:
            statusDesc = json.loads(res.content.decode()).get('statusDesc')
            #print("领取任务失败：%s" %statusDesc)
            raise Exception("领取任务失败：%s" %statusDesc)


    #保存审核意见
    def save_withdrawal_advice(self,taskId,withdrawalId,detailId):
        """
        【功能】：保存提款审核意见

        【参数】：

        taskId:任务id

        withdrawalId:提款申请id

        detailId:提款明细id

        【返回值】：无
        """
        url = "%s/withdrawal/save" % self._lambda_url
        data = {
            "withdrawalId":withdrawalId,
            "id":detailId,
            "taskId":taskId,
            "auditAdvice":text
            }
        res = self._request.post(url,data=json.dumps(data),headers = self._headers)  
        #r = json.loads(res.content.decode())
        status = json.loads(res.content.decode()).get('statusCode')
        if status =='0':
            logger.info("保存审核意见成功")
        else:
            statusDesc = json.loads(res.content.decode()).get('statusDesc')
            #print("保存审核意见失败：%s" %statusDesc)
            raise Exception("保存审核意见失败：%s" %statusDesc)

    # 提款申请审批通过
    # withdrawal_id: 提款申请id
    def withdrawal_apply_pass(self,taskId,withdrawal_id):
        """
        【功能】：提款审批通过

        【参数】：

        taskId:提款任务id

        withdrawal_id:提款申请id

        【返回值】：无
        """
        url = "%s/withdrawal/apply/pass" % self._lambda_url
        data = {
            "taskId":taskId,
            "withdrawalApplyId":withdrawal_id
            }
        res = self._request.post(url,data=json.dumps(data),headers = self._headers)  
        status = json.loads(res.content.decode()).get('statusCode')
        if status =='0':
            logger.info("审批通过")
        else:
            statusDesc = json.loads(res.content.decode()).get('statusDesc')
            raise Exception("审批通过报错：%s" %statusDesc)
        
    def get_withdrawal_iou(self,withdrawalId):
        """
        【功能】：获取提款申请借据拆分中的借据列表

        【参数】：

        withdrawalId: 提款申请id

        【返回值】：返回剩余可拆分金额和借据列表
        """

        url = "%s/iou/list" % self._lambda_url
        params = {
            "withdrawalId":withdrawalId
            }
        res = self._request.get(url,params=params)  #webforms格式的参数
        status = json.loads(res.content.decode()).get('statusCode')
        if status == '0':
            iou_list = json.loads(res.content.decode()).get('list')
            totalAmt = json.loads(res.content.decode()).get('totalAmt') #剩余可拆分金额
            return totalAmt,iou_list
        else:
            statusDesc = json.loads(res.content.decode()).get('statusDesc')
            raise Exception("获取提款的借据列表失败：%s" % statusDesc)
    def create_withdrawal_iou(self,iouAmt,loanDuration,withdrawalId):
        """
        【功能】：拆分借据

        【参数】：

        iouAmt:借据金额

        loanDuration:借据期限

        payAccountId:支付对象的id，从支付对象列表中选

        withdrawalId:对应的提款申请Id

        【返回值】：返回剩余可拆分金额
        """
        ids = []
        account_list = self.get_withdrawal_account(withdrawalId)
        for i in account_list:
            ids.append(i['id'])
        url = "%s/iou/create" % self._lambda_url
        data = {
            "iouAmt": iouAmt,
            "loanDuration":loanDuration ,
            "payeeId":'',
            "payeeAct":'',
            "payAccountId": ids[0],
            "withdrawalId": withdrawalId,
        }
        res = self._request.post(url, data=data)  # webforms格式的参数
        # r = json.loads(res.content.decode())
        status = json.loads(res.content.decode()).get('statusCode')
        if status =='0':
            left_amt = json.loads(res.content.decode()).get('data') #借据拆分后，返回剩余可拆分金额
            return left_amt
        else:
            statusDesc = json.loads(res.content.decode()).get('statusDesc')
            raise Exception("拆分借据失败：%s" % statusDesc)
    def del_withdrawal_iou(self):
        #删除借据
        #/ iou / delete
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