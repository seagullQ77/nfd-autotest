# -*- coding: utf-8 -*-
#产生普通贷
import random

import requests
from faker import Factory

import provinceChoice


def loanGenerate(env=1,loanType=1):#1测试2联调3体验4预发布；1个人2企业
    urlTest= "https://ot.nongfadai.com"#1
    urlDev="https://omegadev.nongfadai.com"#2
    urlInt="https://omegaint.nongfadai.com"#3
    urlPre="https://omegapre.nongfadai.com"#4
    url = (urlTest, urlDev, urlInt, urlPre)[env - 1]
    fake=Factory.create('zh_CN')
    mobile=fake.phone_number()#注册手机
    idCard=fake.ssn()#身份证
    address=fake.address()
    provinceId= provinceChoice.pcList()[0]
    cityId= provinceChoice.pcList()[1]
    name=fake.name()
    timelimit=random.randrange(1,25)#贷款期限
    amount=random.randrange(1,350)#贷款金额
    payloadLoginRegister={'mobile':mobile,
                              'smsCode':"159603",
                              'actype':""
                              }
    payloadLoadStep3Profile={'mobile':mobile,
                                 'idCard':idCard,
                                 'provinceId':provinceId,
                                 'cityId':cityId,
                                 'address':address,
                                 'name':name
                                }
    s = requests.session()
    s.post(url + '/mp_server/loan/loginRegister', data=payloadLoginRegister)
    s.post(url + '/mp_server/loan/loanStep3Profile', data=payloadLoadStep3Profile)


    if loanType==2:#企业借款
        corporateName=fake.company()
        corporateCode=random.randrange(100000000000000,999999999999999)
        organizationCode=str(random.randrange(10000000,99999999))+chr(random.randrange(65,91))
        corporateHolder=fake.name()
        corporateIdCard=fake.ssn()
        payloadLoanStep3Corporate={'corporateContactMobile':mobile,
                                   'corporateName':corporateName,
                                   'corporateCode':corporateCode,
                                   'organizationCode':organizationCode,
                                   'corporateHolder':corporateHolder,
                                   'corporateIdCard':corporateIdCard,
                                   'corporateContactName':name,
                                   'provinceId':provinceId,
                                   'cityId':cityId,
                                   'address':address
                                   }
        r3=s.post(url+'/mp_server/loan/loanStep3Corporate', data=payloadLoanStep3Corporate)
        print r3.content
        id=int(eval(r3.content)['data'])#取上步返回的企业id
        payloadLoanStep4Amount={'loanType':2,
                                 'id':id,
                                 'amount':amount,
                                 'timelimit':timelimit
                                }

        r4=s.post(url+'/mp_server/loan/loanStep4Amount', data=payloadLoanStep4Amount).content

        if "贷款申请成功" in r4:
            print "名称：",corporateName,"id：",id,"联系人：",mobile,"总额：",amount,"万","期限：",timelimit,"个月的贷款申请成功"
        else:
            print r4

    #个人借款
    else:
        payloadLoanStep4Amount={'loanType':1,
                                 'amount':amount,#贷款金额
                                 'timelimit':timelimit#贷款期限
                                }
        r3 = s.post(url+'/mp_server/loan/loanStep4Amount', data=payloadLoanStep4Amount).content
        if "贷款申请成功" in r3:
            return "借款方：",name,"手机：",mobile,"身份证：",idCard,amount,"万",timelimit,"个月的贷款申请成功"
        else:
            return r3