from robot.api import logger

from JiaseLibrary.utils.http import check_json_response


class _SysKeywords():

    def submit_register(self, name, idCardNo, provinceId, cityId, countyId, registerArea, address, mobile):
        url = "%s/custInfo/register/submitRegister" % self.interface_url
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



