# -*- coding: utf-8 -*-
import requests
import random
from faker import Factory
urlTest= "https://ot.nongfadai.com"#1
urlDev="http://omegadev.nongfadai.com"#2
urlInt="https://omegaint.nongfadai.com"#3
urlPre="http://omegapre.nongfadai.com"#4
fake=Factory.create('zh_CN')
mobile=fake.phone_number()
idCard=fake.ssn()
address=fake.address()
provinceId=44
cityId=4403
name=fake.name()
id=-1
timelimit=random.randrange(1,25)
amount=random.randrange(1,350)
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



#定义企业借款函数
def corporateLoan():
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
    id=int(eval(r3.content)['data'])#取上步返回的企业id
    payloadLoanStep4Amount={'loanType':2,
                             'id':id,
                             'amount':amount,
                             'timelimit':timelimit
                            }



    r4=s.post(url+'/mp_server/loan/loanStep4Amount', data=payloadLoanStep4Amount).content

    if "贷款申请成功" in r4:
        print "名称：",corporateName,"id：",id,"总额：",amount,"万","期限：",timelimit,"个月的贷款申请成功"
    else:
        print "贷款申请失败！请检查网络或联系研发二部测试"



#定义个人借款
def personalLoan():
    payloadLoanStep4Amount={'loanType':1,
                             'id':id,
                             'amount':amount,
                             'timelimit':timelimit
                            }
    r3 = s.post(url+'/mp_server/loan/loanStep4Amount', data=payloadLoanStep4Amount).content
    if "贷款申请成功" in r3:
        print "姓名：",name,"手机：",mobile,"身份证：",idCard,amount,"万",timelimit,"个月的贷款申请成功"
    else:
        print "贷款申请失败！请检查网络或联系研发二部测试"




if __name__ == '__main__':
    env=input("环境？1测试，2开发，3体验，4预发布")
    url=[urlTest,urlDev,urlInt,urlPre][env-1]
    loadType=input("借款主体？1个人，2企业")
    s = requests.session()
    r1 = s.post(url+'/mp_server/loan/loginRegister', data=payloadLoginRegister)
    r2 = s.post(url+'/mp_server/loan/loanStep3Profile', data=payloadLoadStep3Profile)
    if loadType==2:
        corporateLoan()
    else:
        personalLoan()