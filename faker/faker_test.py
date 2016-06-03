# coding=utf-8
VERSION = '0.5.7'

from faker.factory import Factory

myfaker = Factory.create(locale='zh_CN')
#print myfaker.person_id()
#print myfaker.phone_number()
#print myfaker.crops()
#print myfaker.name_wuxia()
#print myfaker.date_today_before()
list = myfaker.province_city_name()
for it in list:
    print it
