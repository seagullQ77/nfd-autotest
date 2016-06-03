 # -*- coding:utf-8 -*-
import random
import time
from robot.api import logger
from selenium.webdriver.common.keys import Keys
from robot.libraries.BuiltIn import BuiltIn

class _OmegaMpKeywords():
    
    def __init__(self):        
        pass
        
    '''
         登录omega mp
    phone: 为空则随机生成一个手机号码，否则使用传入的手机号登录
    '''
    def login_omega_mp(self,phone=None):
        if self._browser is None:
            self._browser = BuiltIn().get_library_instance('Selenium2Library')
            self._browser.set_selenium_speed(0.1)
            self._browser.set_selenium_implicit_wait(3)
        if  self._mp_browser is None:
            self._mp_browser = self._browser.open_browser(self._mp_ord_url,browser=self._browser_type)
            #self._browser.maximize_browser_window()
        if phone is None:
            phone = self._myfaker.phone_number()
        if not self._browser._is_element_present('name=mobile') or \
           not self._browser._is_element_present('name=smsCode'):
            try:
                self.logout_omega_mp()
            except:
                logger.info("log out omega mp first error:maybe not login")            
        self._browser.input_text('name=mobile',phone)
        self._browser.input_text('name=smsCode',self._sms_code)
        self._browser.click_element('xpath= //*[@id="mod-main-content"]/div[3]/div/button')
        
        return phone
    
    '''
          退出omega mp
    '''
    def logout_omega_mp(self,phone=None):
        time.sleep(1)
        self._browser.wait_until_page_contains_element('xpath=//*[@id="mod-header"]/button', timeout=2)
        self._browser.click_element('xpath=//*[@id="mod-header"]/button')
        self._browser.wait_until_page_contains_element(u'link=退出登录', timeout=2)
        self._browser.click_link(u'link=退出登录')
        #再次确定按钮
        if self._browser._is_visible("id=dialogButton0"):
            self._browser.click_element('id=dialogButton0')
    
    '''
          当打开了多个浏览页面时，使用此关键字可以返回到打开mp的浏览页面
    '''
    def switch_to_mp_browser(self):
        if self._mp_browser is not None:
            self._browser.switch_browser(self._mp_browser)
    
    '''
          若还未注册为用户，登录后填写个人信息，注册为新用户
     usr_name:姓名，若为空，随机生成一个姓名
     usr_id:身份证号，若为空，随机生成身份证号
     province:省份，若为空，随机选择一个省份
     city:城市，若为空，随机选择一个城市
     addr:详细地址，若为空，自动生成一个地址
     
          返回:usr_name,可在omega查看贷款申请，提交审核贷款申请时传入该参数，定位到该笔申请(姓名是随机生成的，因此默认是唯一的，可以用该字段匹配贷款申请，
          如果自己填写的姓名，也应保证是唯一的，以便后续流程可以正确进行自动化测试)
    '''
    def submit_personal_info(self,usr_name=None,usr_id=None,province=None,city=None,addr=None):
        if usr_name is None:
            usr_name = self._myfaker.name_wuxia()
        if usr_id is None:
            usr_id = self._myfaker.person_id()
            
        self._browser.input_text('name=name',usr_name)
        self._browser.input_text('name=idCard',usr_id)
        
        if province is None:
            self._random_choose_provice_city()
        else:
            self._browser.select_from_list_by_label('name=province',province)
            self._browser.select_from_list_by_label('name=city',city)
            self._browser.input_text('name=address',addr)
        self._browser.click_element('xpath= //section[@id="mod-main-content"]/div[2]/div/button')
        return usr_name
        
    '''
          提交贷款申请信息
    loaner:贷款主体，若为空，默认选择注册用户名为贷款主体,若为company，则自动添加一个企业作为借款方
    amount:申请金额，若为空，生成一个1-100的随机数填入
    timelimit:借款期限，若为空，生成一个1-24的随机数填入
    '''
    def submit_loan_info(self,loaner=None,amount=None,timelimit=None):
        if loaner is None:
            loan_list=self._browser.get_list_items('name=loaner')
            if len(loan_list) <= 1:
                time.sleep(2)
                loan_list=self._browser.get_list_items('name=loaner')
            assert len(loan_list) > 1, u"获取到的贷款主体列表小于1,不正确!" 
            del loan_list[0]
            loaner = random.choice(loan_list)
        elif loaner == 'company':
            loaner = self.add_company_laoner() 
            self._browser.wait_until_page_contains_element('name=loaner',timeout=10)            
        self._browser.select_from_list_by_label('name=loaner',loaner)
        if amount is None:
            amount = random.randint(1,100)
        if timelimit is None:
            timelimit = random.randint(1,24)
        self._browser.input_text('name=amount',amount)
        self._browser.input_text('name=timelimit',timelimit)
        self._browser.click_element('xpath= //section[@id="mod-main-content"]/div[2]/div/button')
        self._browser.click_element("id=dialogButton0")
        return loaner
    
    def add_company_laoner(self):
        company_name = self._myfaker.company()
        self._browser.click_link(u'link=添加')
        self._browser.input_text('name=corporateName',company_name)#企业名称
        self._browser.input_text('name=corporateCode',self._myfaker.corporate_code())#营业执照
        self._browser.input_text('name=organizationCode',self._myfaker.organization_code())#组织机构码
        self._browser.input_text('name=corporateHolder',self._myfaker.name())#法人姓名
        self._browser.input_text('name=corporateIdCard',self._myfaker.person_id())#法人身份证 
        self._random_choose_provice_city()
        self._browser.click_element('xpath=//*[@id="mod-main-content"]/div[2]/div/button')
        return company_name
    
    '''
          随机选取省份、城市和填入地址信息
    '''
    def submit_loan_request(self,type=None,phone=None,amount=None):
        self.login_omega_mp(phone)
        loaner_name = self.submit_personal_info()
        if type is None:
            type = self._myfaker.random_element(['person','company'])
        if type == 'person':
            self.submit_loan_info(amount=amount)
        elif type == 'company':
            loaner_name = self.submit_loan_info(loaner='company',amount=amount)
        return loaner_name
        
    def _random_choose_provice_city(self):
        '''
        pro_list = self._browser.get_list_items('name=province')
        assert len(pro_list) > 1, u"获取到的省份列表小于1,不正确!"   
        del pro_list[0]
        province=random.choice(pro_list)
        self._browser.select_from_list_by_label('name=province',province)
        city_list = self._browser.get_list_items('name=city')
        if len(city_list) <= 1:
            time.sleep(1)
            city_list = self._browser.get_list_items('name=city')
        assert len(city_list) > 1, u"获取到的城市列表小于1,不正确!" 
        del city_list[0]
        city=random.choice(city_list)
        self._browser.select_from_list_by_label('name=city',city)
       
        addr = "%s%s%s"%(province,city,self._myfaker.address())
        self._browser.input_text('name=address',addr)
        '''
        rand_list = self._myfaker.province_city_name()
        self._browser.select_from_list_by_label('name=province',rand_list[0])
        self._browser.select_from_list_by_label('name=city',rand_list[1])
       
        addr = "%s%s%s"%(rand_list[0],rand_list[1],self._myfaker.address())
        self._browser.input_text('name=address',addr)
        
    '''
         提交提款申请
    amount:申请的提款金额，若为空，会根据授信的额度-已申请的金额，计算出剩余可用金额，在该可用金额内生成一个随机数
    period:借款期限，若为空，生成1-24的随机数填入
    add_receiver:是否添加收款方信息(户名、银行卡号、开户行等信息)，默认为False
                 True:添加收款方信息
                 False:不添加收款方信息
    '''
    def submit_withdraw_request(self,amount=None,period=None,add_receiver='False'):
        req_sum = 0
        if amount is None:
            req_sum = self.get_sum_withdraw_requested()
        self._browser.click_element('xpath=//*[@id="mod-header"]/button')
        self._browser.click_link(u'link=我的贷款')
        self._browser.wait_until_page_contains(u'贷款主体：', timeout=1)
        
        #获取登录用户的姓名
        tmp_str = self._browser.get_text('xpath=//*[@id="mod-main-content"]/ul/li/a/p[1]')
        tmp_list = tmp_str.split(u"：")
        name_usr = tmp_list[1]
        
        self._browser.click_element('xpath=//*[@id="mod-main-content"]/ul/li/a/h4')
        self._browser.wait_until_page_contains(u'我要提款', timeout=1)     
        self._browser.click_link(u'link=我要提款')
        
        if amount is None:
            val = self._browser.get_text('xpath=//*[@id="mod-main-content"]/div[1]/p[2]/span')       
            val_int = int(val.split(".")[0])
            amount = self._myfaker.random_int(1,val_int-req_sum)
        
        if period is None:
            period = self._myfaker.random_int(1,12)
        self._browser.input_text('name=withdrawalAmount',amount)
        self._browser.input_text('name=withdrawalPeriod',period)
        self._browser.input_text('name=smsCode',self._sms_code)
       
        if add_receiver == "True":           
            self._browser.click_link('xpath=//*[@id="mod-main-content"]/ul/li/a')
            if self._browser._page_contains(u"添加收款方信息"):
                self._browser.click_link(u'link=添加收款方信息')
            self._browser.input_text("name=accountName",name_usr)
            self._browser.input_text("name=cardNo",self._myfaker.credit_card_number())
            bank = self._list_random_select('name=banklist')
            self._browser.input_text("name=bankDeposit","%s%s"%(bank,self._myfaker.sentence()))
           
            #点击添加
            self._browser.click_element('xpath=//*[@id="mod-main-content"]/div[2]/div/button')
           
            #再次确定按钮
            if self._browser._is_visible("id=dialogButton0"):
                self._browser.click_element('id=dialogButton0')           

        self._browser.wait_until_page_contains(u'确定提款', timeout=1)
        self._browser.click_element('xpath=//*[@id="mod-main-content"]/div[3]/div/button')
        
        #再次确定按钮
        if self._browser._is_visible("id=dialogButton0"):
            self._browser.click_element('id=dialogButton0')
    
    '''获取已申请提款的金额'''
    def get_sum_withdraw_requested(self):
        
        self._browser.wait_until_page_contains(u'贷款申请列表', timeout=1)
        self._browser.click_element('xpath=//*[@id="mod-header"]/button')
        self._browser.click_link(u'link=我的贷款')
        self._browser.wait_until_page_contains(u'贷款主体：', timeout=1)
         
        self._browser.click_element('xpath=//*[@id="mod-main-content"]/ul/li/a/h4')
        self._browser.wait_until_page_contains(u'提款交易明细', timeout=1)     
        self._browser.click_link(u'link=提款交易明细')
        res_sum = 0
        if self._browser._page_contains(u'没有提款记录'):
            return res_sum
        else:
            req_list = self._browser.get_webelements('xpath=//*[@id="mod-main-content"]/ul/li')
            i = 1
            while i <= len(req_list):
                tmp_val = self._browser.get_text('xpath=//*[@id="mod-main-content"]/ul/li[%s]/a/div'%i)
                val = int(filter(lambda x:x.isdigit(),tmp_val))
                res_sum += val
                i += 1
        return res_sum
        
        
    '''
          操作select控件，随机选择一个选择项
    locator:select控件的路径，如id/name/xpath
         返回:随机选中的选择项
    '''
    def _list_random_select(self,locator):
        get_list = self._browser.get_list_items(locator)
        if len(get_list) <= 1:
            time.sleep(2)
            get_list=self._browser.get_list_items(locator)
        assert len(get_list) > 1, u"获取到的列表列表小于1,不正确!"   
        del get_list[0] #第一个元素为请选择，需要删除掉第一个元素
        random_item = self._myfaker.random_element(get_list)
        self._browser.select_from_list_by_label(locator,random_item)
        return random_item