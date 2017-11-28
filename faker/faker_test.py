# coding=utf-8
VERSION = '0.5.7'

from faker.factory import Factory

myfaker = Factory.create(locale='zh_CN')

print myfaker.person_id() #随机生成符合校验规则的身份证号
    
print myfaker.credit_card_number() #生成符合校验规则的银行卡号
print myfaker.name_wuxia()#随机生成一个武侠小说的名字
print myfaker.phone_number()#生成一个随机电话号码
# print myfaker.crops() #随机生成一种农作物

# print myfaker.date_today_before()#随机生成一个当前日期之前的日期
# print myfaker.mac_address()
print myfaker.company()#随机生成一个公司名称
# print myfaker.name()#随机生成一个姓名
# print myfaker.corporate_code() #随机生成一个企业营业执照号码
# print myfaker.organization_code()#随机生成一个符合校验规则的组织机构代码

# print myfaker.address() #随机生成一个地址
# print myfaker.text() #随机生成一段文本
# for i in range(5):
   # print myfaker.phone_number() 
