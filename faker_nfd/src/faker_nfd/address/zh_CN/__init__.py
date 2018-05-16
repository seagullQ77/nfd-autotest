from faker.providers.address.zh_CN import Provider as FackerProvider
import json
from .nfd_districtData import districtData

class Provider(FackerProvider):

    def __init__(self, generator):
        super(Provider, self).__init__(generator)

        self.districtData_json = json.loads(districtData)


    def nfd_province(self):
        provice = self.random_element(self.districtData_json)
        return provice['label']

    def nfd_provinceId(self):
        provice = self.random_element(self.districtData_json)
        return provice['value']

    def nfd_city(self):
        provice = self.random_element(self.districtData_json)
        city = self.random_element(provice['children'])
        return city['label']

    def nfd_cityId(self):
        provice = self.random_element(self.districtData_json)
        city = self.random_element(provice['children'])
        return city['value']

    def nfd_county(self):
        provice = self.random_element(self.districtData_json)
        city = self.random_element(provice['children'])
        county = self.random_element(city['children'])
        return county['label']

    def nfd_countyId(self):
        provice = self.random_element(self.districtData_json)
        city = self.random_element(provice['children'])
        county = self.random_element(city['children'])
        return county['value']

    def nfd_address(self):
        provice = self.random_element(self.districtData_json)
        city = self.random_element(provice['children'])
        county = self.random_element(city['children'])
        return provice['label'],provice['value'],city['label'],city['value'],county['label'],county['value']