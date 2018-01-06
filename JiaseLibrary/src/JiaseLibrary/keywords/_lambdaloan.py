# -*- coding:utf-8 -*-
import json
import random
from robot.api import logger
from utils.lambda_db import LambdaDbCon


class _LambdaLoanKeywords():
    
    def __init__(self):
        pass

    def query_prod_id(self,prod_name):
        '''
        根据产品名称查询产品id
        :param prod_name:产品名称
        :return:产品id
        '''
        url = '%s/prod/childproduct/displayable_tree' % self._lambda_url
        res = self._request.get(url)
        ret = json.loads(res.content.decode())
        prod_info_list = ret.get('data')
        if ret.get('statusCode') == '0':
            logger.info('查询产品列表成功')
            for prod_info in prod_info_list:
                if prod_info.get('name') == prod_name:
                    prod_id = prod_info.get('id')
                    return prod_id
            else:
                raise AssertionError('产品表中找不到对应的产品:%s' % prod_name)
        else:
            raise AssertionError('查询产品列表失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def effectived_credit_config_query(self, cust_type, prod_id, loan_apply_id, loan_detail_id):
        '''
        获取产品授信配置id
        :param cust_type:客户类型
        :param prod_id:产品id
        :param loan_apply_id:授信id
        :param loan_detail_id:授信明细id
        :return:产品授信配置dict
        '''
        url = '%s/loan/credit/details/viewEffectivedCreditConfig' % self._lambda_url
        params = {
            "custType": cust_type,
            "prodId": prod_id,
            "loanApplyId": loan_apply_id,
            "loanDetailId": loan_detail_id
        }
        res = self._request.get(url, params=params)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('获取有效的产品授信配置成功')
            return ret.get('data')
        else:
            raise AssertionError('获取有效的产品授信配置失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def query_fund_source(self,fund_source_type_code):
        url = '%s/common/public/queryFundSource' % self._lambda_url
        params =    {
                    "fundSourceTypeCode":fund_source_type_code
                    }
        res = self._request.get(url, params=params,headers=self._headers)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('获取资金来源成功')
            return ret
        else:
            raise AssertionError('获取资金来源失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def create_fund_source(self):
        fund_source_list= self.query_fund_source('WDPT').get('data') + self.query_fund_source('LHDK').get('data')
        fund_source_dict = random.choice(fund_source_list)
        return fund_source_dict

    def query_provinces(self):
        '''
        获取省份列表
        '''
        url = '%s/dt/areas/prvinces' % self._lambda_url
        params = {}
        res = self._request.get(url, params=params,headers=self._headers)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('获取省份列表成功')
            return ret.get('data')
        else:
            raise AssertionError('获取省份列表失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def query_citys(self,area_id):
        '''
        根据省份id获取城市id列表
        :param area_id:省份id
        :return:城市id列表
        '''
        url = '%s/dt/areas/citys' % self._lambda_url
        params =    {
                    "areaId":area_id
                    }
        res = self._request.get(url, params=params,headers=self._headers)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('获取省份对应城市列表成功')
            return ret.get('data')
        else:
            raise AssertionError('获取省份对应列表失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def query_countys(self,area_id):
        '''
        根据城市id获取区域id列表
        :param area_id:城市id
        :return:区域id列表
        '''
        url = '%s/dt/areas/countys' % self._lambda_url
        params =    {
                    "areaId":area_id
                    }
        res = self._request.get(url, params=params,headers=self._headers)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('获取城市对应区列表成功')
            return ret.get('data')
        else:
            raise AssertionError('获取城市对应区列表失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def create_province_city_county(self):
        province_list = self.query_provinces()
        province_id = random.choice(province_list).get('areaId')
        city_list = self.query_citys(province_id)
        city_id = random.choice(city_list).get('areaId')
        county_list = self.query_countys(city_id)
        county_id = random.choice(county_list).get('areaId')
        province_city_county_dict = {
                                    'province_id':province_id,
                                    'city_id':city_id,
                                    'county_id':county_id
                                    }
        return province_city_county_dict

    def update_mgnt_fees(self,effectived_credit_config,loan_apply_id, loan_detail_id, prod_id):
        '''
        更新业务管理费信息
        :param effectived_credit_config:view_effectived_credit_config方法返回值
        :param loan_apply_id:授信id
        :param loan_detail_id:授信明细id
        :param prod_id:产品id
        :return:
        '''
        mgnt_fees_list = effectived_credit_config.get('mgntFees')

        for mgnt_fees in mgnt_fees_list:
            mgnt_fees_id = mgnt_fees.get('id')
            mgnt_fees_value = str(round(random.uniform(1,10),1))
            mgnt_fees_calc_type = random.choice(['NHLL','GDBL','GDZ'])
            mgnt_fees_item_id = mgnt_fees.get('itemId')
            mgnt_fees_item_name = mgnt_fees.get('itemName')

            url = '%s/loan/credit/mgntfees/update' % self._lambda_url
            payload =   {
                        "id": mgnt_fees_id,
                        "calcType": mgnt_fees_calc_type,
                        "feeValue": mgnt_fees_value,
                        "loanApplyId": loan_apply_id,
                        "loanDetailId": loan_detail_id,
                        "prodId": prod_id,
                        "itemId": mgnt_fees_item_id
                        }

            res = self._request.post(url, headers=self._headers, data=json.dumps(payload))
            ret = json.loads(res.content.decode())
            if ret.get('statusCode') == '0':
                logger.info('更新%s成功,产品明细id:%s' % (mgnt_fees_item_name,loan_detail_id))
            else:
                raise AssertionError('更新%s失败,产品明细id:%s,错误码:%s,错误信息:%s' % (mgnt_fees_item_name,loan_detail_id,ret.get('statusCode'), ret.get('statusDesc')))

    def update_service_fees(self, effectived_credit_config,loan_apply_id, loan_detail_id, prod_id):
        '''
        更新业务服务费信息
        :param effectived_credit_config:view_effectived_credit_config方法返回值
        :param loan_apply_id:授信id
        :param loan_detail_id:授信明细id
        :param prod_id:产品id
        :return:
        '''
        service_fees_list = effectived_credit_config.get('serviceFees')
        for service_fees in service_fees_list:
            service_fees_id = service_fees.get('id')
            service_fees_value = str(round(random.uniform(1,10),1))
            service_fees_calc_type = random.choice(['NHLL','GDBL','GDZ'])
            service_fees_item_id = service_fees.get('itemId')
            service_fees_item_name = service_fees.get('itemName')

            url = '%s/loan/credit/servicefees/update' % self._lambda_url
            payload =   {
                        "id": service_fees_id,
                        "calcType": service_fees_calc_type,
                        "feeValue": service_fees_value,
                        "loanApplyId": loan_apply_id,
                        "loanDetailId": loan_detail_id,
                        "prodId": prod_id,
                        "itemId": service_fees_item_id
                        }

            res = self._request.post(url, headers=self._headers, data=json.dumps(payload))
            ret = json.loads(res.content.decode())
            if ret.get('statusCode') == '0':
                logger.info('更新%s成功,产品明细id:%s' % (service_fees_item_name,loan_detail_id))
            else:
                raise AssertionError('更新%s失败,产品明细id:%s,错误码:%s,错误信息:%s' % (service_fees_item_name,loan_detail_id,ret.get('statusCode'), ret.get('statusDesc')))

    def loan_apply_create(self,cust_id):
        '''
        新增授信
        :param cust_id:客户id
        :param cust_type:客户类型
        :return: 授信id
        '''
        cust_info = self.custom_view(cust_id)
        cust_name_full = cust_info.get('baseInfo').get('custName') + '(' + cust_info.get('baseInfo').get('idCode') + ')'
        cust_id = cust_info.get('baseInfo').get('id')
        cust_type = cust_info.get('baseInfo').get('custType')

        url = '%s/loan/apply/add/create' % self._lambda_url
        data = {
            "custType": cust_type,
            "custId": cust_id,
            "custName": cust_name_full
        }
        res = self._request.post(url, data=json.dumps(data), headers=self._headers)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('新增授信成功')
            loan_apply_id = ret.get('data').get('id')
            sql = "SELECT COUNT(*) FROM loan_credit_apply WHERE id='%s' AND cust_id='%s'" %(loan_apply_id,cust_id)
            db = LambdaDbCon(self._lambda_db_host,self._lambda_db_user,self._lambda_db_passwd,self._lambda_db_port,self._lambda_db_charset)
            db_check_flag = db.check_db(sql)
            db.close()
            if db_check_flag:
                logger.info('新增授信数据库验证成功')
                return loan_apply_id
            else:
                raise AssertionError('新增授信数据库验证失败 sql:%s' % sql)
        else:
            raise AssertionError('新增授信失败,错误码:%s,错误信息: %s' % (ret.get('statusCode'), ret.get('statusDesc')))


    def loan_apply_prepare_create(self,loan_apply_id):
        '''
        生成授信明细id
        :param loan_apply_id:授信id
        :param cust_id:客户id
        :return:授信明细id
        '''
        loan_apply_cust_info = self.loan_apply_view(loan_apply_id)
        cust_id = loan_apply_cust_info.get('custId')

        url = '%s/loan/credit/details/prepare_create' % self._lambda_url
        params = {
            "loanApplyId": loan_apply_id,
            "custId": cust_id
        }
        res = self._request.get(url, params=params)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('生成授信明细id成功')
            loan_detail_id = ret.get('data').get('id')
            sql = "SELECT count(*) FROM loan_credit_detail WHERE cust_id ='%s' AND loan_apply_id='%s' AND id='%s'" %(cust_id,loan_apply_id,loan_detail_id)
            db = LambdaDbCon(self._lambda_db_host,self._lambda_db_user,self._lambda_db_passwd,self._lambda_db_port,self._lambda_db_charset)
            db_check_flag = db.check_db(sql)
            db.close()
            if db_check_flag:
                logger.info('新增授信明细数据库验证成功')
                return loan_detail_id
            else:
                raise AssertionError('新增授信明细数据库验证失败 sql:%s' % sql)
        else:
            raise AssertionError('生成授信明细id失败,错误码:%s,错误信息: %s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def bank_list(self,cust_id, account_type):
        '''
        获取客户银行账号列表
        :param cust_id:
        :param account_type:
        :return:客户银行卡相关信息list
        '''
        url = '%s/cust/bank/accounts/list' % self._lambda_url
        params = {
            "accountype": account_type,
            "custId": cust_id
        }
        res = self._request.get(url, headers=self._headers, params=params)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('获取客户银行账号列表成功')
            return ret.get('data')
        else:
            raise AssertionError('获取客户银行账号列表失败,错误码:%s,错误信息: %s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def query_agreement_list(self,loan_detail_id):
        '''
        获取账户约定信息
        :param loan_detail_id:授信明细id
        :return:账户约定信息dict
        '''
        url = '%s/contract/agreement/list' % self._lambda_url
        params = {
            "loanDetailId": loan_detail_id
        }
        res = self._request.get(url, headers=self._headers, params=params)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('获取账户约定信息成功')
            return ret.get('data')
        else:
            raise AssertionError('获取账户约定信息失败,错误码:%s,错误信息: %s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def update_agreement(self, loan_apply_id, loan_detail_id):
        '''
        更新账户约定信息
        :param cust_id:客户id
        :param cust_type:客户类型
        :param loan_apply_id:授信id
        :param loan_detail_id:授信明细id
        :return:
        '''
        agreement_info_list = self.query_agreement_list(loan_detail_id)
        for agreement_info in agreement_info_list:
            agreement_id = agreement_info.get('id')
            account_name = agreement_info.get('accountName')
            cust_id = agreement_info.get('custId')
            bank_info = self.bank_list(cust_id, 1)[0]
            card_no = bank_info.get('cardNo')
            pre_id_no = bank_info.get('preIdno')
            pre_phone = bank_info.get('prePhone')
            bank_name = bank_info.get('bankName')
            bank_deposit = bank_info.get('bankDeposit')
            bank_number = bank_info.get('bankNumber')
            bank_id = bank_info.get('id')
            apply_type = agreement_info.get('applyType')

            url = '%s/contract/agreement/update' % self._lambda_url
            payload = {
                "custId": cust_id,
                "custName": "",
                "id": agreement_id,
                "isCorporateAccount": "false",
                "accountName": account_name,
                "cardNo": card_no,
                "preIdno": pre_id_no,
                "prePhone": pre_phone,
                "bankName": bank_name,
                "bankDeposit": bank_deposit,
                "bankNumber": bank_number,
                "bankId": bank_id,
                "applyType": apply_type,
                "loanApplyId": loan_apply_id,
                "loanDetailId": loan_detail_id
            }
            res = self._request.post(url, headers=self._headers, data=json.dumps(payload))
            ret = json.loads(res.content.decode())
            if ret.get('statusCode') == '0':
                logger.info('更新账户约定成功')
                sql = "SELECT COUNT(*) FROM contract_agreement  WHERE id='%s' AND loan_apply_id='%s' AND loan_detail_id='%s' AND cust_id='%s' AND bank_id='%s' and apply_type='%s'" \
                        % (str(agreement_id),str(loan_apply_id),str(loan_detail_id),str(cust_id),str(bank_id),str(apply_type))
                db = LambdaDbCon(self._lambda_db_host,self._lambda_db_user,self._lambda_db_passwd,self._lambda_db_port,self._lambda_db_charset)
                db_check_flag = db.check_db(sql)
                db.close()
                if db_check_flag:
                    logger.info('新增授信明细数据库验证成功')
                else:
                    raise AssertionError('更新账户约定数据库验证失败 sql:%s' % sql)
            else:
                raise AssertionError('更新账户约定失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def loan_detail_self_temp_save(self,cust_id, prod_credit_id,prod_id,loan_apply_id, loan_detail_id,borrower_ratio,interest_subsidy_ratio,withhold):
        '''
        自贷额度暂存新增账户约定
        :param cust_id:客户id
        :param prod_credit_id:产品授信配置id
        :param prod_id:产品id
        :param loan_apply_id:授信id
        :param loan_detail_id:授信明细id
        :param borrower_ratio:借款人质保金保利
        :param interest_subsidy_ratio:贴息比例
        :param withhold:是否代扣
        :return:
        '''
        url = '%s/loan/credit/details/self/tempSave' % self._lambda_url
        data =  {
                "custId":cust_id,
                "id":loan_detail_id,
                "loanApplyId":loan_apply_id,
                "prodCreditId":prod_credit_id,
                "prodId":prod_id,
                "detailSelf":   {
                                "borrowerRatio":borrower_ratio,
                                "interestSubsidyRatio":interest_subsidy_ratio
                                },
                "withhold":withhold
                }
        res = self._request.post(url, data=json.dumps(data), headers=self._headers)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('自贷额度暂存新增账户约定成功')

        else:
            raise AssertionError('自贷额度暂存新增账户约定失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def loan_detail_self_save(self, loan_apply_id, loan_detail_id, prod_name,**kwargs):
        '''
        保存自贷额度信息
        :param prod_name:产品名称
        :param loan_apply_id:授信id
        :param loan_detail_id:授信明细id
        :param kwargs:
            self_limit:自贷额度
            loan_duration:自带额度
            loan_duration_unit:额度单位
            limit_type:额度类型
            repayment_type:还款方式
            withhold:是否代扣
        :return:
        '''
        loan_apply_cust_info = self.loan_apply_view(loan_apply_id)
        cust_id = loan_apply_cust_info.get('custId')
        cust_type = loan_apply_cust_info.get('custType')

        prod_id = self.query_prod_id(prod_name)
        effectived_credit_config = self.effectived_credit_config_query(cust_type, prod_id, loan_apply_id, loan_detail_id)
        prod_credit_config = effectived_credit_config.get('prodCreditConfig')
        prod_credit_id = prod_credit_config.get('id')
        self.update_mgnt_fees(effectived_credit_config,loan_apply_id, loan_detail_id, prod_id)
        self.update_service_fees(effectived_credit_config,loan_apply_id, loan_detail_id, prod_id)


        # 授信期限与授信期限单位
        loan_duration_unit = kwargs.get('loan_duration_unit',random.choice(["MONTH",'DAY'])) # 授信期限单位
        loan_duration_min = int(prod_credit_config.get('creditDurationMin'))
        loan_duration_max = int(prod_credit_config.get('creditDurationMax'))
        if loan_duration_unit == 'MONTH':
            loan_duration = str(random.randint(loan_duration_min, loan_duration_max))
        else:
            loan_duration = str(random.randint(loan_duration_min*28,loan_duration_max*28))
        loan_duration = kwargs.get('loan_duration',loan_duration)

        self_limit = kwargs.get('self_limit', str(random.randint(5,5000)*1000)) #自带额度
        limit_type = kwargs.get('limit_type', random.choice(['GENERAL','SPECIAL'])) # 额度类型
        single_withdrawal_period = str(random.randint(1,10)) # 单笔提款最长期限
        limit_duration = str(random.randint(1,10)) # 额度存续期限
        borrower_ratio = str(round(random.uniform(1,10),1))  # 借款人质保金比例
        init_interest_subsidy = "N" # 无用

        interest_subsidy_area = prod_credit_config.get('alllowDiscount').split(',')
        interest_subsidy = random.choice(interest_subsidy_area) # 是否贴息
        interest_subsidy_ratio = '0'

        borrow_year_rate = str(round(random.uniform(1,10),1)) # 借款主体承担年利率

        repayment_type_area = prod_credit_config.get('repaymentType').split(',')
        repayment_type = kwargs.get('repayment_type', random.choice(repayment_type_area)) # 还款方式

        interest_settlement_unit_area = prod_credit_config.get('interestSettlementDuration').split(',')
        interest_settlement_unit = random.choice(interest_settlement_unit_area) # 结息周期(M,S)

        interest_settlement_type_area = prod_credit_config.get('interestSettlementType').split(',')
        interest_settlement_type = random.choice(interest_settlement_type_area) # 结息方式(GDR,DYR)

        repayment_datetime_min = int(prod_credit_config.get('fixDayMin'))
        repayment_datetime_max = int(prod_credit_config.get('fixDayMax'))
        repayment_datetime = str(random.randint(repayment_datetime_min,repayment_datetime_max)) #固定还款日

        main_guarantee_type_area = prod_credit_config.get('mainGuaranteeForm').split(',')
        main_guarantee_type = random.choice(main_guarantee_type_area) # 主担保方式

        group_guarantee_type_area = prod_credit_config.get('combinationGuaranteeType').split(',')
        group_guarantee_type = random.choice(group_guarantee_type_area) # 组合担保类型

        group_guarantee_area = prod_credit_config.get('combinationGuarantee').split(',')
        group_guarantee = ','.join(random.sample(group_guarantee_area,random.choice(range(1,len(group_guarantee_area)+1)))) #组合担保

        repayment_source_area = prod_credit_config.get('repaymentSource').split(',')
        repayment_source = ','.join(random.sample(repayment_source_area,random.choice(range(1,len(repayment_source_area)+1)))) #还款来源

        loan_purpose_type_area = prod_credit_config.get('loanUsage').split(',')
        loan_purpose_type = random.choice(loan_purpose_type_area) # 贷款用途

        loan_payment_mode_area = prod_credit_config.get('paymentType').split(',')
        loan_payment_mode = random.choice(loan_payment_mode_area) # 借款支付方式
        withhold = kwargs.get('withhold',random.choice(['true','false'])) # 是否代扣
        
        if interest_settlement_type == 'DYR':
            repayment_datetime = None

        # DEBX 等额本息
        # YCFQ 到期还本付息
        # XXHB 到期还本,按周期付息
        # ZQBX 按计划还本,按周期付息
        # FDHK 分段还款
        if repayment_type == 'DEBX':
            interest_subsidy = 'N'
            interest_settlement_type = None
            repayment_datetime = None
            loan_duration_unit = 'MONTH'
        elif repayment_type == 'YCFQ':
            interest_settlement_type = None
            interest_settlement_unit = None
            repayment_datetime = None
            loan_duration_unit = 'DAY'
        elif repayment_type == 'XXHB':
            loan_duration_unit = 'MONTH'
        elif repayment_type == 'ZQBX':
            pass
        elif repayment_type == 'FDHK':
            interest_settlement_type = None
            repayment_datetime = None
            borrow_year_rate = str(round(random.uniform(10.2,20),1))

        loan_year_rate = str(float(borrow_year_rate) + float(interest_subsidy_ratio))  # 借款年化利率 = 借款人承担利率 + 贴息比例

        loan_detail = self.loan_detail_view(loan_detail_id)
        loan_detail_guarantor = loan_detail.get('detailGuarantorBean')

        if loan_detail_guarantor:
            province_id = loan_detail.get('prjProvinceId')
            city_id = loan_detail.get('prjCityId')
            county_id = loan_detail.get('prjCountyId')

            fund_source = loan_detail.get('fundSource')
            fund_source_type = loan_detail.get('fundSourceType')

            loan_duration = loan_detail.get('loanDuration')
            loan_duration_unit = loan_detail.get('loanDurationUnit')

            interest_settlement_type = loan_detail_guarantor.get('interestSettlementType')
            interest_settlement_unit = loan_detail_guarantor.get('interestSettlementUnit')
            repayment_type = loan_detail_guarantor.get('repaymentType')
            repayment_datetime = loan_detail_guarantor.get('repaymentDatetime')

        else:
            province_city_county = self.create_province_city_county()
            province_id = province_city_county.get('province_id')
            city_id = province_city_county.get('city_id')
            county_id = province_city_county.get('county_id')

            fund_source_dict = self.create_fund_source()
            fund_source = fund_source_dict.get('dictValue')
            fund_source_type = fund_source_dict.get('categoryCode')

        self.loan_detail_self_temp_save(cust_id, prod_credit_id,prod_id,loan_apply_id, loan_detail_id,borrower_ratio,interest_subsidy_ratio,withhold)
        self.update_agreement(loan_apply_id, loan_detail_id)

        url = '%s/loan/credit/details/self/save' % self._lambda_url
        data = {
            "prodName": prod_name,
            "prodId": prod_id,
            "alterType": "",
            "mainGuarantorId": "",
            "mainCustId": "",
            "mainCustName": "",
            "prjProvinceId": province_id,
            "prjCityId": city_id,
            "prjCountyId": county_id,
            "marketingChannel": "",
            "marketingReferrer": "",
            "marketingContact": "",
            "partnerName": "",
            "partnerId": "",
            "partnerPrjName": "",
            "partnerPrjRemark": "",
            "loanDuration": loan_duration,
            "loanDurationUnit": loan_duration_unit,
            "detailSelf": {
                "selfLimit": self_limit,
                "limitType": limit_type,
                "singleWithdrawalPeriod": single_withdrawal_period,
                "limitDuration": limit_duration,
                "borrowerRatio": borrower_ratio,
                "loanYearRate": loan_year_rate,
                "initInterestSubsidy": init_interest_subsidy,
                "interestSubsidy": interest_subsidy,
                "interestSubsidyRatio": interest_subsidy_ratio,
                "borrowYearRate": borrow_year_rate,
                "repaymentType": repayment_type,
                "interestSettlementUnit": interest_settlement_unit,
                "interestSettlementType": interest_settlement_type, 
                "repaymentDatetime": repayment_datetime,
                "mainGuaranteeType": main_guarantee_type,
                "groupGuaranteeType": group_guarantee_type,
                "groupGuarantee": group_guarantee,
                "repaymentSource": repayment_source,
                "loanPurposeType": loan_purpose_type,
                "loanPurposeRemark": "",
                "loanPaymentMode": loan_payment_mode
            },
            "withhold": withhold, 
            "fundSource": fund_source,
            "fundSourceType": fund_source_type,
            "loanApplyId": loan_apply_id,
            "id": loan_detail_id,
            "custId": cust_id,
            "prodCreditId": prod_credit_id
        }
        res = self._request.post(url, data=json.dumps(data), headers=self._headers)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('保存自贷额度成功')
            sql =   """
                    SELECT COUNT(*) FROM loan_detail_self WHERE
                    id = '%s'
                    AND  self_limit='%s'
                    AND cust_id = '%s'
                    AND limit_duration = '%s'
                    AND single_withdrawal_period = '%s'
                    AND borrower_ratio = '%s'
                    AND loan_year_rate = '%s'
                    AND interest_subsidy = '%s'
                    AND interest_subsidy_ratio = '%s'
                    AND borrow_year_rate = '%s'
                    AND repayment_type = '%s'
                    AND loan_purpose_type = '%s'
                    AND loan_payment_mode = '%s'
                    """% (
                    loan_detail_id,
                    "%.3f" % (float(self_limit)),
                    cust_id,
                    "%.4f" % (float(limit_duration)),
                    "%.4f" % (float(single_withdrawal_period)),
                    "%.4f" % (float(borrower_ratio)),
                    "%.4f" % (float(loan_year_rate)),
                    interest_subsidy,
                    "%.4f" % (float(interest_subsidy_ratio)),
                    "%.4f" % (float(borrow_year_rate)),
                    repayment_type,
                    loan_purpose_type,
                    loan_payment_mode
                    )
            db = LambdaDbCon(self._lambda_db_host,self._lambda_db_user,self._lambda_db_passwd,self._lambda_db_port,self._lambda_db_charset)
            db_check_flag = db.check_db(sql)
            db.close()
            if db_check_flag:
                logger.info('保存自贷额度数据库验证成功')
            else:
                raise AssertionError('保存自贷额度数据库验证失败 sql:%s' % sql)
        else:
            raise AssertionError('保存自贷额度失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def loan_detail_guarantor_save(self,loan_apply_id, loan_detail_id, prod_name, **kwargs):
        '''
        保存自贷额度信息
        :param cust_name:客户id
        :param cust_type:客户类型
        :param prod_name:产品名称
        :param loan_apply_id:授信id
        :param loan_detail_id:授信明细id
        :param kwargs
            self_limit:自贷额度
            guarantee_limit:担保额度
            loan_duration_unit:额度单位
            limit_type:额度类型
            repayment_type:还款方式
        :return:
        '''
        loan_apply_cust_info = self.loan_apply_view(loan_apply_id)
        cust_id = loan_apply_cust_info.get('custId')
        cust_type = loan_apply_cust_info.get('custType')

        prod_id = self.query_prod_id(prod_name)
        effectived_credit_config = self.effectived_credit_config_query(cust_type, prod_id, loan_apply_id, loan_detail_id)
        prod_credit_config = effectived_credit_config.get('prodCreditConfig')
        prod_credit_id = prod_credit_config.get('id')

        # 授信期限与授信期限单位
        loan_duration_unit = kwargs.get('loan_duration_unit',random.choice(["MONTH",'DAY'])) # 授信期限单位
        loan_duration_min = int(prod_credit_config.get('creditDurationMin'))
        loan_duration_max = int(prod_credit_config.get('creditDurationMax'))
        if loan_duration_unit == 'MONTH':
            loan_duration = str(random.randint(loan_duration_min, loan_duration_max))
        else:
            loan_duration = str(random.randint(loan_duration_min*28,loan_duration_max*28))
        loan_duration = kwargs.get('loan_duration',loan_duration)

        guarantee_limit = kwargs.get('guarantee_limit',str(random.randint(5,5000) * 1000))
        limit_type = kwargs.get('limit_type',random.choice(['GENERAL','SPECIAL']))
        limit_duration = str(random.randint(1,10)) # 额度存续期限
        single_highest_limit =  str(int(guarantee_limit) - (random.randint(1,int(guarantee_limit)/1000)*1000))# 单笔最高授信额度
        single_longest_limit_duration = str(random.randint(1,10))
        single_longest_limit_duration_unit = random.choice(["MONTH",'DAY'])
        loan_comprehensive_year_rate = str(random.randint(0,10))
        loan_comprehensive_year_rate_up = str(random.randint(0,10) + 30)
        loan_year_rate_guarantor =  str(random.randint(1,20)) #借款年化利率
        guarantee_ratio = str(round(random.uniform(1,10),1))
        config_borrow_year_rate = str(round(random.uniform(1,10),1))
        borrow_year_rate = str(round(random.uniform(1,10),1)) # 借款主体承担年利率

        repayment_type_area = prod_credit_config.get('repaymentType').split(',')
        repayment_type = random.choice(repayment_type_area) # 还款方式

        interest_settlement_unit_area = prod_credit_config.get('interestSettlementDuration').split(',')
        interest_settlement_unit = random.choice(interest_settlement_unit_area) # 结息周期(M,S)

        interest_settlement_type_area = prod_credit_config.get('interestSettlementType').split(',')
        interest_settlement_type = random.choice(interest_settlement_type_area) # 结息方式(GDR,DYR)

        repayment_datetime_min = int(prod_credit_config.get('fixDayMin'))
        repayment_datetime_max = int(prod_credit_config.get('fixDayMax'))
        repayment_datetime = str(random.randint(repayment_datetime_min,repayment_datetime_max)) #固定还款日

        main_guarantee_type_area = prod_credit_config.get('mainGuaranteeForm').split(',')
        main_guarantee_type = random.choice(main_guarantee_type_area) # 主担保方式

        group_guarantee_type_area = prod_credit_config.get('combinationGuaranteeType').split(',')
        group_guarantee_type = random.choice(group_guarantee_type_area) # 组合担保类型

        group_guarantee_area = prod_credit_config.get('combinationGuarantee').split(',')
        group_guarantee = ','.join(random.sample(group_guarantee_area,random.choice(range(1,len(group_guarantee_area)+1)))) #组合担保

        loan_payment_mode_area = prod_credit_config.get('paymentType').split(',')
        loan_payment_mode = ','.join(random.sample(loan_payment_mode_area,random.choice(range(1,len(loan_payment_mode_area)+1)))) # 借款支付方式


        # DEBX 等额本息 
        # YCFQ 到期还本付息
        # XXHB 到期还本,按周期付息
        # ZQBX 按计划还本,按周期付息
        # FDHK 分段还款
        if repayment_type == 'DEBX':
            interest_subsidy = 'N'
            interest_settlement_type = None
            repayment_datetime = None
            loan_duration_unit = 'MONTH'
        elif repayment_type == 'YCFQ':
            interest_settlement_type = None
            interest_settlement_unit = None
            repayment_datetime = None
            loan_duration_unit = 'DAY'
        elif repayment_type == 'XXHB':
            loan_duration_unit = 'MONTH'
        elif repayment_type == 'ZQBX':
            pass
        elif repayment_type == 'FDHK':
            interest_settlement_type = None
            repayment_datetime = None
            borrow_year_rate = str(round(random.uniform(10.2,20),1))

        if interest_settlement_type == 'DYR':
            repayment_datetime = None

        loan_detail = self.loan_detail_view(loan_detail_id)
        loan_detail_self = loan_detail.get('detailSelfBean')
        if loan_detail_self:
            province_id = loan_detail.get('prjProvinceId')
            city_id = loan_detail.get('prjCityId')
            county_id = loan_detail.get('prjCountyId')

            fund_source = loan_detail.get('fundSource')
            fund_source_type = loan_detail.get('fundSourceType')

            loan_duration = loan_detail.get('loanDuration')
            loan_duration_unit = loan_detail.get('loanDurationUnit')

            interest_settlement_type = loan_detail_self.get('interestSettlementType')
            interest_settlement_unit = loan_detail_self.get('interestSettlementUnit')
            repayment_type = loan_detail_self.get('repaymentType')
            repayment_datetime = loan_detail_self.get('repaymentDatetime')
        else:
            province_city_county = self.create_province_city_county()
            province_id = province_city_county.get('province_id')
            city_id = province_city_county.get('city_id')
            county_id = province_city_county.get('county_id')

            fund_source_dict = self.create_fund_source()
            fund_source = fund_source_dict.get('dictValue')
            fund_source_type = fund_source_dict.get('categoryCode')

        url = '%s/loan/credit/details/guarantor/save' % self._lambda_url
        data = {
            "prodName": prod_name,
            "prodId": prod_id,
            "mainCustId": "0",
            "mainCustName": "",
            "prjProvinceId": province_id,
            "prjCityId": city_id,
            "prjCountyId": county_id,
            "marketingChannel": "",
            "marketingReferrer": "",
            "marketingContact": "",
            "partnerName": "",
            "partnerId": "0",
            "partnerPrjName": "",
            "partnerPrjRemark": "",
            "loanDuration": loan_duration,
            "loanDurationUnit": loan_duration_unit,
            "detailGuarantor": {
                "guaranteeLimit": guarantee_limit,
                "limitType": limit_type,
                "limitDuration": limit_duration,
                "singleHighestLimit": single_highest_limit,
                "singleLongestLimitDuration": single_longest_limit_duration,
                "singleLongestLimitDurationUnit": single_longest_limit_duration_unit,
                "guaranteeRatio": guarantee_ratio,
                "loanComprehensiveYearRate": loan_comprehensive_year_rate,
                "loanComprehensiveYearRateUp": loan_comprehensive_year_rate_up,
                "loanYearRateGuarantor": loan_year_rate_guarantor,
                "repaymentType": repayment_type,
                "interestSettlementUnit": interest_settlement_unit,
                "interestSettlementType": interest_settlement_type,
                "repaymentDatetime": repayment_datetime,
                "configBorrowYearRate": config_borrow_year_rate,
                "mainGuaranteeType": main_guarantee_type,
                "groupGuaranteeType": group_guarantee_type,
                "groupGuarantee": group_guarantee,
                "loanPaymentMode": loan_payment_mode,
                "borrowYearRate": borrow_year_rate,
                "loanYearRate": "12"
            },
            "fundSource": fund_source,
            "fundSourceType": fund_source_type,
            "loanApplyId": loan_apply_id,
            "id": loan_detail_id,
            "custId": cust_id,
            "prodCreditId": prod_credit_id
        }

        res = self._request.post(url, data=json.dumps(data), headers=self._headers)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('新增担保额度成功')
        else:
            raise AssertionError('新增担保额度失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def loan_detail_view(self,loan_detail_id):
        '''
        查询授信明细详情
        :param loan_detail_id:授信明细id
        :return:授信详情dict
        '''
        url = '%s/loan/credit/details/view' % self._lambda_url
        params =    {
                    "id":loan_detail_id,
                    }
        res = self._request.get(url, params=params, headers=self._headers)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('查询授信详情成功')
            return ret.get('data')
        else:
            raise AssertionError('查询授信详情失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def loan_apply_view(self, loan_apply_id):
        '''
        查看授信申请详情
        :param loan_apply_id:
        :return:
        '''
        url = '%s/loan/apply/view' % self._lambda_url
        params =    {
                    "loanApplyId":loan_apply_id,
                    }
        res = self._request.get(url, params=params, headers=self._headers)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('授信详情查询成功')
            return ret.get('data')
        else:
            raise AssertionError('授信详情查询失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def loan_detail_id_list_query(self,loan_apply_id):
        '''
        查询授信下所有授信明细id
        :param loan_apply_id:授信id
        :return:授信明细id列表
        '''
        loan_detail_id_list = []
        loan_apply_info = self.loan_apply_view(loan_apply_id)
        loan_detail_list = loan_apply_info.get('detailList')
        for loan_detail in loan_detail_list:
            loan_detail_id = loan_detail.get('id')
            loan_detail_id_list.append(loan_detail_id)
        return loan_detail_id_list

    def loan_apply_submit(self,loan_apply_id,is_next='Y'):
        '''
        授信提交,投资经理提交授信申请
        :param loan_apply_id: 授信id
        :param is_next: Y/y:提交到下一节点  N/n:提交到被打回节点
        :return:
        '''
        task_id = self.loan_apply_task_id_query(loan_apply_id)

        # 授信task_id若存在,则表明是已经提交过了的,不存在则表示是初次提交
        if task_id:
            auditor_info = self.loan_apply_auditor_query(loan_apply_id,is_next)
            candidate_group_id = auditor_info.get('positionCode')
            assignee_user_id = auditor_info.get('userId')
            task_def_key = auditor_info.get('taskDefKey')
        else:
            assignee_user_id = None
            candidate_group_id = None
            task_def_key = None

        url = '%s/loan/apply/submit' % self._lambda_url
        payload = {
            "loanApplyId": loan_apply_id,
            "assigneeUserId":assignee_user_id,
            "candidateGroupId":candidate_group_id,
            "taskDefKey":task_def_key,
            "taskId":task_id

        }
        res = self._request.post(url, data=json.dumps(payload), headers=self._headers)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('授信提交成功')
        else:
            raise AssertionError('授信提交失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))


    def loan_apply_pass(self,loan_apply_id,is_next='Y',is_claim=None,candidate_group=None):
        '''
        授信审批,投资经理之后的每一步审批提交都需要调用
        :param loan_apply_id:授信id
        :param is_next: Y/y:提交到下一节点  N/n:提交到被打回节点
        :param is_claim: 是否领取任务,Y:领取
        :param candidate_group:岗位列表,格式为list 如: ['一级审批岗','二级审批岗','三级审批岗']
        :return:
        '''
        candidate_group_id = []
        task_id = self.loan_apply_task_id_query(loan_apply_id)
        process_status = self.loan_apply_view(loan_apply_id).get('processStatus') #流程状态
        if process_status == 'BACK':
            auditor_info = self.loan_apply_auditor_query(loan_apply_id,is_next=is_next)
            assignee_user_id = auditor_info.get('userId')
            task_def_key = auditor_info.get('taskDefKey')
            candidate_group_id = None
        elif process_status == 'RETREAT':
            assignee_user_id = None
            task_def_key = None
            candidate_group_id = None
        elif process_status == 'PASS':
            assignee_user_id = None
            task_def_key = None
            if candidate_group:
                for candidate in candidate_group:
                    if candidate == '一级审批岗':
                        candidate_group_id.append('POSITION_PRIMARY_AUDIT')
                    elif candidate == '二级审批岗':
                        candidate_group_id.append('POSITION_SECONDARY_AUDIT')
                    elif candidate == '三级审批岗':
                        candidate_group_id.append('POSITION_THIRD_AUDIT')
                    else:
                        pass
        else:
            raise  AssertionError('授信流程状态不正确,授信id:%s,授信流程状态:%s' %(loan_apply_id,process_status))
        # 领取任务
        if is_claim == 'Y' or is_claim == 'y':
            self.loan_task_claim(loan_apply_id)

        # 审核意见
        loan_detail_id_list = self.loan_detail_id_list_query(loan_apply_id)
        for i,loan_detail_id in enumerate(loan_detail_id_list):
            if i == 0:
                self.loan_advice(loan_detail_id, is_approved='1')
            else:
                self.loan_advice(loan_detail_id, is_approved=random.choice(['1','0']))

        url = '%s/loan/apply/pass' % self._lambda_url
        payload =   {
                    "assigneeUserId": assignee_user_id,
                    "candidateGroupId": candidate_group_id,
                    "taskDefKey":task_def_key,
                    "taskId":task_id
                    }
        res = self._request.post(url, data=json.dumps(payload), headers=self._headers)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('授信通过成功')
        else:
            raise AssertionError('授信通过失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def loan_apply_auditor_query(self,loan_apply_id,is_next='Y',user_name=None,candidate_group=None):
        '''
        查询授信可用审核人列表
        :param loan_apply_id:授信id
        :param is_next: Y/y:下一流程节点  N/n:回退的流程节点
        :return:
        '''

        candidate_group_id = []
        if candidate_group:
            for candidate in candidate_group:
                if candidate == '一级审批岗':
                    candidate_group_id.append('POSITION_PRIMARY_AUDIT')
                elif candidate == '二级审批岗':
                    candidate_group_id.append('POSITION_SECONDARY_AUDIT')
                elif candidate == '三级审批岗':
                    candidate_group_id.append('POSITION_THIRD_AUDIT')
                else:
                    pass

        url = '%s/loan/apply/auditor' % self._lambda_url

        payload =   {
                    "loanApplyId":loan_apply_id,
                    "pageSize":100,
                    "pageNo":1,
                    "userName":user_name,
                    "candidateGroupId":candidate_group_id
                    }
        res = self._request.post(url, data=json.dumps(payload),headers=self._headers)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('查询授信可用审核人列表成功')
            auditor_info_list = ret.get('list')
            if not auditor_info_list:
                auditor_info = {}
                return auditor_info
            if len(auditor_info_list) == 1:
                auditor_info = auditor_info_list[0]
            else:
                if is_next == 'Y' or is_next == 'y':
                    for auditor_info in auditor_info_list:
                        if auditor_info.get('group'):
                            return auditor_info
                elif is_next == 'N' or is_next == 'n':
                    for auditor_info in auditor_info_list:
                        if not auditor_info.get('group'):
                            return auditor_info
                else:
                    pass
        else:
            raise AssertionError('查询授信可用审核人列表失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def loan_apply_list(self,page_size=100,page_no=1):
        '''
        查询授信列表
        :param page_size:每页数量
        :param page_no:第几页
        :return:授信相关list
        '''
        url = '%s/loan/apply/add/list' % self._lambda_url
        params =    {
                    "pageNo":page_no,
                    "pageSize":page_size
                    }
        res = self._request.get(url, params=params, headers=self._headers)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('查询授信列表成功')
            return ret.get('list')
        else:
            raise AssertionError('授信列表查询失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def loan_apply_task_id_query(self,loan_apply_id):
        '''
        查询授信task_id
        :param loan_apply_id:授信id
        :return:task_id
        '''
        loan_apply_info_list = self.loan_apply_list(loan_apply_id)
        for loan_apply_info in loan_apply_info_list:
            if loan_apply_info.get('id') == loan_apply_id:
                loan_apply_task_id = loan_apply_info.get('taskId')
                return loan_apply_task_id

    def loan_task_claim(self,loan_apply_id):
        '''
        领取授信任务
        :param loan_apply_id:授信id
        :return:
        '''
        task_id = self.loan_apply_task_id_query(loan_apply_id)
        url = '%s/workbench/loanCreditApply/claim' % self._lambda_url
        payload =   {
                    "taskId": task_id
                    }
        res = self._request.post(url, data=payload)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('领取任务成功成功')
        else:
            raise AssertionError('领取任务失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))
     
    def task_unclaim(self,loan_apply_id):
        '''
        放回授信任务
        :param loan_apply_id:授信id
        :return:
        '''
        task_id = self.loan_apply_task_id_query(loan_apply_id)
        url = '%s/workbench/loanCreditApply/unclaim' % self._lambda_url
        payload =   {
                    "taskId": task_id
                    }
        res = self._request.post(url, data=payload)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('放回任务成功')
        else:
            raise AssertionError('放回任务失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def loan_advice_id_query(self,loan_detail_id):
        '''
        查询审核意见id
        :param loan_detail_id:授信明细id
        :return:审核意见id
        '''
        url = '%s/loan/advice/view' % self._lambda_url
        params =    {
                    "loanDetailId":loan_detail_id
                    }
        res = self._request.get(url, params=params, headers=self._headers)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            return ret.get('data').get('id')
        else:
            raise AssertionError('失败:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))


    def loan_advice(self,loan_detail_id,is_approved='1'):
        '''
        更新审核意见
        :param loan_detail_id:授信明细id
        :param is_approved:1:同意/0:不同意
        :return:
        '''
        advice_id = self.loan_advice_id_query(loan_detail_id)

        loan_score_details = []
        score = 10
        for i in range(18):
            point_score = random.randint(0, 10) / 10
            loan_score_id = str(i + 1)
            tmp = {
                "id": "",
                "adviceId": "",
                "loanScoreId": loan_score_id,
                "loanScoreConfigId": "",
                "pointScore": str(point_score)
                }
            loan_score_details.append(tmp)
            score -= point_score
            
        score = round(score, 1)
        if score < 0:
            score = 0

        url = '%s/loan/advice/save' % self._lambda_url
        payload =   {
                    "id":advice_id,
                    "isApproved":is_approved,
                    "adviceNote":"测试",
                    "score":score,
                    "loanDetailId":loan_detail_id,
                    "loanScoreDetails": loan_score_details
                    }
        res = self._request.post(url, data=json.dumps(payload), headers=self._headers)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('更新审核意见成功')
        else:
            raise AssertionError('更新审核意见失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def loan_apply_cancle(self,loan_apply_id):
        '''
        投资经理进行授信撤销
        :param loan_apply_id:授信id
        :return:
        '''
        url = '%s/loan/apply/cancel' % self._lambda_url
        task_id = self.loan_apply_task_id_query(loan_apply_id)
        payload =   {
                    "loanApplyId":loan_apply_id,
                    "taskId": task_id
                    }
        res = self._request.post(url, data=json.dumps(payload), headers=self._headers)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('授信撤销成功')
        else:
            raise AssertionError('授信撤销失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def loan_apply_reject(self,loan_apply_id,is_claim=None):
        '''
        授信审批拒绝
        :param loan_apply_id: 授信id
        :param is_claim: 是否领取任务,Y:领取
        :return: 
        '''

        # 领取任务
        if is_claim == 'Y' or is_claim == 'y':
            self.loan_task_claim(loan_apply_id)

        # 审核意见
        # 选择审批【拒绝】，不能有审核【同意】的授信明细

        loan_detail_id_list = self.loan_detail_id_list_query(loan_apply_id)
        for loan_detail_id in loan_detail_id_list:
            self.loan_advice(loan_detail_id, is_approved='1')

        url = '%s/loan/apply/reject' % self._lambda_url
        task_id = self.loan_apply_task_id_query(loan_apply_id)
        payload =   {
                    "loanApplyId":loan_apply_id,
                    "taskId": task_id
                    }
        res = self._request.post(url, data=json.dumps(payload), headers=self._headers)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('授信拒绝成功')
        else:
            raise AssertionError('授信拒绝失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def loan_apply_rollback_auditor(self,loan_apply_id):
        '''
        授信回退人列表
        :param loan_apply_id:授信id
        :return:授信回退人列表list
        '''

        url = '%s/loan/apply/rollbackAuditor' % self._lambda_url
        params =   {
                    "applyId":loan_apply_id
                    }
        res = self._request.get(url, params=params, headers=self._headers)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('查询授信回退人列表成功')
            return ret.get('data')
        else:
            raise AssertionError('查询授信回退人列表失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def loan_apply_back(self,loan_apply_id,back_position,is_claim=None):
        '''
        授信申请回退
        :param loan_apply_id:授信id
        :param is_claim: 是否领取任务,Y:领取
        :param back_position:回退节点 申请/复核/内审/初审/复审
        :return:
        '''

        # 领取任务
        if is_claim == 'Y' or is_claim == 'y':
            self.loan_task_claim(loan_apply_id)

        loan_detail_id_list = self.loan_detail_id_list_query(loan_apply_id)
        for loan_detail_id in loan_detail_id_list:
            self.loan_advice(loan_detail_id, is_approved=random.choice(['1','0']))

        loan_apply_rollback_auditor_list = self.loan_apply_rollback_auditor(loan_apply_id)

        for loan_apply_rollback_auditor in loan_apply_rollback_auditor_list:
            if loan_apply_rollback_auditor.get('nextTask') == back_position:
                assignee_user_id = loan_apply_rollback_auditor.get('userId')
                task_def_key = loan_apply_rollback_auditor.get('taskDefKey')
        if assignee_user_id and task_def_key:
            url = '%s/loan/apply/back' % self._lambda_url
            task_id = self.loan_apply_task_id_query(loan_apply_id)
            payload =   {
                        "taskId":task_id,
                        "assigneeUserId":assignee_user_id,
                        "taskDefKey":task_def_key
                        }
            res = self._request.post(url, data=json.dumps(payload), headers=self._headers)
            ret = json.loads(res.content.decode())
            if ret.get('statusCode') == '0':
                logger.info('授信回退成功')
            else:
                raise AssertionError('授信回退失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))
        else:
            raise AssertionError('回退节点不正确,选择的回退节点为:%s')

    def loan_apply_retreat(self,loan_apply_id):
        '''
        授信业务回收
        :param loan_apply_id:loan_apply_id
        :return:
        '''

        url = '%s/loan/apply/retreat' % self._lambda_url
        task_id = self.loan_apply_task_id_query(loan_apply_id)
        payload =   {
                    "taskId": task_id
                    }
        res = self._request.post(url, data=payload)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('授信业务收回成功')
        else:
            raise AssertionError('授信业务收回失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def loan_guarantors_query(self,cust_id):
        '''
        查询担保方相关信息
        :param cust_name:客户名
        :return:担保方相关信息dict
        '''
        cust_info = self.custom_view(cust_id)
        cust_name = cust_info.get('baseInfo').get('custName')
        url = '%s/loan/guarantors/queryGuarantorCust' % self._lambda_url
        params =   {
                    "name":cust_name
                    }
        res = self._request.get(url, params=params, headers=self._headers)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('查询担可用担保方成功')
            guarantors_info_list = ret.get('data')
            for guarantors_info in guarantors_info_list:
                if guarantors_info.get('custName') == cust_name and guarantors_info.get('id') == cust_id:
                    return guarantors_info
            else:
                raise AssertionError('输入的客户在可用担保方中查询不到')

        else:
            raise AssertionError('查询可用担保方失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def loan_guarantors_create(self,loan_detail_id,guarantors_cust_id,**kwargs):
        '''
        新增担保方
        :param loan_detail_id:授信明细id
        :param cust_name:担保方名称
        :param kwargs:
            is_deductible_limit:是否扣减担保额度
            is_main_guarantor:是否主担保方
            is_provide_guarantee:是否对担保项下借款主体提供担保
        :return:
        '''
        guarantors_info = self.loan_guarantors_query(guarantors_cust_id)
        guarantors_cust_id = guarantors_info.get('id')
        guarantors_cust_name = guarantors_info.get('custName')
        guarantors_cust_code = guarantors_info.get('custCode')

        loan_detail_info = self.loan_detail_view(loan_detail_id)
        loan_detail_self_info = loan_detail_info.get('detailSelfBean')
        interest_subsidy = loan_detail_self_info.get('interestSubsidy')


        guarantor_ratio =  str(random.randint(0,100))
        deposit_ratio = str(random.randint(0,100))

        if interest_subsidy == 'Y':
            interest_subsidy_ratio = str(round(random.uniform(1, 10), 1))
        else:
            interest_subsidy_ratio = '0'

        is_deductible_limit = kwargs.get('is_deductible_limit','false')
        is_main_guarantor = kwargs.get('is_main_guarantor','false')
        is_provide_guarantee = kwargs.get('is_provide_guarantee','false')
        url = '%s/loan/guarantors/create' % self._lambda_url
        payload =   {
                    "id":"",
                    "custId":guarantors_cust_id,
                    "custName":guarantors_cust_name,
                    "custCode":guarantors_cust_code,
                    "guarantorRatio":guarantor_ratio, # 担保比例
                    "depositRatio":deposit_ratio, # 质保金比例
                    "interestSubsidyRatio":interest_subsidy_ratio, # 贴息比例
                    "isDeductibleLimit":is_deductible_limit, # 是否扣减担保额度
                    "isMainGuarantor":is_main_guarantor, # 是否主担保方
                    "isProvideGuarantee":is_provide_guarantee, # 是否对担保项下借款主体提供担保
                    "loanDetailId":loan_detail_id
                    }

        res = self._request.post(url, data=json.dumps(payload), headers=self._headers)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('新增授信担保方成功')
            loan_detail_info = self.loan_detail_view(loan_detail_id)
            loan_apply_id = loan_detail_info.get('loanApplyId')
            loan_apply_info = self.loan_apply_view(loan_apply_id)
            cust_id = loan_apply_info.get('custId')
            cust_type = loan_apply_info.get('custType')
            self.update_agreement(loan_apply_id, loan_detail_id)
            sql =   """
                    SELECT
                      COUNT(*)
                    FROM
                      loan_guarantor_info
                    WHERE loan_detail_id = '%s' 
                      AND cust_name = '%s'
                      AND guarantor_ratio = '%s'
                      AND deposit_ratio = '%s'
                      AND interest_subsidy_ratio = '%s'
                      AND is_deductible_limit = '%s'
                      AND is_main_guarantor = '%s'
                      AND is_provide_guarantee = '%s'
                    """ % (
                    loan_detail_id,
                    guarantors_cust_name,
                    '%.3f' % (float(guarantor_ratio)),
                    '%.3f' % (float(deposit_ratio)),
                    '%.3f' % (float(interest_subsidy_ratio)),
                    '0' if is_deductible_limit == "false" else '1',
                    '0' if is_main_guarantor == "false" else '1',
                    '0' if is_provide_guarantee == "false" else '1'
                    )
            db = LambdaDbCon(self._lambda_db_host, self._lambda_db_user, self._lambda_db_passwd, self._lambda_db_port,self._lambda_db_charset)
            db_check_flag = db.check_db(sql)
            db.close()
            if db_check_flag:
                logger.info('新增授信担保方数据库验证成功')
            else:
                raise AssertionError('新增授信担保方数据库验证失败 sql:%s' % sql)
        else:
            raise AssertionError('新增授信担保方失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def loan_guarantors_delete(self,loan_detail_id,cust_name):
        '''
        新增担保方
        :param loan_detail_id:授信明细id
        :param cust_name:担保方名称
        :return:
        '''
        loan_guarantors_id = self.loan_guarantors_list_query(loan_detail_id,cust_name)
        url = '%s/loan/guarantors/delete' % self._lambda_url
        payload =   {
                    "id":loan_guarantors_id
                    }
        res = self._request.post(url, data=payload)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('删除授信担保方成功')
            sql = "SELECT COUNT(*) FROM loan_guarantor_info WHERE loan_detail_id = '%s' AND  cust_name = '%s'" %(loan_detail_id,cust_name)
            db = LambdaDbCon(self._lambda_db_host,self._lambda_db_user,self._lambda_db_passwd,self._lambda_db_port,self._lambda_db_charset)
            db_check_flag = db.check_db(sql,0)
            if db_check_flag:
                logger.info('删除授信担保方数据库验证成功')
            else:
                raise AssertionError('删除授信担保方数据库验证失败 sql:%s' % sql)
        else:
            raise AssertionError('删除授信担保方失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def loan_guarantors_list_query(self,loan_detail_id,cust_name):
        '''
        查询授信担保方
        :param loan_detail_id:授信明细id
        :return:授信担保信息id
        '''
        url = '%s/loan/guarantors/list' % self._lambda_url
        payload =   {
                    "loanDetailId":loan_detail_id
                    }
        res = self._request.post(url, data=payload)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('查询担保方列表成功')
            guarantors_list =  ret.get('data')
            for guarantors in guarantors_list:
                if guarantors.get('custName') == cust_name:
                    return guarantors.get('id')
            else:
                raise AssertionError('授信担保方列表中找不到对应的担保方')
        else:
            raise AssertionError('查询担保方列表失败,错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))
