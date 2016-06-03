 # -*- coding:utf-8 -*-
import random
import time
from robot.api import logger
from selenium.webdriver.common.keys import Keys
from robot.libraries.BuiltIn import BuiltIn

class _OmegaConsoleKeywords():
    
    '''登录Omega系统
       usr:登录用户名
       psd:用户名对应密码
       usr和psd为空时，默认使用配置文件里的用户名和密码登录
    '''   
    def login_omega(self,usr=None,psd=None):        
        if self._browser is None:
            self._browser = BuiltIn().get_library_instance('Selenium2Library')
            self._browser.set_selenium_speed(0.1)
            self._browser.set_selenium_implicit_wait(3)
        
        if self._omega_browser is None:
            self._omega_browser = self._browser.open_browser(self._omega_url,browser=self._browser_type)
            #assert u'用户登录' in self._browser.get_title()
            self._browser.maximize_browser_window()
        
        if not self._browser._is_element_present('id=userCode') or \
           not self._browser._is_element_present('id=userPwd'):
            try:
                self.logout_omega()
            except:
                logger.info("log out omega first error:maybe not login") 
        if usr is None and psd is None:
            self._browser.input_text('id=userCode',self._omega_usr)
            self._browser.input_text('id=userPwd',self._omega_psd+Keys.RETURN)
        else:
            self._browser.input_text('id=userCode',usr)
            self._browser.input_text('id=userPwd',psd+Keys.RETURN)
            
    '''
         当前用户退出omega系统
    '''
    def logout_omega(self):        
        self._browser.click_link(u"link=首页")
        time.sleep(1)
        self._browser.click_element('xpath=/html/body/div[1]/header/nav/div/ul/li/a')
        self._browser.click_link(u"link=退出")
        
     
    '''随机获取一个担保方的名称并返回，在提交贷款申请时使用'''
    def get_loan_guarantor(self): 
        if self._browser._is_visible(u"link=担保方管理"):
            pass
        else:      
            self._browser.click_link(u"link=贷款管理")
        self._browser.click_link(u"link=担保方管理")
        guarantor_name = self._browser.get_table_cell('xpath=//*[@id="jsGridGuarantor"]/div[2]/table', 
                                                      random.randint(1,10), 1)
        return guarantor_name
       
    '''
          当打开了多个浏览页面时，使用此关键字可以返回到打开omega的浏览页面
    '''
    def switch_to_omega_browser(self):
        if self._omega_browser is not None:
            self._browser.switch_browser(self._omega_browser)
        
    '''
          贷款申请提交：进入贷款申请页面，点击修改，添加相关信息后，点击提交或者保存为草稿
    loan_name:借款方名称（个人或者企业名称），必填项
    loan_type:产品类型（种植贷、零售贷、经销商贷），为空时，随机从三种类型中选取一个
    guarantor_name:担保方名称，若为空，随机从担保方中选取一个
    advise_amount:建议自贷金额，若为空，则生成一个申请金额/2-申请金额的随机金额
    change:True重新填入信息,False已有信息，不需要重新填入信息，直接点击提交
    res:默认为submit，填写完信息后，点击提交
         draft:填写完信息后，点击保存草稿        
    '''

    def modify_loan_application(self,loan_name,loan_type=None,guarantor_name=None,advise_amount=None,
                                guarant_amount=None,guarant_amount_rich=None,change='True',res="submit"): 
        if change=='True' and guarantor_name is None:
                guarantor_name =  self.get_loan_guarantor()
        if self._browser._is_visible(u"link=贷款申请"):
            pass
        else:      
            self._browser.click_link(u"link=贷款管理")
        self._browser.click_link(u"link=贷款申请")
        
        #点击修改按钮，添加相关资料
        self._browser.wait_until_element_is_visible("xpath=//*[@id='jsGrid']/div[2]/table")
        row = self._browser.table_get_row_by_text("xpath=//*[@id='jsGrid']/div[2]/table",
                                            loan_name,
                                             7)
        self._browser.click_link('xpath= //*[@id="jsGrid"]/div[2]/table/tbody/tr[%s]/td[16]/div/a' %row)
        self._browser.click_element('xpath=//*[@id="editBtn"]')
        time.sleep(1)
        if change == "True":               
            # 如果已有担保方，删除担保方，重新添加：
            g_table_xpath = 'xpath=//*[@id="JSNaturalGuarantorTable"]/div[2]/table'
            if self._browser._is_visible(g_table_xpath):
                rows = self._browser.table_get_row_nums(g_table_xpath)
                tr_index = 1
                while tr_index <= rows:
                    self._browser.click_element('xpath=//*[@id="JSNaturalGuarantorTable"]/div[2]/table/tbody/tr[1]/td[6]/input[2]')
                    #再次确定按钮
                    if self._browser._is_element_present("id=Omega_Base_dialog_ok"):
                        self._browser.click_element('id=Omega_Base_dialog_ok')
                    time.sleep(1)
                    tr_index += 1 
                  
            #添加担保方，默认是添加非额度担保方，先从企业担保方页面随机选一个担保方，然后再添加                  
            tmp_locat = '''xpath=//i[@onclick="QueryComponent('guarantor_query_div',queryGuarantor,_selectedGuarantor,'非额度担保方')"]'''
            self._browser.click_element(tmp_locat)
            self._browser.input_text('xpath=//*[@id="guarantor_query_div_input_query_component"]/div[1]/input',guarantor_name+Keys.RETURN)
            self._browser.click_element('link=%s'%guarantor_name)
        
            if loan_type is None:
                loan_type = random.choice([u'种植贷',u'零售贷',u'经销商贷'])        
            self._browser.select_from_list_by_label('id=loanType',loan_type)
            
            guarant={"0.00":0.6,
                     "10000.00":0.1,
                     "200000.00":0.1,
                     "100000.00":0.1,
                     "200000.00":0.1}
            if guarant_amount is None:
                #guarant_amount= self._myfaker.random_element(guarant)
                guarant_amount = '0.00'
            if guarant_amount_rich is None:
                guarant_amount_rich = '0.00'
            yearRate = random.randint(15,24)
            proposerRate = random.randint(0,15)
            guarantorRate = yearRate-proposerRate
            
            #种植贷
            if loan_type == u'种植贷':
                self._browser.input_text("id=plantBreed",self._myfaker.crops()) #种植品种
                self._browser.input_text("id=plantDuration",random.randint(1,20)) #种植年限(年)
                self._browser.input_text("id=plantAreaSize",random.randint(100,2000)) #种植面积(亩)
                self._browser.input_text("id=plantSingleCost",random.randint(1000,5000))#单亩农资成本(元)
                self._browser.input_text("id=address",self._myfaker.address())#种植地址
                self._browser.input_text("id=creditBalance",random.randint(1000,10000))#申请时信用卡透支余额(元)
                self._browser.input_text("id=familyAmount",random.randint(1000000,10000000))#家庭总资产(元)
                self._browser.input_text("id=yearIncome",random.randint(100000,1000000))#家庭年度总收入(元)
                self._browser.input_text("id=familyDebt",random.randint(0,100000))#家庭总负债余额(元)
                self._browser.input_text("id=monthDebt",random.randint(0,100000))#家庭负债月还款额(元)            
                self._browser.input_text("id=yearRate",yearRate)#年化收益率
                self._browser.input_text("id=proposerRate",proposerRate)#申请人承担利率
                self._browser.input_text("id=guarantorRate",guarantorRate)#担保方承担利率
            #零售贷
            elif loan_type == u'零售贷':            
                #设置成立时间
                self._set_date_control("id=establishedDate",self._myfaker.date())
                
                self._browser.input_text("id=retailName",self._myfaker.company()) #零售店名称
                self._browser.input_text("id=yesterAmount",random.randint(1,20)) #去年营业额
                self._browser.input_text("id=address",self._myfaker.address())#零售店地址
                self._browser.input_text("id=familyAmount",random.randint(1000000,10000000))#家庭总资产(元)
                self._browser.input_text("id=familyDebt",random.randint(0,100000))#家庭总负债余额(元)
                self._browser.input_text("id=yearIncome",random.randint(100000,1000000))#家庭年度总收入(元)
                self._browser.input_text("id=monthDebt",random.randint(0,100000))#家庭负债月还款额(元)
                self._browser.input_text("id=creditBalance",random.randint(1000,10000))#申请时信用卡透支余额(元)
                
                self._browser.input_text("id=yearRate",yearRate)#年化收益率
                self._browser.input_text("id=proposerRate",proposerRate)#申请人承担利率
                self._browser.input_text("id=guarantorRate",guarantorRate)#担保方承担利率
                          
                self._browser.input_text("id=guaranteedAmount",guarant_amount)#普通担保金额
                self._browser.input_text("id=guaranteedAmountRich",guarant_amount_rich)#富农贷担保金额
            #经销商贷
            elif loan_type == u'经销商贷':   
                self._browser.input_text("id=retailName",self._myfaker.company()) #企业名称
                self._browser.input_text("id=beforeYesterCost",random.randint(1000000,10000000)) #前年销售成本(元)           
                self._browser.input_text("id=yesterCost",random.randint(1000000,10000000))#去年销售成本(元)
                self._browser.input_text("id=beforeYesterAmount",random.randint(10000,99999999))#前年销售额(元)
                self._browser.input_text("id=yesterAmount",random.randint(10000,99999999))#去年销售额(元)
                self._browser.input_text("id=beforeYesterProfit",random.randint(10000,50000000))#前年毛利润(元)
                self._browser.input_text("id=yesterProfit",random.randint(10000,50000000))#去年毛利润(元)
                
                yearRate = random.randint(15,24)           
                self._browser.input_text("id=yearRate",yearRate)#年化收益率
                self._browser.input_text("id=guaranteedAmount",guarant_amount)#普通担保金额
                self._browser.input_text("id=guaranteedAmountRich",guarant_amount_rich)#富农贷担保金额
            
            if advise_amount is None:
                advise_amount = self._get_value_and_chage("id=loanLimit")
            self._browser.input_text("id=adviseMoney",advise_amount)#建议自贷金额
            self._browser.input_text("id=advisePeriod",random.randint(1,24))#建议期限
            self._browser.select_from_list_by_label("id=repaymentType",
                                                    random.choice([u'按月付息,到期还本',u'等额本息',u'等额本金']))#还款方式
            self._browser.input_text("id=depositRatio",random.randint(5,10))#保证金比例
            
            #设置预用款时间  
            self._set_date_control("id=predictLoanDate",self._myfaker.date_today_next())
            
            self._browser.input_text("id=suggestion",self._myfaker.text())#调查意见
            
              
            self._browser.click_element('id=mainId_text')
            self._browser.input_text('xpath=//*[@id="user_query_div_input_query_component"]/div[1]/input',self.omega_usr_no+Keys.RETURN) #主办人
            self._browser.click_link('link=%s (工号:%s)'%(self.omega_usr_name,self.omega_usr_no))
            
        if res == 'submit':
            self._browser.click_element('xpath=/html/body/div[1]/div/div/nav/div/button[3]') #提交
        elif res == 'draft':
            self._browser.click_element('xpath=/html/body/div[1]/div/div/nav/div/button[2]') #保存草稿
            
        #再次确定按钮
        if self._browser._is_element_present("id=Omega_Base_dialog_ok"):
            self._browser.click_element('id=Omega_Base_dialog_ok') 
        
        #关闭成功消息提示
        if self._browser._is_element_present("id=Omega_Base_tip_closeBtn"):
            self._browser.click_element('id=Omega_Base_tip_closeBtn')
            
        
    ''' 总监审批环节：通过、不通过、拒绝三种结果
        loan_name:借款方名称（个人或者企业名称），必填项
        guarant_amount:普通担保金额
        guarant_amount_rich:富农贷担保金额
        res: pass 审批通过
             fail 审批不通过
             reject 审批拒绝           
    '''
    def loan_chief_approval (self,loan_name,res="pass",loan_limit=None,guarant_amount=None,guarant_amount_rich=None,
                             change='False'):
               
        if self._browser._is_visible(u"link=总监审批"):
            pass
        else:
            self._browser.click_link(u"link=贷款管理")           
        self._browser.click_link(u"link=总监审批")
        
        #点击详情，进行审批
        self._browser.wait_until_element_is_visible("xpath=//*[@id='jsGridApproved']/div[2]/table")
        row = self._browser.table_get_row_by_text("xpath=//*[@id='jsGridApproved']/div[2]/table",
                                                  loan_name,
                                                  1)
        self._browser.click_link('xpath=//*[@id="jsGridApproved"]/div[2]/table/tbody/tr[%s]/td[9]/a' %row)
       
        if change == 'True':
            guarant={"1000":0.4,
             "10000.00":0.2,
             "200000.00":0.2,
             "100000.00":0.1,
             "200000.00":0.1}
            loan_limit = self._get_value_and_chage("id=loanLimitMinisterVal")
            self._browser.input_text("id=loanLimitMinisterVal",loan_limit) #自贷金额(元)
            self._browser.input_text("id=loanPeriodMinister",random.randint(1,24))#建议期限(月)：
            if self._browser._is_visible("id=guaranteedAmountMinister"):
                self._browser.input_text("id=guaranteedAmountMinister",self._myfaker.random_element(guarant))#普通担保金额(元)
            if self._browser._is_visible("id=guaranteedAmountRichMinister"):
                self._browser.input_text("id=guaranteedAmountRichMinister",self._myfaker.random_element(guarant))#富农贷担保金额(元)
            self._browser.input_text("id=depositRatioAudit",random.randint(5,10))#保证金比例(%)
            self._browser.input_text("id=yearRateAudit",random.randint(15,24))#年化利率(%)
            
            self._browser.select_from_list_by_label("id=repaymentTypeAudit",
                                            random.choice([u'按月付息,到期还本',u'等额本息',u'等额本金']))#还款方式
        if loan_limit is not None:
            self._browser.input_text("id=loanLimitMinisterVal",loan_limit) #自贷金额(元)
        if guarant_amount is not None:
            self._browser.input_text("id=guaranteedAmountMinister",guarant_amount)#普通担保金额(元)
        if guarant_amount_rich is not None:
            self._browser.input_text("id=guaranteedAmountRichMinister",guarant_amount_rich)#富农贷担保金额(元)
        if res == "pass":
            self._browser.wait_until_element_is_visible("id=save")
            self._browser.input_text("id=feedbackInfoAudit",u"总监调查意见为通过：%s"%self._myfaker.paragraph())#调查意见
            self._browser.click_element("id=save")
        elif res == "fail":
            self._browser.wait_until_element_is_visible("id=save2")
            self._browser.input_text("id=feedbackInfoAudit",u"总监调查意见为不通过：%s"%self._myfaker.paragraph())#调查意见
            self._browser.click_element("id=save2")
        elif res == "reject":
            self._browser.wait_until_element_is_visible("id=save3")
            self._browser.input_text("id=feedbackInfoAudit",u"总监调查意见为拒绝：%s"%self._myfaker.paragraph())#调查意见
            self._browser.click_element("id=save3")
        else:
            raise "loan_chief_approval:res is not right(must be pass/fail/reject)"
        
        #再次确定按钮
        if self._browser._is_visible("id=Omega_Base_dialog_ok"):
            self._browser.click_element('id=Omega_Base_dialog_ok')
        
        #关闭成功消息提示
        if self._browser._is_visible("id=Omega_Base_tip_closeBtn"):
            self._browser.click_element('id=Omega_Base_tip_closeBtn')  
    
    ''' 内部审核环节：通过、不通过、拒绝三种结果
        loan_name:借款方名称（个人或者企业名称），必填项
        res: pass 审批通过
             fail 审批不通过
    '''
    def loan_inner_approval (self,loan_name,res="pass"):
               
        if self._browser._is_visible(u"link=内部审核"):
            pass
        else:
            self._browser.click_link(u"link=贷款管理")                    
        self._browser.click_link(u"link=内部审核")
        
        #点击详情，进行审批
        self._browser.wait_until_element_is_visible("xpath=//*[@id='jsGridSubmit']/div[2]/table")
        row = self._browser.table_get_row_by_text("xpath=//*[@id='jsGridSubmit']/div[2]/table",
                                                  loan_name,
                                                  1)
        self._browser.click_link('xpath=//*[@id="jsGridSubmit"]/div[2]/table/tbody/tr[%s]/td[9]/a' %row)
        
        self._browser.wait_until_element_is_visible("id=auditInfo")    
        self._browser.input_text("id=materialScore",random.randint(1,10))#资料评分
        
        if res == "pass":
            self._browser.input_text("id=auditInfo",u"审核意见为通过：%s"%self._myfaker.paragraph())#审核意见
            self._browser.click_element("id=save")
        elif res == "fail":
            self._browser.input_text("id=auditInfo",u"审核意见为不通过：%s"%self._myfaker.paragraph())#审核意见         
            self._browser.click_element("id=save2")
        else:
            raise "loan_chief_approval:res is not right(must be pass/fail)"
        
        #再次确定按钮
        if self._browser._is_visible("id=Omega_Base_dialog_ok"):
            self._browser.click_element('id=Omega_Base_dialog_ok')
        
        #关闭成功消息提示
        if self._browser._is_visible("id=Omega_Base_tip_closeBtn"):
            self._browser.click_element('id=Omega_Base_tip_closeBtn')
    
    ''' 贷款初审环节：通过、不通过、拒绝三种结果
        loan_name:借款方名称（个人或者企业名称），必填项
        res: pass 审批通过
             fail 审批不通过
             reject 审批拒绝
        guarant_amount:普通担保金额
        guarant_amount_rich:富农贷担保金额
        change: True 自动更改初审信息，会更改初审金额、年化收益率等信息，所有信息随机生成,但如果传入有其他参数，以传入参数为准
                False 不会自动更改初审信息，直接点击通过或者不通过或者拒绝，但如果传入有其他参数，仍会填入对应的值，修改相应的信息
    '''
    def loan_approval_first (self,loan_name,res="pass",loan_limit=None,guarant_amount=None,
                             guarant_amount_rich=None,change='False'):
               
        if self._browser._is_visible(u"link=贷款初审"):
            pass
        else:
            self._browser.click_link(u"link=贷款管理")           
        self._browser.click_link(u"link=贷款初审")
        self._browser.wait_until_element_is_visible("xpath=//*[@id='jsGridApproved']/div[2]/table")
        row = self._browser.table_get_row_by_text("xpath=//*[@id='jsGridApproved']/div[2]/table",
                                                  loan_name,
                                                  1)
        self._browser.click_link('xpath=//*[@id="jsGridApproved"]/div[2]/table/tbody/tr[%s]/td[9]/a' %row)
       
        if change == 'True':
            guarant={"1000":0.4,
             "10000.00":0.2,
             "200000.00":0.2,
             "100000.00":0.1,
             "200000.00":0.1}
            loan_limit = self._get_value_and_chage("id=loanLimitAuditVal")
            self._browser.input_text("id=loanLimitAuditVal",loan_limit) #初审金额(元)
            self._browser.input_text("id=loanPeriodAudit",random.randint(1,24))#建议期限(月)：
            if self._browser._is_visible("id=guaranteedAmountInitAuditStr"):
                self._browser.input_text("id=guaranteedAmountInitAuditStr",self._myfaker.random_element(guarant))#普通担保金额(元)
            if self._browser._is_visible("id=guaranteedAmountRichInitAuditStr"):
                self._browser.input_text("id=guaranteedAmountRichInitAuditStr",self._myfaker.random_element(guarant))#富农贷担保金额(元)
            self._browser.input_text("id=depositRatioAudit",random.randint(5,10))#保证金比例(%)
            self._browser.input_text("id=yearRateAudit",random.randint(15,24))#年化利率(%)
            
            self._browser.select_from_list_by_label("id=repaymentTypeAudit",
                                            random.choice([u'按月付息,到期还本',u'等额本息',u'等额本金']))#还款方式
        if loan_limit is not None:
            self._browser.input_text("id=loanLimitAuditVal",loan_limit) #初审金额(元)
        if guarant_amount is not None:
            self._browser.input_text("id=guaranteedAmountInitAuditStr",guarant_amount)#普通担保金额(元)
        if guarant_amount_rich is not None:
            self._browser.input_text("id=guaranteedAmountRichInitAuditStr",guarant_amount_rich)#富农贷担保金额(元)
        self._browser.input_text("id=initAuditScore",random.randint(1,10))#初审评分
        
        if res == "pass": 
            self._browser.wait_until_element_is_visible("id=save")
            self._browser.input_text("id=feedbackInfoAudit",u"初审意见为通过：%s"%self._myfaker.paragraph())#初审意见           
            self._browser.click_element("id=save")
        elif res == "fail":
            self._browser.wait_until_element_is_visible("id=save2")
            self._browser.input_text("id=feedbackInfoAudit",u"初审意见为不通过：%s"%self._myfaker.paragraph())#初审意见
            self._browser.click_element("id=save2")
        elif res == "reject":
            self._browser.wait_until_element_is_visible("id=save3")
            self._browser.input_text("id=feedbackInfoAudit",u"初审意见为拒绝：%s"%self._myfaker.paragraph())#初审意见
            self._browser.click_element("id=save3")
        else:
            raise "loan_chief_approval:res is not right(must be pass/fail/reject)"
        
        #再次确定按钮
        if self._browser._is_visible("id=Omega_Base_dialog_ok"):
            self._browser.click_element('id=Omega_Base_dialog_ok')
        
        #若贷款初审失败，则停止测试，并生成快照
        #self._browser.page_should_not_contain(u'贷款初审失败')
        '''
        if self._browser._is_visible('id=Omega_Base_tip'):
            msg = self._browser.get_text('xpath=//*[@id="Omega_Base_tip"]/h4')
            if u'失败' in msg:
                self._browser.capture_page_screenshot()
                raise AssertionError(u'贷款主体:%s,初审失败'%loan_name)
        '''     
        #关闭成功消息提示
        if self._browser._is_visible("id=Omega_Base_tip_closeBtn"):
            self._browser.click_element('id=Omega_Base_tip_closeBtn') 
        
             
    ''' 贷款复审环节：通过、不通过、拒绝三种结果
        loan_name:借款方名称（个人或者企业名称），必填项
        res: pass 审批通过
             fail 审批不通过
             reject 审批拒绝
        guarant_amount:普通担保金额
        guarant_amount_rich:富农贷担保金额
        change: True 自动更改复审信息，所有信息随机生成,但如果传入有其他参数，仍以传入参数为准
                False 不会自动更改初审信息，直接点击通过或者不通过或者拒绝，但如果传入有其他参数，仍会填入对应的值，修改相应的信息
    '''
    def loan_approval_again (self,loan_name,res="pass",loan_limit=None,guarant_amount=None,
                             guarant_amount_rich=None,change='False'):
               
        if self._browser._is_visible(u"link=贷款复审"):
            pass
        else:
            self._browser.click_link(u"link=贷款管理")           
        self._browser.click_link(u"link=贷款复审")
        self._browser.wait_until_element_is_visible("xpath=//*[@id='jsGridApproved']/div[2]/table")
        row = self._browser.table_get_row_by_text("xpath=//*[@id='jsGridApproved']/div[2]/table",
                                                  loan_name,
                                                  1)
        self._browser.click_link('xpath=//*[@id="jsGridApproved"]/div[2]/table/tbody/tr[%s]/td[9]/a' %row)
       
        if change == 'True':
            guarant={"1000":0.4,
             "10000.00":0.2,
             "200000.00":0.2,
             "100000.00":0.1,
             "200000.00":0.1}
            loan_limit = self._get_value_and_chage("id=loanLimitAuditVal")
            self._browser.input_text("id=loanLimitAuditVal",loan_limit) #初审金额(元)
            self._browser.input_text("id=loanPeriodAudit",random.randint(1,24))#建议期限(月)：
            if self._browser._is_visible("id=guaranteedAmountAudit"):
                self._browser.input_text("id=guaranteedAmountAudit",self._myfaker.random_element(guarant))#普通担保金额(元)
            if self._browser._is_visible("id=guaranteedAmountRichAudit"):
                self._browser.input_text("id=guaranteedAmountRichAudit",self._myfaker.random_element(guarant))#富农贷担保金额(元)
            self._browser.input_text("id=depositRatioAudit",random.randint(5,10))#保证金比例(%)
            self._browser.input_text("id=yearRateAudit",random.randint(15,24))#年化利率(%)
            
            self._browser.select_from_list_by_label("id=repaymentTypeAudit",
                                            random.choice([u'按月付息,到期还本',u'等额本息',u'等额本金']))#还款方式
        if loan_limit is not None:
            self._browser.input_text("id=loanLimitAuditVal",loan_limit) #初审金额(元)   
        if guarant_amount is not None:
            self._browser.input_text("id=guaranteedAmountAudit",guarant_amount)#普通担保金额(元)  
        if guarant_amount_rich is not None:
             self._browser.input_text("id=guaranteedAmountRichAudit",guarant_amount_rich)#富农贷担保金额(元)             
        
        if res == "pass": 
            self._browser.wait_until_element_is_visible("id=save") 
            self._browser.input_text("id=feedbackInfoAudit",u"复审意见为通过：%s"%self._myfaker.paragraph())#复审意见          
            self._browser.click_element("id=save")
        elif res == "fail":
            self._browser.wait_until_element_is_visible("id=save2")
            self._browser.input_text("id=feedbackInfoAudit",u"复审意见为不通过：%s"%self._myfaker.paragraph())#复审意见
            self._browser.click_element("id=save2")
        elif res == "reject":
            self._browser.wait_until_element_is_visible("id=save3")
            self._browser.input_text("id=feedbackInfoAudit",u"复审意见为拒绝：%s"%self._myfaker.paragraph())#复审意见
            self._browser.click_element("id=save3")
        else:
            raise AssertionError("loan_chief_approval:res is not right(must be pass/fail/reject)")
        
        #再次确定按钮
        if self._browser._is_visible("id=Omega_Base_dialog_ok"):
            self._browser.click_element('id=Omega_Base_dialog_ok')
        
        #若贷款复审失败，则停止测试，并生成快照
        #self._browser.page_should_not_contain(u'贷款复审失败')
        '''
        if self._browser._is_visible('id=Omega_Base_tip'):
            msg = self._browser.get_text('xpath=//*[@id="Omega_Base_tip"]/h4')
            if u'失败' in msg:
                self._browser.capture_page_screenshot()
                raise AssertionError(u'贷款主体:%s,复审失败'%loan_name)
        '''    
        #关闭成功消息提示
        if self._browser._is_visible("id=Omega_Base_tip_closeBtn"):
            self._browser.click_element('id=Omega_Base_tip_closeBtn') 
    
    ''' 贷审会环节：通过、不通过、拒绝三种结果
        loan_name:借款方名称（个人或者企业名称），必填项
        res: pass 审批通过
             fail 审批不通过
             reject 审批拒绝
        guarant_amount:普通担保金额
        guarant_amount_rich:富农贷担保金额
        change: True 自动更改复审信息，所有信息随机生成,但如果传入有其他参数，仍以传入参数为准
                False 不会自动更改初审信息，直接点击通过或者不通过或者拒绝，但如果传入有其他参数，仍会填入对应的值，修改相应的信息
    '''
    def loan_approval_meeting(self,loan_name,res="pass",loan_limit=None,guarant_amount=None,
                             guarant_amount_rich=None,change='False'):
               
        if self._browser._is_visible(u"link=贷审会"):
            pass
        else:
            self._browser.click_link(u"link=贷款管理")           
        self._browser.click_link(u"link=贷审会")
        self._browser.wait_until_element_is_visible("xpath=//*[@id='jsGridWaitLoan']/div[2]/table")
        row = self._browser.table_get_row_by_text("xpath=//*[@id='jsGridWaitLoan']/div[2]/table",
                                                  loan_name,
                                                  1)
        self._browser.click_link('xpath=//*[@id="jsGridWaitLoan"]/div[2]/table/tbody/tr[%s]/td[6]/a' %row)
       
        if change == 'True':
            guarant={"1000":0.4,
             "10000.00":0.2,
             "200000.00":0.2,
             "100000.00":0.1,
             "200000.00":0.1}
            loan_limit = self._get_value_and_chage("id=dsh_loanLimitAuditVal")
            self._browser.input_text("id=dsh_loanLimitAuditVal",loan_limit) #贷审金额(元)
            self._browser.input_text("id=dsh_loanPeriodAudit",random.randint(1,24))#贷审期限(月)：
            if self._browser._is_visible("id=dsh_guaranteedAmountAudit"):
                self._browser.input_text("id=dsh_guaranteedAmountAudit",self._myfaker.random_element(guarant))#普通担保金额(元)
            if self._browser._is_visible("id=dsh_guaranteedAmountRichAudit"):
                self._browser.input_text("id=dsh_guaranteedAmountRichAudit",self._myfaker.random_element(guarant))#富农贷担保金额(元)
            self._browser.input_text("id=dsh_depositRatioAudit",random.randint(5,10))#保证金比例(%)
            self._browser.input_text("id=dsh_yearRateAudit",random.randint(15,24))#年化利率(%)
            
            self._browser.select_from_list_by_label("id=dsh_repaymentTypeAudit",
                                            random.choice([u'按月付息,到期还本',u'等额本息',u'等额本金']))#还款方式
        if loan_limit is not None:
            self._browser.input_text("id=dsh_loanLimitAuditVal",loan_limit) #贷审金额(元)   
        if guarant_amount is not None:
            self._browser.input_text("id=dsh_guaranteedAmountAudit",guarant_amount)#普通担保金额(元)  
        if guarant_amount_rich is not None:
             self._browser.input_text("id=dsh_guaranteedAmountRichAudit",guarant_amount_rich)#富农贷担保金额(元)             
        
        if res == "pass": 
            self._browser.wait_until_element_is_visible("id=save") 
            self._browser.input_text("id=dsh_feedbackInfoAudit",u"贷审会意见为通过：%s"%self._myfaker.paragraph())#贷审会意见          
            self._browser.click_element("id=save")
        elif res == "fail":
            self._browser.wait_until_element_is_visible("id=save2")
            self._browser.input_text("id=dsh_feedbackInfoAudit",u"贷审会意见为不通过：%s"%self._myfaker.paragraph())#贷审会意见
            self._browser.click_element("id=save2")
        elif res == "reject":
            self._browser.wait_until_element_is_visible("id=save3")
            self._browser.input_text("id=dsh_feedbackInfoAudit",u"贷审会意见为拒绝：%s"%self._myfaker.paragraph())#贷审会意见
            self._browser.click_element("id=save3")
        else:
            raise AssertionError("loan_chief_approval:res is not right(must be pass/fail/reject)")
        #再次确定按钮
        if self._browser._is_visible("id=Omega_Base_dialog_ok"):
            self._browser.click_element('id=Omega_Base_dialog_ok')
        
        #若贷款复审失败，则停止测试，并生成快照
        #self._browser.page_should_not_contain(u'贷款复审失败')
        if self._browser._is_visible('id=Omega_Base_tip'):
            msg = self._browser.get_text('xpath=//*[@id="Omega_Base_tip"]/h4')
            if u'失败' in msg:
                self._browser.capture_page_screenshot()
                raise AssertionError(u'贷款主体:%s,贷审会失败'%loan_name)
            
        #关闭成功消息提示
        if self._browser._is_visible("id=Omega_Base_tip_closeBtn"):
            self._browser.click_element('id=Omega_Base_tip_closeBtn') 
            
    '''
        判断贷款申请的状态是否正确：
    loan_name:借款方名称（个人或者企业名称），必填项
    status:贷款申请的预期状态，必填项，现有的状态包括：待提交、已提交、内部审核未通过、内部审核已通过、终审已拒绝、终审未通过、终审已通过、初审未通过、
        初审已通过、初审已拒绝、总监审批通过、总监审批不通过、总监审批拒绝、合同签署成功、合同签署失败、复审已通过、复审未通过、复审已拒绝、贷审会已通过、
        贷审会未通过、贷审会已拒绝、担保方合同签署成功、担保方合同签署失败、放弃申请
    ''' 
    def loan_status_should_be(self,loan_name,status):
               
        if self._browser._is_visible(u"link=贷款申请"):
            pass
        else:      
            self._browser.click_link(u"link=贷款管理")
        self._browser.click_link(u"link=贷款申请")
        
        #点击修改按钮，添加相关资料
        self._browser.wait_until_element_is_visible("xpath=//*[@id='jsGrid']/div[2]/table")
        row = self._browser.table_get_row_by_text("xpath=//*[@id='jsGrid']/div[2]/table",
                                            loan_name,
                                             7)
        loan_status = self._browser.get_text('xpath= //*[@id="jsGrid"]/div[2]/table/tbody/tr[%s]/td[10]' %row)
        if loan_status == status:
            logger.info(u'%s的贷款申请状态为:%s,预期状态为:%s'%(loan_name,loan_status,status))
        else:
            self._browser.capture_page_screenshot()
            raise AssertionError(u'%s的贷款申请状态为:%s,预期状态为:%s'%(loan_name,loan_status,status))
        
            
    def _get_value_and_chage(self,locator): 
        get_text = self._browser.get_value(locator)
        get_text = get_text.replace(",",'')
        get_text = get_text.replace(".00",'')
        val = int(get_text)
        return random.randint(val/2,val)
    
    def _set_date_control(self,locator,date_str):
        element_date = self._browser.get_webelement(locator)
        script_str = ''
        if locator.startswith('id='):
            script_str += "var setDate=document.getElementById(\"%s\");"%locator.replace("id=","")
        elif locator.startswith('name='):
            script_str += "var setDate=document.getElementByName(\"%s\");"%locator.replace("name=","")
        elif locator.startswith('tag='):
            script_str += "var setDate=document.getElementsByTagName(\"%s\");"%locator.replace("tag=","")
        else:
            raise AssertionError("set date control error: locator is not right,must be id/name/tag")
        script_str += "if (setDate.hasAttribute('readonly')){setDate.removeAttribute('readonly');}"         
        self._browser.execute_javascript(script_str)
        element_date.clear()
        element_date.send_keys(date_str)
     
                   
                
                
        
        
        
        
    
    


