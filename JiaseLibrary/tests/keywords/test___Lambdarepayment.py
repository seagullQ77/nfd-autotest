
import JiaseLibrary
from JiaseLibrary import JiaseLibrary


class Test__Lambdarepayment():
    def test__create_repayment_apply(self):
        # 登录
        jiase = JiaseLibrary()
        jiase.login_lambda(role = 'lambda_repay_match',usr='18233333333',psd='150315')
        jiase._create_repayment_apply("IOU2017112300002", "218", "JKF")


        self.fail()

    def test__save_repayment_apply(self):
        self.fail()

    def test_submit_repayment_apply(self):
        self.fail()

    def test_repayment_apply_aduit_pass(self):
        self.fail()

    def test_repayment_apply_aduit_reject(self):
        self.fail()

    def test_repayment_apply_aduit_back(self):
        self.fail()

    def test_repayment_apply_aduit_cancel(self):
        self.fail()

    def test_repayment_apply_aduit_retreat(self):
        self.fail()

    def test__create_prepay_apply(self):
        self.fail()

    def test__save_prepay_apply(self):
        self.fail()

    def test_submit_prepay_apply(self):
        self.fail()

    def test_prepay_apply_aduit_pass(self):
        self.fail()

    def test_prepay_apply_aduit_reject(self):
        self.fail()

    def test_prepay_apply_aduit_back(self):
        self.fail()

    def test_prepay_apply_aduit_cancel(self):
        self.fail()

    def test_prepay_apply_aduit_retreat(self):
        self.fail()
