
from JiaseLibrary.utils.http import check_json_response


class _MpSysKeywords():

    def login_with_sms(self, username, smsCode, captchaCode = None):
        url = "%s/login" % self.interface_url
        load = {
            "username": username,
            "smsCode": smsCode,
            "captchaCode" : captchaCode
        }
        resp = self.session.post(url, json = load)
        ret = check_json_response(resp)
        return ret['data']['registered'], ret['data']['passwordReset']

    def submit_register(self, mobile):
        name = self._faker.name()
        idCardNo =  self._faker.person_id()
        provinceId = 111
        cityId = 111
        countyId = 111
        registerArea = self._faker.city()
        address = self._faker.street_address()
        url = "%s/custInfo/register/submitRegister" % self.interface_url
        print(url)
        load = {
            "name": name,
            "idCardNo": idCardNo,
            "provinceId": provinceId,
            "cityId": cityId,
            "countyId": countyId,
            "registerArea": registerArea,
            "address": address,
            "mobile": mobile,
            "createChannel":60
        }
        resp = self.session.post(url, json = load)
        ret = check_json_response(resp)


    def logout(self):
        url = "%s/logout" % self.interface_url
        load = {
        }
        headers = self.session.headers.copy()
        headers['Content-Type'] = "application/x-www-form-urlencoded"
        resp = self.session.post(url, data = load, headers = headers)
        ret = check_json_response(resp)


    def update_password(self, newPassword):
        url = "%s/update-password" % self.interface_url
        load = {
            "newPassword": newPassword,
        }
        headers = self.session.headers.copy()
        headers['Content-Type'] = "application/x-www-form-urlencoded"
        resp = self.session.post(url, data = load, headers = headers)
        ret = check_json_response(resp)
        aaa = 1



