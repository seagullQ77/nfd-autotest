from faker import Faker


faker0 = Faker("zh_CN")
print(faker0.name(),faker0.ssn(),faker0.phone_number(),faker0.credit_card_number())


