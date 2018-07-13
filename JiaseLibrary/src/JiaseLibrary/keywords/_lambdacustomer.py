 # -*- coding:utf-8 -*-
import json
import random
import datetime
from functools import reduce
from robot.api import logger
from JiaseLibrary.utils.lambda_encrpt import LambdaEncrpt

class _LambdaCustomerKeywords():
    
    def __init__(self):        
        pass


    def custom_personal_create(self,cust_kind=None,cust_name=None,id_code=None):
        '''
        :param cust_kind:客户类型，若不传，则默认都选择,参数类型:'HZS|DBKH|DKKH' 代表 '合作商|担保客户|贷款客户'
        :param cust_name:客户名
        :param id_code:证件号
        :return:客户id
        '''
        url = '%s/cust/infos/personal/create' % self._lambda_url
        if cust_name is None:
            cust_name = self._faker.name_wuxia()
        if id_code is None:
            id_code = self._faker.person_id()

        cust_list = []
        if cust_kind is None:
            cust_kind_str = '1,2,4'
        else:
            cust_kind = cust_kind.split('|')
            if 'DKKH' in cust_kind :
              cust_list.append('1')
            if 'DBKH' in cust_kind :
              cust_list.append('2')
            if 'HZS' in cust_kind :
              cust_list.append('4')
            cust_kind_str = ','.join(cust_list)
            
        payload =   {
                    "baseInfo":     {
                                    "custName":cust_name,
                                    "custKind":cust_kind_str,
                                    "idType":'GR_SFZ',
                                    "idCode":id_code,
                                    "idExpire":"",
                                    "isLimitless":'',
                                    "createChannel":"20"
                                    },
                    "idExpire":"",
                    "isLimitless":"true"
                    }
        res = self._request.post(url,headers=self._headers,data=json.dumps(payload))
        ret = json.loads(res.content.decode())

        if ret.get('statusCode') == '0':
            logger.info('新增个人客户成功:%s' %cust_name)
            cust_id = ret.get('data')

            # 不校验id_code
            # AND id_code = '%s'
            sql =   """
                    SELECT count(*) FROM cust_info_base WHERE
                    cust_name = '%s' 
                    AND id = '%s' 
                    AND id_type = '%s' 
                     
                    AND cust_kind = '%s'
                    """ %(
                    cust_name,
                    cust_id,
                    'GR_SFZ',
                    #LambdaEncrpt(self._lambda_db_env)._encrypt(id_code),
                    reduce(lambda x, y:int(x) + int(y), cust_kind_str.split(','))
                    )
            db_check_flag = self.db.check_db(sql)
            if db_check_flag:
                logger.info('新增个人客户数据库验证成功')
            else:
                raise AssertionError('新增个人客户数据库验证失败 sql:%s' % sql)
            sql =   "SELECT count(*) FROM cust_info_personal WHERE id = '%s'"  % cust_id
            db_check_flag = self.db.check_db(sql)
            if db_check_flag:
                logger.info('新增个人客户数据库验证成功')
            else:
                raise AssertionError('新增个人客户数据库验证失败 sql:%s' % sql)

            self.custom_personal_update(cust_id, cust_name, id_code)
            self.cust_business_create(cust_id)
            self.cust_income_create(cust_id,cust_name)
            #self.cust_bank_accounts_create(cust_id)
            self.custom_update_db(cust_id, 'GR')
            return cust_id
        else:
            raise AssertionError('新增个人客户失败:错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))


    def cust_income_create(self,cust_id,cust_name):
        """

        #添加财政收入，授信必要条件
        :return:
        """
        url1 = '%s/cust/revexps/create' % self._lambda_url
        payload = {
            "businessSubject": cust_name,
            "businessSubjectId": cust_id,
            "custId":  cust_id,
            "recordmonth": 5,
            "recordmonthend": 5,
            "recordTime" :"2018/5",
            "recordTimeEnd": "2018/5",
            "recordyear": "2018" ,
            "recordyearend":"2018"
        }
        res1 = self._request.post(url1, headers=self._headers, data=json.dumps(payload))
        ret1 = json.loads(res1.content.decode())

        url2 = '%s/cust/revexps/list' % self._lambda_url
        params = {"custId": cust_id}
        res2 = self._request.get(url2, headers=self._headers, params = params)
        ret2 = json.loads(res2.content.decode())
        revenueExpenditure_list = ret2.get('data')
        for revenueExpenditure in revenueExpenditure_list:
            revenueExpenditure_id = revenueExpenditure.get('id')

        if ret1.get('statusCode') == '0':
            logger.info('添加收支信息成功，接下来添加收入信息')
            url3 = '%s/cust/revexps/income/create' % self._lambda_url
            payload1 ={
                "custId": cust_id,
                "incomeAmount" : 1000,
                "productType" : "CUST_PRODUCT_SEED",
                "purchasePrice" : 111,
                "revenueExpenditureId" : revenueExpenditure_id,
                "salePrice" : 111,
                "saleTrade" : "LS"
            }
            res3 = self._request.post(url3,headers=self._headers,data=json.dumps(payload1))
            ret3 = json.loads(res3.content.decode())
            if ret3.get('statusCode') == '0':
                logger.info('添加总收入成功')
            else:
                raise AssertionError('添加总收入失败:错误码:%s,错误信息:%s' % (ret3.get('statusCode'), ret3.get('statusDesc')))
        else:
            raise AssertionError('添加收入信息失败:错误码:%s,错误信息:%s' % (ret1.get('statusCode'), ret1.get('statusDesc')))

    def custom_enterprise_create(self,cust_personal_id,cust_kind=None, cust_name=None, id_code=None):
        '''
        新增企业客户
        :param cust_personal_id:个人客户id
        :param cust_kind:客户类型
        :param cust_name:客户名称
        :param id_code:证件号
        :return:客户id
        '''
        url = '%s/cust/infos/enterprise/create' % self._lambda_url
        if not cust_name:
            cust_name = self._faker.name_wuxia() + '企业'
        if not id_code:
            id_code = ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(18)])
        id_type = random.choice(['QY_XYDM','QY_YYZZH'])

        cust_list = []
        if cust_kind is None:
            cust_kind_str = '1,2,4'
        else:
            cust_kind = cust_kind.split('|')
            if 'DKKH' in cust_kind:
                cust_list.append('1')
            if 'DBKH' in cust_kind:
                cust_list.append('2')
            if 'HZS' in cust_kind:
                cust_list.append('4')
            cust_kind_str = ','.join(cust_list)

        payload = {
            "baseInfo": {
                "custName": cust_name,
                "custKind": cust_kind_str,
                "idType": id_type,
                "idCode": id_code,
                "createChannel": "20"
            },
            "idExpire": "",
            "isLimitless": "true"
        }
        res = self._request.post(url, headers=self._headers, data=json.dumps(payload))
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('新增企业客户成功:%s' % cust_name)
            cust_id = ret.get('data')
            self.custom_enterprise_update(cust_id, cust_name,cust_kind_str,id_type,id_code, cust_personal_id)
            self.cust_business_create(cust_id)
            self.cust_bank_accounts_create(cust_id)
            self.custom_update_db(cust_id,'QY')
            return cust_id
        else:
            raise AssertionError('新增企业客户失败:错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))


    def custom_personal_view(self,cust_id):
        '''
        查询个人客户信息
        :param cust_id:客户id
        :return:客户信息dict
        '''
        url = '%s/cust/infos/personal/view' % self._lambda_url
        params =    {
                    "custId":cust_id
                    }

        res = self._request.get(url,headers=self._headers,params=params)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('查询个人客户信息成功')
            return ret.get('data')
        else:
            raise AssertionError('查询个人客户信息失败:错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def custom_enterprise_view(self,cust_id):
        '''
        查询企业客户信息
        :param cust_id:客户id
        :return:客户信息dict
        '''
        url = '%s/cust/infos/enterprise/view' % self._lambda_url
        params =    {
                    "custId":cust_id
                    }

        res = self._request.get(url,headers=self._headers,params=params)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('查询企业客户信息成功')
            return ret.get('data')
        else:
            raise AssertionError('查询企业客户信息失败:错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def custom_view(self,cust_id):
        '''
        根据客户id与客户类型查询客户信息
        :param cust_name:客户名称
        :param cust_type:客户类型 GR:个人/QY:企业
        :return:客户信息dict
        '''
        try:
            cust_info = self.custom_personal_view(cust_id)
        except:
            cust_info = self.custom_enterprise_view(cust_id)
        return cust_info

    def custom_query(self,cust_name,cust_type,cust_id):
        '''
        根据客户名称查询客户信息
        :param cust_name:客户名
        :param cust_type:客户类型
        :param cust_id:客户id
        :return:客户信息dict
        '''
        url = '%s/cust/infos/queryByName' % self._lambda_url
        params =    {
                    "name":cust_name,
                    "custType":cust_type
                    }
        res = self._request.get(url,headers=self._headers,params=params)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('查询客户列表成功')
            custom_info_list = ret.get('data')
            for custom_info in custom_info_list:
                if custom_info.get('custName') == cust_name and custom_info.get('id') == cust_id:
                    return custom_info
            else:
                raise AssertionError('找不到对应的客户信息,%s %s %s' % (cust_name,cust_type,cust_id))
        else:
            raise AssertionError('查询客户列表失败:错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def custom_personal_update(self,cust_id, cust_name, id_code):
        #补充个人客户必填信息
        url = '%s/cust/infos/personal/update' % self._lambda_url
        mobile_phone = self._faker.phone_number()
        province_city_county = self.create_province_city_county()
        family_province_id = province_city_county.get('province_id')
        family_city_id = province_city_county.get('city_id')
        family_county_id = province_city_county.get('county_id')
        province_city_county = self.create_province_city_county()
        residence_province_id = province_city_county.get('province_id')
        residence_city_id = province_city_county.get('city_id')
        residence_county_id = province_city_county.get('county_id')

        health_condition = random.choice(['ZC','LH','YB','CJ','WZ'])
        family_address = self._faker.address()
        marital_condition = random.choice(['1','2','3','4'])
        education = random.choice(['ZJ','ZK','BK','YJS','CZ'])
        address_type = random.choice(['10','20'])
        residence_condition = random.choice(['10', '20', '30', '40', '50', '60', '70', '80'])
        residence_phone = self._faker.phone_number()
        residence_address = self._faker.address()
        family_count = str(random.randint(1, 10))

        #family_desc = self._faker.sentence()
        family_desc='1'
        work_year = str(random.randint(1, 30))
        #work_desc = self._faker.sentence()
        work_desc='1'


        payload =   {
                    "baseInfo": {
                                "custKind": "1,2,4",
                                "custName": cust_name,
                                "idCode": id_code,
                                "idType": 'GR_SFZ',
                                "mobilePhone": mobile_phone
                                },
                    "id": cust_id,
                    "custEdit": "true",
                    "custKind": ["1","2","4"],
                    "idExpire": "", #证件有效期
                    "country": "1",
                    "birthday": "",
                    "nation": "1",
                    "familyProvinceId": family_province_id,
                    "familyCityId": family_city_id,
                    "familyCountyId": family_county_id,
                    "healthCondition": health_condition,
                    "familyAddress": family_address,
                    "maritalCondition": marital_condition,
                    "education": education,
                    "isLimitless": "1", # 0不勾选有效 1勾选有效
                    "addressType": address_type,
                    "residenceCondition": residence_condition,
                    "residenceProvinceId": residence_province_id,
                    "residenceCityId": residence_city_id,
                    "residenceCountyId": residence_county_id,
                    "residencePhone": residence_phone,
                    "residenceVillage": "1",
                    "residenceAddress": residence_address,
                    "familyCount": family_count,
                    "familyDesc": family_desc,
                    "workYear": work_year,
                    "workDesc": work_desc
                    }
        res = self._request.post(url,headers=self._headers,data=json.dumps(payload))
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('%s新增个人客户详细信息成功' % cust_name)
            sql =   """
                    SELECT COUNT(*) FROM cust_info_personal WHERE
                    id = '%s' 
                    AND family_province_id = '%s' 
                    AND family_city_id = '%s' 
                    AND family_county_id = '%s' 
                    AND family_address = '%s' 
                    AND health_condition = '%s' 
                    AND marital_condition = '%s' 
                    AND education = '%s' 
                    AND address_type = '%s' 
                    AND residence_province_id = '%s' 
                    AND residence_city_id = '%s' 
                    AND residence_county_id = '%s' 
                    AND residence_condition = '%s' 
                    
                    AND family_count = '%s' 
                    AND family_desc = '%s' 
                    AND work_year = '%s' 
                    AND work_desc = '%s'
                    """ % (
                    cust_id,
                    family_province_id,
                    family_city_id,
                    family_county_id,
                    family_address,
                    health_condition,
                    marital_condition,
                    education,
                    address_type,
                    residence_province_id,
                    residence_city_id,
                    residence_county_id,
                    residence_condition,
                    #LambdaEncrpt(self._lambda_db_env)._encrypt(residence_phone), 不校验手机号
                    family_count,
                    family_desc,
                    work_year,
                    work_desc
                    )
            db_check_flag = self.db.check_db(sql)
            if db_check_flag:
                logger.info('新增个人客户数据库验证成功')
            else:
                raise AssertionError('新增个人客户数据库验证失败 sql:%s' % sql)
        else:
            raise AssertionError('新增个人客户详细信息失败:错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def custom_enterprise_update(self,cust_id,cust_name,cust_kind_str,id_type,id_code,cust_personal_id):
        #补充企业客户必填信息
        url = '%s/cust/infos/enterprise/update' % self._lambda_url
        mobile_phone = self._faker.phone_number()
        province_city_county = self.create_province_city_county()
        office_province_id = province_city_county.get('province_id')
        office_city_id = province_city_county.get('city_id')
        office_county_id = province_city_county.get('county_id')

        cust_personal_info = self.custom_personal_view(cust_personal_id).get('baseInfo')
        legal_person_name = cust_personal_info.get('custName')
        legal_person_id = cust_personal_info.get('id')
        controller_name = cust_personal_info.get('custName')
        controller_id = cust_personal_info.get('id')

        loan_bank_no = self._faker.credit_card_number()
        loan_bank_expire = (datetime.datetime.now() + datetime.timedelta(days=365)).strftime('%Y-%m-%d')
        regist_currency = random.choice(['RMB', 'MY'])
        regist_capital = str(random.randint(1, 9000))
        regist_date = (datetime.datetime.now() + datetime.timedelta(days=-365)).strftime('%Y-%m-%d')
        paidin_apital = str(random.randint(1, 9000))
        business_year = str(random.randint(1, 30))
        office_address = self._faker.address()
        working_field = random.choice(['M', 'N', 'K', 'L', 'O', 'R', 'S', 'P', 'Q', 'J', 'C', 'D', 'A', 'B', 'E', 'H', 'I', 'F', 'G','T'])
        enterprise_property = random.choice(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '161', '171'])
        enterprise_scale = random.choice(['10', '20', '30', '40'])
        business_place_type = random.choice(['1', '2', '3', '4'])
        business_place_size = str(random.randint(10, 1000))
        main_business = random.choice(['ZZ', 'SC', 'MY'])
        staff_count = str(random.randint(10, 10000))
        contact_name = cust_name + "业务联系人"
        #business_scope = self._faker.sentence()
        business_scope ='aaa'
        remark ='ss'
        #remark = self._faker.sentence()

        payload =   {
                    "id": cust_id,
                    "version": "0",
                    "baseInfo": {
                                "custKind": cust_kind_str,
                                "custName": cust_name,
                                "idType": id_type,
                                "idCode": id_code,
                                "telePhone": "",
                                "mobilePhone": mobile_phone
                                },
                    "organizationCode": "",
                    "legalPersonId": legal_person_id, # 法人id
                    "legalPersonName": legal_person_name, # 法人名称
                    "controllerId": controller_id, # 实际控制人id
                    "controllerName": controller_name, # 实际控制人名称
                    "loanBankNo": loan_bank_no, # 借款卡号
                    "loanBankExpire": loan_bank_expire, #借款卡号有效期
                    "registDate": regist_date, # 注册日期
                    "registCurrency": regist_currency, # 注册资本币种
                    "registCapital": regist_capital, # 注册资本
                    "paidinCapital": paidin_apital, # 实收资本
                    "businessYear": business_year, # 实际经营年限
                    "officeProvinceId": office_province_id,
                    "officeCityId": office_city_id,
                    "officeCountyId": office_county_id,
                    "officeAddress": office_address,
                    "workingField": working_field, # 所属行业
                    "enterpriseProperty": enterprise_property, # 企业性质
                    "enterpriseScale": enterprise_scale, # 企业规模
                    "businessPlaceType": business_place_type, # 经营场所类型
                    "businessPlaceSize": business_place_size, # 经营场所面积
                    "mainBusiness": main_business, # 主营业务
                    "staffCount": staff_count,# 员工人数
                    "contactName": contact_name, # 业务联系人
                    "businessScope": 'aaa', # 经营范围
                    "remark": 'ss'
                }   ##AND loan_bank_no = '%s'   #LambdaEncrpt(self._lambda_db_env)._encrypt(loan_bank_no),
        res = self._request.post(url,headers=self._headers,data=json.dumps(payload))
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('%s新增企业客户详细信息成功' % cust_name)
            sql =   """
                    SELECT COUNT(*) FROM cust_info_enterprise WHERE
                    id = '%s' 
                    AND legal_person_id = '%s' 
                    AND controller_id = '%s' 
                    AND loan_bank_expire = '%s' 
                    AND regist_date = '%s' 
                    AND regist_currency = '%s' 
                    AND regist_capital = '%s' 
                    AND business_year = '%s' 
                    AND office_province_id = '%s' 
                    AND office_city_id = '%s' 
                    AND office_county_id = '%s' 
                    AND office_address = '%s' 
                    AND working_field = '%s' 
                    AND enterprise_property = '%s' 
                    AND enterprise_scale = '%s' 
                    AND business_place_type = '%s' 
                    AND business_place_size = '%s' 
                    AND main_business = '%s' 
                    AND staff_count = '%s' 
                    AND contact_name = '%s' 
                    AND business_scope = '%s' 
                    AND remark = '%s'
                    """ % (
                    cust_id,
                    legal_person_id,
                    controller_id,
                    loan_bank_expire,
                    datetime.datetime.strptime(regist_date, "%Y-%m-%d").date().strftime('%Y-%m-%d %H:%M:%S'),
                    regist_currency,
                    regist_capital,
                    business_year,
                    office_province_id,
                    office_city_id,
                    office_county_id,
                    office_address,
                    working_field,
                    enterprise_property,
                    enterprise_scale,
                    business_place_type,
                    business_place_size,
                    main_business,
                    staff_count,
                    contact_name,
                    business_scope,
                    remark
                    )
            db_check_flag = self.db.check_db(sql)

            if db_check_flag:
                logger.info('新增个人客户数据库验证成功')
            else:
                raise AssertionError('新增个人客户数据库验证失败 sql:%s' % sql)

        else:
            raise AssertionError('新增企业客户详细信息失败:错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def cust_business_query(self,cust_id):
        '''
        查询经营信息列表
        :param cust_id:客户id
        :return:经营新低列表dict
        '''
        url = '%s/cust/business/new/list' % self._lambda_url
        params =   {
                    "custId":cust_id,
                    }
        res = self._request.get(url,headers=self._headers,params=params)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            return ret.get('data')
        else:
            raise AssertionError('查询经营信息列表失败:错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def cust_business_create(self,cust_id,business_type=None):
        '''
        新增经营信息大类
        :param cust_id:客户id
        :param business_type:主营类型  ZZ:种植类/SC:生产类/MY:贸易类
        :return:经营信息id
        '''
        # 查询经营信息列表,如果列表为空则是否主营业务设置为是,否则设置为否
        cust_business_list = self.cust_business_query(cust_id)
        if cust_business_list:
            is_main = False
        else:
            is_main = True

        if not business_type:
            business_type = random.choice(['ZZ','SC','MY'])

        if business_type == 'ZZ':
            plant_year = str(random.randint(1,10))
        else:
            plant_year = None

        url = '%s/cust/business/new/create' % self._lambda_url
        payload =   {
                    "businessType":business_type,   # ZZ:种植类/SC:生产类/MY:贸易类
                    "plantYear":plant_year,
                    "isMain":is_main, # 是否主营业务
                    "custId":cust_id,
                    #"remark":self._faker.sentence()
                    "remark":'1'
                    }
        res = self._request.post(url,headers=self._headers,data=json.dumps(payload))
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('新增主营业务成功')
            cust_business_id = ret.get('data')
            if business_type == 'ZZ':
                self.cust_business_plant_create(cust_business_id)
            else:
                self.cust_business_product_create(cust_business_id)
            sql = """SELECT count(*) FROM cust_business_info WHERE 
                  cust_id = '%s'
                  AND id = '%s'
                  AND is_main = '%s'
                  """ % (
                cust_id,
                cust_business_id,
                '1' if is_main else '0'
                )
            db_check_flag = self.db.check_db(sql)
            if db_check_flag:
                logger.info('新增主营业务数据库验证成功')
            else:
                raise AssertionError('新增主营业务数据库验证失败 sql:%s' % sql)
            return cust_business_id
        else:
            raise AssertionError('新增主营业务失败:错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def cust_business_delete(self,cust_id,cust_business_id):
        '''
        删除经营信息大类
        :param cust_id:客户id
        :param business_type:主营类型  ZZ:种植类/SC:生产类/MY:贸易类
        :return:
        '''
        url = '%s/cust/business/new/delete' % self._lambda_url
        payload =   {
                    "id":cust_business_id,
                    "custId":cust_id
                    }
        res = self._request.post(url,data=payload)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('删除主营业务大类成功')
        else:
            raise AssertionError('删除主营业务大类失败:错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def cust_business_plant_create(self, cust_business_id):
        '''
        新增种植类经营信息
        :param cust_id:客户id
        :param business_type:主营类型  ZZ:种植类/SC:生产类/MY:贸易类
        :return:
        '''
        url = '%s/cust/business/new/plant/create' % self._lambda_url
        payload =   {
                    "businessId": cust_business_id,
                    }
        res = self._request.post(url, headers=self._headers,data=json.dumps(payload))
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('新增种植类经营信息成功')
            sql = "SELECT COUNT(*) FROM cust_business_plant_new WHERE business_id = '%s'" % cust_business_id
            db_check_flag = self.db.check_db(sql)
            if db_check_flag:
                logger.info('新增种植类经营信息数据库验证成功')
            else:
                raise AssertionError('新增种植类经营信息失败 sql:%s' % sql)
        else:
            raise AssertionError('新增种植类经营信息失败:错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def cust_business_product_create(self, cust_business_id):
        '''
        新增生产类/贸易类经营信息
        :param cust_business_id:经营信息id
        :return:
        '''
        url = '%s/cust/business/new/product/create' % self._lambda_url
        payload =   {
                    "businessId": cust_business_id,
                    }
        res = self._request.post(url, headers=self._headers,data=json.dumps(payload))
        ret = json.loads(res.content.decode())
        sql = "SELECT COUNT(*) FROM cust_business_product_new WHERE business_id = '%s'" % cust_business_id
        db_check_flag = self.db.check_db(sql)
        if db_check_flag:
            logger.info('新增生产类/贸易类经营信息数据库验证成功')
        else:
            raise AssertionError('新增生产类/贸易类经营信息数据库验证失败 sql:%s' % sql)
        if ret.get('statusCode') == '0':
            logger.info('新增生产类/贸易类经营信息成功')
        else:
            raise AssertionError('新增生产类/贸易类经营信息失败:错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def cust_bank_accounts_create(self,cust_id,bank_name='中国工商银行',bank_sub_name='中国工商银行深圳市分行'):
        '''
        新增客户银行卡信息
        :param cust_business_id:经营信息id
        :return:
        '''
        is_corporate_account = random.choice(['true','false'])
        if is_corporate_account == 'true':
            pre_id_type = random.choice(['QY_XYDM', 'QY_YYZZH'])
            pre_idno = ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(18)])
        else:
            pre_id_type = 'GR_SFZ'
            pre_idno = self._faker.person_id()
        pre_phone = self._faker.phone_number()
        account_name = self._faker.name_wuxia()

        bank_info = self.dt_bank_info_query(bank_name)
        bank_code = bank_info.get('bankCode')
        bank_id = bank_info.get('id')

        bank_sub_info = self.dt_bank_sub_info_query(bank_sub_name,bank_code)
        bank_number = bank_sub_info.get('bankNumber')
        card_no = self._faker.credit_card_number()


        url = '%s/cust/bank/accounts/create' % self._lambda_url
        payload =   {
                    "isCorporateAccount":is_corporate_account, # 对公账户:true/对私账户:false
                    "accountName":account_name,
                    "cardNo":card_no,
                    "preIdtype":pre_id_type, # 信用代码:QY_XYDM/营业执照号:QY_YYZZH
                    "preIdno":pre_idno, # 证件号码
                    "prePhone":pre_phone, # 银行预留手机号码
                    "bankCode":bank_code,
                    "bankId":bank_id,
                    "bankName":bank_name,
                    "bankDeposit":bank_sub_name,
                    "bankNumber":bank_number, # 银行行号
                    "custId":cust_id
                    }
        res = self._request.post(url, headers=self._headers,data=json.dumps(payload))
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('新增生产类/贸易类经营信息成功')
            sql =   """
                    SELECT COUNT(*) FROM cust_bank_account WHERE 
                    account_name = '%s'
                    AND card_no = '%s'
                    AND bank_name = '%s'
                    AND bank_deposit = '%s'
                    AND pre_phone = '%s'
                    AND pre_idtype = '%s'
                    AND pre_idno = '%s'
                    AND is_corporate_account = '%s'
                    AND bank_number = '%s' 
                    """ % (
                    account_name,
                    card_no,
                    bank_name,
                    bank_sub_name,
                    pre_phone,
                    pre_id_type,
                    pre_idno,
                    1 if is_corporate_account == 'true' else 0,
                    bank_number
                    )
            db_check_flag = self.db.check_db(sql)
            if db_check_flag:
                logger.info('新增银行卡数据库验证成功')
            else:
                raise AssertionError('新增银行卡数据库验证失败 sql:%s' % sql)
        else:
            raise AssertionError('新增生产类/贸易类经营信息失败:错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def dt_bank_info_query(self, bank_name):
        '''
        查询根据银行名称查询银行相关信息
        :param bank_name:银行名称
        :return:
        '''
        url = '%s/dt/bank/listBankDetail' % self._lambda_url
        params =   {
                    "bankName":bank_name
                    }
        res = self._request.get(url, headers=self._headers,params=params)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('查询银行相关信息成功')
            bank_info_list = ret.get('data')
            for bank_info in bank_info_list:
                if bank_info.get('bankName') == bank_name:
                    return bank_info
            else:
                raise AssertionError('找不到对应的银行信息:%s' % bank_name)
        else:
            raise AssertionError('查询银行相关信息失败:错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def dt_bank_sub_info_query(self, bank_name,bank_code):
        '''
        查询支行信息
        :param bank_name:支行名称
        :param bank_code:银行code
        :return:
        '''
        url = '%s/dt/bank/listBankSub' % self._lambda_url
        params =    {
                    "bankCode":bank_code,
                    "bankName":bank_name
                    }
        res = self._request.get(url, headers=self._headers,params=params)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('查询银行相关信息成功')
            bank_info_list = ret.get('data')
            for bank_info in bank_info_list:
                if bank_info.get('bankName') == bank_name:
                    return bank_info
            else:
                raise AssertionError('找不到对应的银行信息:%s' % bank_name)
        else:
            raise AssertionError('查询银行相关信息失败:错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def custom_update_db(self,cust_id,cust_type):
        '''
        更新客户状态为JD,更新客户同步状态为SUCCESS,更新个人客户实名认证为PASS
        :param custId: 客户id
        :param custType: 客户类型
        :return:
        '''
        sql = "UPDATE cust_info_base SET cust_status='JD',sync_status='SUCCESS' WHERE id='%s' AND cust_type='%s'" % (cust_id, cust_type)
        self.db.exec_sql(sql)

        if cust_type == 'GR':
            sql = "UPDATE `cust_info_personal` SET id_check_result = 'PASS' WHERE id = '%s'" % cust_id
            self.db.exec_sql(sql)

    def custom_group_create(self,cust_id):
        '''
        新增关联客户组
        :param cust_id:客户id
        :return:关联客户id
        '''

        cust_name = self.custom_group_member_is_enable(cust_id)
        group_type = random.choice(['GROUP','COMPANY','RELATIVES','BUSINESS_CONTACT','BORROWER_GROUP'])
        url = '%s/cust/group/createGroup' % self._lambda_url
        payload =   {
                    "id":"",
                    "groupType":group_type,
                    "mainBorrowerId":cust_id,
                    "custName":cust_name
                    }
        res = self._request.post(url,headers=self._headers,data=json.dumps(payload))
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('新增关联客户成功')
            group_id = ret.get('data').get('id')
            return group_id
        else:
            raise AssertionError('新增关联客户失败:错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def custom_group_add_member(self,group_id,cust_id):
        '''
        添加关联组成员
        :param group_id:关联客户组id
        :param cust_id:客户id
        :return:
        '''
        cust_name = self.custom_group_member_is_enable(cust_id)
        relation = random.choice(['HOLD_INTEREST','LEGAL_PERSON'])
        url = '%s/cust/group/createMember' % self._lambda_url
        payload =   {
                    "id":"",
                    "relationCustId":cust_id,
                    "custName":cust_name,
                    "custType":"",
                    "mobilePhone":"",
                    "idType":"",
                    "idCode":"",
                    "relation":relation,
                    "groupId":group_id
                    }
        res = self._request.post(url,headers=self._headers,data=json.dumps(payload))
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('新增关联客户成员成功')
        else:
            raise AssertionError('新增关联客户成员失败:错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def custom_group_delete_member(self,group_id,cust_id):
        '''
        添加关联组成员
        :param group_id:关联客户组id
        :param cust_id:客户id
        :return:
        '''
        relation_id = self.custom_group_member_relation_id_get(group_id,cust_id)
        url = '%s/cust/group/deleteMember' % self._lambda_url
        payload =   {
                    "relationId":relation_id,
                    }
        res = self._request.post(url,data=payload)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('删除关联客户成员成功')
        else:
            raise AssertionError('删除关联客户成员失败:错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def custom_group_update_main_borrower(self,group_id,cust_id):
        '''
        设置关联客户组主借款人
        :param group_id:关联客户组id
        :param cust_id:客户id
        :return:
        '''
        relation_id = self.custom_group_member_relation_id_get(group_id,cust_id)
        url = '%s/cust/group/updateMainBorrower' % self._lambda_url
        payload =   {
                    "groupId":group_id,
                    "mainRelationId":relation_id
                    }
        res = self._request.post(url,data=payload)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('设置关联客户主借款人成功')
        else:
            raise AssertionError('设置关联客户主借款人失败:错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def custom_group_member_relation_id_get(self,group_id,cust_id):
        '''
        根据客户id查询关联客户关联id
        :param group_id:关联客户组id
        :return:关联客户关联id
        '''
        url = '%s/cust/group/viewGroup' % self._lambda_url
        params =    {
                    "id":group_id
                    }

        res = self._request.get(url,headers=self._headers,params=params)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('查看关联客户信息成功')
            cust_group_member_list = ret.get('data').get('memberList')
            for cust_group_member in cust_group_member_list:
                if cust_group_member.get('relationCustId') == cust_id:
                    return cust_group_member.get('id')
            else:
                raise AssertionError('对应的客户不在关联组内.cust_id:%s' % cust_id)
        else:
            raise AssertionError('查看关联客户信息成功失败:错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def custom_group_query(self,cust_name=None):
        '''
        查询可用的关联的客户列表
        :param cust_name:客户名
        :return:可用的关联的客户列表
        '''
        url = '%s/cust/group/queryCust' % self._lambda_url
        params =    {
                    "custName":cust_name,
                    "isMainBorrower":"true"
                    }

        res = self._request.get(url,headers=self._headers,params=params)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('查询可用关联的客户列表成功')
            return ret.get('data')
        else:
            raise AssertionError('查询可用关联的客户列表失败:错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def custom_group_member_is_enable(self,cust_id):
        '''
        查询客户是否可用的关联客户
        :param cust_id:
        :return:客户名
        '''
        custom_group_member_list = self.custom_group_query()
        for custom_group_member in custom_group_member_list:
            if custom_group_member.get('id') == cust_id:
                return custom_group_member.get('custName')
        else:
            raise AssertionError('可用关联客户列表中没有找到对应的客户,cust_id:%s' % cust_id)

    def custom_group_freeze(self,*args):
        '''
        冻结关联客户
        :param args:关联客户组id,支持输入多个
        :return:
        '''
        group_ids = ','.join(map(str,args))
        url = '%s/cust/group/freezeGroup' % self._lambda_url
        payload =   {
                    "groupIds":group_ids
                    }
        res = self._request.post(url,data=payload)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('冻结关联客户成功')
        else:
            raise AssertionError('冻结关联客户失败:错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))

    def custom_group_unfreeze(self,*args):
        '''
        冻结关联客户
        :param args:关联客户组id,支持输入多个
        :return:
        '''
        group_ids = ','.join(map(str,args))
        url = '%s/cust/group/unFreezeGroup' % self._lambda_url
        payload =   {
                    "groupIds":group_ids
                    }
        res = self._request.post(url,data=payload)
        ret = json.loads(res.content.decode())
        if ret.get('statusCode') == '0':
            logger.info('解冻关联客户成功')
        else:
            raise AssertionError('解冻关联客户失败:错误码:%s,错误信息:%s' % (ret.get('statusCode'), ret.get('statusDesc')))
