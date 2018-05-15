from faker import Faker

from faker_nfd import NfdCompanyProvider
from faker_nfd import NfdCreditCardProvide
from faker_nfd import NfdDatatimeProvider
from faker_nfd import NfdLoremProvider
from faker_nfd import NfdPersonProvider

fake = Faker("zh_cn")

fake.add_provider(NfdCompanyProvider)
fake.add_provider(NfdCreditCardProvide)
fake.add_provider(NfdDatatimeProvider)
fake.add_provider(NfdLoremProvider)
fake.add_provider(NfdPersonProvider)



print("姓名: " + fake.name_wuxia())
print("身份证: " + fake.person_id())
print("手机: " + fake.phone_number())
print("银行卡: " + fake.credit_card_number())
print("地址: " + fake.address())

print(fake.crops())
print(fake.date_today_next())
print (fake.company())
print(fake.corporate_code())
print(fake.organization_code())

aaa = 1