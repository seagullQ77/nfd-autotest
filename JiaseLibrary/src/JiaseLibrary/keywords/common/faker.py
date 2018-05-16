from faker import Faker
from faker_nfd import NfdCompanyProvider
from faker_nfd import NfdCreditCardProvide
from faker_nfd import NfdDatatimeProvider
from faker_nfd import NfdLoremProvider
from faker_nfd import NfdPersonProvider
from faker_nfd import NfdAddressProvider

class FakerKeywords():
    def __init__(self):
        self.fake = Faker("zh_cn")
        self.fake.add_provider(NfdCompanyProvider)
        self.fake.add_provider(NfdCreditCardProvide)
        self.fake.add_provider(NfdDatatimeProvider)
        self.fake.add_provider(NfdLoremProvider)
        self.fake.add_provider(NfdPersonProvider)
        self.fake.add_provider(NfdAddressProvider)


    def get_person_name(self):
        """
        获取一个随机的人名
        :return:
        """
        return self.fake.name_wuxia()

    def get_person_id(self):
        """
        获取一个符合规则的身份证号
        :return:
        """
        return self.fake.person_id()

    def get_mobile_number(self):
        """
        获取一个手机号
        :return:
        """
        return self.fake.phone_number()

    def get_bank_card_number(self):
        """
        获取一个符合规则的银行卡号
        :return:
        """
        return self.fake.credit_card_number()

    def nfd_address(self):
        return self.fake.nfd_address()

    def street_address(self):
        return self.fake.street_address()

