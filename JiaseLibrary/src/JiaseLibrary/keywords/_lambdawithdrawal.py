 # -*- coding:utf-8 -*-
import json
from robot.api import logger

class _LambdaWithdrawalKeywords():
    
    def __init__(self):        
        pass

    def _get_custid(self,custname,custtype):
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
            for key,value in baseInfo.items():
                # print(key,value)
                if key == 'custName' and value == custname :
                    return baseInfo.get('id')

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
        # 新建提款
        url = "%s/withdrawal/apply/create" % self._lambda_url
        custId = self._get_custid(custname, custtype)
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
                logger.info("对%s新建提款失败%s" % (contractNo, statusDesc))

    def withdrawal_apply_view(self,apply_detailId):
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
            return details

    def _delegate_bank(self,withdrawalApplyId):
        #获取提款对应的第三方银行卡列表
        url = "%s/withdrawal/delegate/bank/list" % self._lambda_url
        params = {
            "withdrawalApplyId":withdrawalApplyId
            }
        res = s.get(url,params = params)
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

    def _create_deBank(self,withdrawalApplyId):
        #创建跟提款关联的第三方银行卡
        url = "%s/withdrawal/delegate/bank/create" % self._lambda_url
        data =      {
                "accountName":'test_new',
                "cardNo":'384750923840293',#银行帐号
                "preIdno":'394758092384302955',#身份证号码
                "prePhone":"18600000001",#银行预留手机号
                "bankCode":'402584009991',
                "bankId":'36',
                "bankName":'深圳农村商业银行',
                "isCorporateAccount":"false",
                "bankDeposit":'深圳龙岗鼎业村镇银行龙华支行',#支行
                "bankNumber":'320584000031',#行号
                "withdrawalApplyId":withdrawalApplyId,
                "preIdtype":'GR_SFZ'   #=GR_SFZ
                }
        res = s.post(url,headers=self._headers,data=json.dumps(data))
        response = res.content.decode()
        status = json.loads(res.content.decode()).get('statusCode')
        if status == '0':
            pass
        else:
            statusDesc = json.loads(res.content.decode()).get('statusDesc')
            logger.info('新增第三方银行卡失败:%s' %statusDesc)
            return

    def get_custBank(custId):
        url = 'http://%s/cust/bank/accounts/list' %host
        """
        params = {"accountype":accountype,
                "custId":custId   
                }
        """
        params = {
                "custId":custId   
                }  
        res = s.get(url,params=params)
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
    def create_withdrawal_apply_account(self,details,custId,payAmt=1000,Duration=None):
        #提款申请支付对象提交
        withdrawalId = details['withdrawalId']
        if details['loanPaymentMode'] == 'ZZZF':
            #如果是自主支付，直接获取客户银行卡列表
            banklist = self.get_custBank(custId)#调用account_agreement中的get_custBank方法   需要联调
            #banklist = [{'accountName': '方圆久', 'bankDeposit': '中国工商银行深圳市分行', 'bankName': '中国工商银行', 'cardNo': '3111182159021202', 'preIdtype': 'GR_SFZ', 'omegaId': '', 'updateBy': 'wlh_投资经理1', 'custId': 31, 'id': 32, 'bankNumber': '102584000002', 'bankCode': '102100099996', 'showEdit': True, 'accountNamePy': 'fang,yuan,jiu', 'otherBankName': '', 'updateTime': 1510654948000, 'preIdno': '922825772275372829', 'custName': '方圆', 'omegaTab': '', 'updateById': 2, 'prePhone': '18600000001', 'isCorporateAccount': False, 'bankId': 2, 'createBy': 'wlh_投资经理1', 'createTime': 1510654949000, 'fatorVerify': False, 'withdrawalApplyId': '', 'bankNameAbb': 'ICBC', 'createById': 2}]
            if len(banklist) ==0:
                self.create_custBank(custId)
        else:
            banklist = self._delegate_bank(withdrawalId)#获取跟提款关联的第三方银行卡列表
            if len(banklist) == 0:#如果第三方银行卡列表为空则新建一张银行卡再重新获取列表
                self._create_deBank(withdrawalId)
                banklist = self._delegate_bank(withdrawalId)
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
        data =   {
                "bankId":bankid,
                "custId":custId,
                "custName":custName,#支付对象
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
            logger.info('支付对象失败：%s' %statusDesc)
            return
        
    # 保存提款申请
    # withdrawal_id 提款申请的id
    def save_withdrawal_apply(self,detailId,Amt):
        #保存提款详情
        url = "%s/withdrawal/apply/save" % self._lambda_url
        data = {
                "id": detailId,#提款详情id
                "detainPeriod":'0', #预扣利息期数
                "advanceInterestPaymentType":'FKQ',#预扣利息缴交方式
                "advanceBizMgntPaymentType":'FKQ',#预扣管理费缴交方式
                "bizServicePaymentType":'FKQ',#服务费缴交方式
                "depositPaymentType":'KCYE',#保证金缴交方式
                "repaymentType":'XXHB',#还款方式
                "chargeOffAct":'CFNC',#合同性质
                "depositToActStatus":'TRUE',#保证金到账状态
                "mngtToActStatus":'TRUE',#管理费到账状态
                "serviceToActStatus":'TRUE',#服务费到账状态
                "whInterestToActStatus":'TRUE',#预扣利息到账状态
                "withdrawalAmt":Amt #提款金额
            }
        res = self._request.post(url,data=json.dumps(data),headers=self._headers)
        status = json.loads(res.content.decode()).get('statusCode')
        if status == '0':
            logger.info('保存提款详情成功')
        else:
            statusDesc = json.loads(res.content.decode()).get('statusDesc')
            logger.info('保存提款详情失败:%s' %statusDesc)

    
    def submit_withdrawal_apply(self,withdrawalApplyId):
        #提交提款申请
        url = "%s/withdrawal/apply/submit" % self._lambda_url
        data = {
                "withdrawalApplyId":withdrawalApplyId
            }
        res = self._request.post(url,data=json.dumps(data),headers=self._headers)
        status = json.loads(res.content.decode()).get('statusCode')
        if status == '0':
            logger.info('提交提款成功：%s' %withdrawalApplyId)
        else:
            statusDesc = json.loads(res.content.decode()).get('statusDesc')
            logger.info('提交提款失败:%s' %statusDesc)
    
    
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