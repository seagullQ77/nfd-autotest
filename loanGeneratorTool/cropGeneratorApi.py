# -*- coding: utf-8 -*-
#产生富农贷
import random
import requests
from faker import Factory
import provinceChoice
def loanGenerate(GuarantorId,env,education=1,isMarried=1,contactType=1):#1测试2联调3体验4预发布；1~3,高中，大专，大学；1-5，老婆，子女，父母，朋友，其他
    urlTest= "https://ot.nongfadai.com"#1
    urlDev="https://omegadev.nongfadai.com"#2
    urlInt="https://omegaint.nongfadai.com"#3
    urlPre="https://omegapre.nongfadai.com"#4
    url = (urlTest, urlDev, urlInt, urlPre)[env - 1]
    fake=Factory.create('zh_CN')
    mobile=fake.phone_number()#手机号码
    #mobile=15252859069
    contactMobilePhone=fake.phone_number()
    idCard=fake.ssn()
    contactIdCardNo=fake.ssn()
    address=fake.address()
    [provinceId,cityId,countyId]= provinceChoice.pcList()
    name=fake.name()
    contactName=fake.name()
    loanPeriod=random.randrange(1,25)
    loanLimit=random.randrange(1,2000001)
    #loanLimit = 50000#贷款额度
    cardNo=fake.credit_card_number()
    payloadLoginRegister={'mobile':mobile,
                          'smsCode':"159603",
                          'actype':"crop"
                          }
    payloadLoanStep3Profile={'mobile':mobile,
                             'idCard':idCard,
                             'provinceId':provinceId,
                             'cityId':cityId,
                             'countyId':countyId,
                             'address':address,
                             'name':name
                            }
    s = requests.session()
    s.post(url + '/mp_server/loan/loginRegister', data=payloadLoginRegister)
    s.post(url + '/mp_server/loan/loanStep3Profile', data=payloadLoanStep3Profile)
    payloadUpdatePersonal={
            'education':education,#1~3,高中，大专，大学
            'isMarried':isMarried,#0,1
            'contactType':contactType,#1-5，老婆，子女，父母，朋友，其他
            'contactName':contactName,
            'contactIdCardNo':contactIdCardNo,
            'contactMobilePhone':contactMobilePhone,
            'loginMobilePhone':mobile
        }
    r1 = s.post(url + '/mp_server/loan/updatePersonal', data=payloadUpdatePersonal)
    payloadAddPersonalAsset={
            'assetCategory':random.randrange(1,4),
            'location':address,
            'currentValue':random.randrange(1,99999999999),
            'quantity':random.randrange(1,99999999999),
            'loginMobilePhone':mobile
        }
    r2=s.post(url+'/mp_server/loan/addPersonalAsset', data=payloadAddPersonalAsset).content

    payloadUpdateProdType={
            'loanType':random.randrange(1,3),
            'plantBreed':random.choice(['小麦','玉米','金色凤梨','美国黑布林']),
            'plantAreaSize':random.randrange(1,100),
            'landRent':random.randrange(1,100),
            'contractDuration':random.randrange(1,100),
            'bizLocAreaSize':random.randrange(1,100),
            'lastYearPurchaseAmount':random.randrange(1,100),
            'bizLocProp':random.choice(['RENT','OWN']),
            'monthlyRent':random.randrange(1,100),
            'loginMobilePhone':mobile
            }
    r3=s.post(url+'/mp_server/loan/updateProdType', data=payloadUpdateProdType).content
    #print r3

    payloadLoanSetp4Corp={
        'bankId':random.randrange(1,41),
        'beforeLastYearIncome':random.randrange(1,1000000),
        'cardNo':cardNo,
        'GuarantorId':GuarantorId,
        'isDelegation':random.choice([0,1]),
        'lastYearIncome':random.randrange(1,1000000),
        'loanLimit':loanLimit,
        'loanPeriod':loanPeriod,
        'loginMobilePhone':mobile,
        'operationDuration':random.randrange(1,100)
        }
    r4=s.post(url+'/mp_server/loan/loanSetp4Corp', data=payloadLoanSetp4Corp).content
    if "贷款申请成功" in r4:
        return "借款方：",name,"手机：",mobile,"身份证：",idCard,"金额：",loanLimit,"元的",loanPeriod,"个月富农贷申请成功"
    else:
        return r4
