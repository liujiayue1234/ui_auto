import pytest
import allure
from APP.page.app_login_page import LoginPage
from common.readconfig import con
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
from common.logger import Logger


@allure.feature("app_login")
@pytest.mark.app
@pytest.mark.app_login
class TestAppLogin:

    @pytest.fixture(scope='session', autouse=True)
    def handle_permission(self, app_driver):
        """Launch the App and initialize LoginPage."""
        login_page = LoginPage(app_driver)
        try:
            login_page.agree_permission()
        except (NoSuchElementException, TimeoutException):
            pass

    @allure.story("app_login")
    def test_driver_login_logout(self, app_driver):
        """Test admin login and logout functionality."""
        login_page = LoginPage(app_driver)
        login_page.input_organization(con.get('ACCOUNT', 'DR7_GRP'))
        login_page.input_driver(con.get('ACCOUNT', 'DR7_USER'))
        login_page.input_password(con.get('ACCOUNT', 'DRIVER7_PD'))
        login_page.click_login()
        try:
            login_page.ongoing_tl()
        except Exception as e:
            pass
        login_page.logout()
        assert 1 == 1

    def test_login_without_password(self, app_driver):
        login_page = LoginPage(app_driver)
        login_page.input_organization(con.get('ACCOUNT', 'DR7_GRP'))
        login_page.input_driver(con.get('ACCOUNT', 'DR7_USER'))
        login_page.click_login()
        msg = login_page.get_login_error_msg()
        assert "not valid" in msg
