from faker import Faker


faker0 = Faker("zh_CN")
print(faker0.name(),faker0.ssn(),faker0.phone_number(),faker0.credit_card_number())

import time

t = (2009, 2, 17, 17, 3, 38, 1, 48, 0)
t = time.mktime(t)
print (time.strftime("%b %d %Y %H:%M:%S", time.gmtime(t)))