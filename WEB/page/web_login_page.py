import time
from common.logger import Logger
from common.readconfig import con
from WEB.base.basepage import Basepage
from common.readelement import Element
from config.config import WEB_ELEMENT_PATH

search = Element(WEB_ELEMENT_PATH, 'web_login_element')


class WebLoginPage(Basepage):
    def input_organization(self, value):
        self.send_key(search['organizationIdInput'], value)

    def input_user(self, value):
        self.send_key(search['userIdInput'], value)

    def input_password(self, value):
        self.send_key(search['passwordInput'], value)

    def click_login_button(self):
        self.click(search['loginButton'])

    def admin_login(self):
        self.input_organization(con.get("ACCOUNT", "ADMIN_GRP"))
        self.input_user(con.get("ACCOUNT", "ADMIN_USER"))
        self.input_password(con.get("ACCOUNT", "ADMIN_PD"))
        self.click_login_button()

    def jprl_login(self):
        self.input_organization(con.get("ACCOUNT", "JPRL_GRP"))
        self.input_user(con.get("ACCOUNT", "JPRL_USER"))
        self.input_password(con.get("ACCOUNT", "JPRL_PD"))
        self.click_login_button()

    def org07mgr_login(self):
        self.input_organization(con.get("ACCOUNT", "ORG7_GRP"))
        self.input_user(con.get("ACCOUNT", "ORG7_USER"))
        self.input_password(con.get("ACCOUNT", "ORG7_PD"))
        self.click_login_button()

    def carrier_login(self):
        self.input_organization(con.get("ACCOUNT", "CA71_GRP"))
        self.input_user(con.get("ACCOUNT", "CA71_USER"))
        self.input_password(con.get("ACCOUNT", "CA71_PD"))
        self.click_login_button()

    def driver_login(self):
        self.input_organization(con.get("ACCOUNT", "DR7_GRP"))
        self.input_user(con.get("ACCOUNT", "DR7_USER"))
        self.input_password(con.get("ACCOUNT", "DR7_PD"))
        self.click_login_button()

    def get_error_when_missing_org(self):
        return self.get_text(search["OrgMissError"])

    def get_error_when_missing_username(self):
        return self.get_text(search["userMissError"])

    def get_error_when_missing_pwd(self):
        return self.get_text(search["pwdMissError"])

    def get_error_wrong_pwd(self):
        return self.get_text(search["wrongPwdError"])

    def menu_card_exist(self):
        self.wait_loading_icon_disappear()
        try:
            return self.check_element_exist(search["ManuCard"],None,2)
        except Exception as e:
            return False

    def click_menu_card(self):
        self.click(search['ManuCard'])

    def open_function_page(self, close_current=True):
        self.click_menu_card()
        self.enter_into_new_page(close_current=True)


if __name__ == '__main__':
    pass
