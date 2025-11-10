import pytest
import allure
from WEB.page.web_login_page import WebLoginPage
from common.readconfig import con
import time
from common.logger import Logger


@allure.feature("web_login")
@pytest.mark.web
@pytest.mark.web_login
class TestWebLogin:
    @pytest.fixture(scope='class', autouse=True)
    def open_url(self, web_driver):
        login_page = WebLoginPage(web_driver)
        login_page.get_url(con.get("ENV", "HOST"))
        login_page.wait_loading_icon_disappear()
        login_page.wait_page_load_complete()
        yield

    @pytest.fixture(scope='function', autouse=True)
    def refresh_url(self, web_driver):
        yield
        login_page = WebLoginPage(web_driver)
        login_page.refresh()

    @allure.story("web_login")
    def test_01_login_without_org(self,web_driver):
        login_page = WebLoginPage(web_driver)
        login_page.input_user(con.get("ACCOUNT", "ADMIN_USER"))
        login_page.input_password(con.get("ACCOUNT", "ADMIN_PD"))
        login_page.click_login_button()
        assert login_page.get_error_when_missing_org() in ('Organization ID is required.','組織ID は必須項目です。')
        assert login_page.get_title() == 'TiDi - Portal Site'

    @allure.story("web_login")
    def test_02_login_without_username(self,web_driver):
        login_page = WebLoginPage(web_driver)
        login_page.input_organization(con.get("ACCOUNT", "ADMIN_GRP"))
        login_page.input_password(con.get("ACCOUNT", "ADMIN_PD"))
        login_page.click_login_button()
        assert login_page.get_error_when_missing_username() in ('User ID is required.','ユーザーID は必須項目です。')
        assert login_page.get_title() == 'TiDi - Portal Site'

    @allure.story("web_login")
    def test_03_login_without_pwd(self,web_driver):
        login_page = WebLoginPage(web_driver)
        login_page.input_organization(con.get("ACCOUNT", "ADMIN_GRP"))
        login_page.input_user(con.get("ACCOUNT", "ADMIN_USER"))
        login_page.click_login_button()
        assert login_page.get_error_when_missing_pwd() in ('Password is required.','パスワード は必須項目です。')
        assert login_page.get_title() == 'TiDi - Portal Site'

    @allure.story("web_login")
    def test_04_user_pwd_mismatch(self,web_driver):
        login_page = WebLoginPage(web_driver)
        login_page.input_organization(con.get("ACCOUNT", "ADMIN_GRP"))
        login_page.input_user(con.get("ACCOUNT", "ADMIN_USER"))
        login_page.input_password('####')
        login_page.click_login_button()
        assert 'GW1004' in login_page.get_error_wrong_pwd()
        assert login_page.get_title() == 'TiDi - Portal Site'
    

    @allure.story("web_login")
    def test_05_admin_login_logout(self, web_driver):
        login_page = WebLoginPage(web_driver)
        login_page.admin_login()
        assert login_page.menu_card_exist() is True
        login_page.logout()

    @allure.story("web_login")
    def test_06_jprl_login_logout(self, web_driver):
        login_page = WebLoginPage(web_driver)
        login_page.jprl_login()
        assert login_page.menu_card_exist() is True
        login_page.logout()

    @allure.story("web_login")
    def test_07_warehouse_manager_login_logout(self, web_driver):
        login_page = WebLoginPage(web_driver)
        login_page.org07mgr_login()
        assert login_page.menu_card_exist() is True
        login_page.logout()

    @allure.story("web_login")
    def test_08_carrier_manager_login_logout(self,web_driver):
        login_page = WebLoginPage(web_driver)
        login_page.carrier_login()
        assert login_page.menu_card_exist() is True
        login_page.logout()

    @allure.story("web_login")
    def test_09_driver_login(self,web_driver):
        login_page = WebLoginPage(web_driver)
        login_page.driver_login()
        assert 'PT9015' in login_page.get_error_wrong_pwd()
        assert login_page.get_title() == 'TiDi - Portal Site'

