from common.readconfig import con
from APP.base.basepage import BasePage
from common.readelement import Element
from config.config import APP_ELEMENT_PATH
from common.logger import Logger

search = Element(APP_ELEMENT_PATH, 'android_app_login_element')


class LoginPage(BasePage):
    def __init__(self, driver):
        """Initialize LoginPage with Appium WebDriver."""
        super().__init__(driver)

    def agree_permission(self):
        self.click(search['policyCheck'])
        self.click(search['agreeButton'])
        self.click(search['systemAuth'])

    def ongoing_tl(self, continue_option=False):
        if continue_option:
            self.click(search['ongoingContinue'])
        else:
            self.click(search['ongoingNo'])

    def input_organization(self, value):
        self.send_key(search['organizationIdInput'], value)

    def input_driver(self, value):
        self.send_key(search['driverIdInput'], value)

    def input_password(self, value):
        self.send_key(search['passwordInput'], value)

    def click_login(self):
        self.click(search['loginButton'])

    def login_07_driver(self):
        self.input_organization(con.get("ACCOUNT", "DR7_GRP"))
        self.input_driver(con.get("ACCOUNT", "DR7_USER"))
        self.input_password(con.get("ACCOUNT", "DRIVER7_PD"))
        self.click_login()

    def get_login_error_msg(self):
        return self.get_text(search['errorMsg'])
