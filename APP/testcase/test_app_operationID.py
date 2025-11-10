import pytest
import allure
from APP.page.app_operationID_page import OperationIDPage
from APP.page.app_login_page import LoginPage
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from common.readconfig import con
from common.logger import Logger


@allure.feature("app_operationID")
@pytest.mark.app
@pytest.mark.app_operationID
class TestAppOperationID:

    @pytest.fixture(scope='session', autouse=True)
    def open_login(self, app_driver):
        """Launch the App and initialize LoginPage."""
        login_page = LoginPage(app_driver)
        try:
            login_page.agree_permission()
        except (NoSuchElementException, TimeoutException):
            pass
        login_page.login_07_driver()
        try:
            login_page.ongoing_tl()
        except (NoSuchElementException, TimeoutException):
            pass

    @allure.story("app_operationID")
    def test_regular_current_date(self, app_driver, open_login):
        """Test admin login and logout functionality."""
        op_page = OperationIDPage(app_driver)
        op_page.select_date()
        op_page.input_trunkline_id("25R07060510102923")
        name = op_page.get_course_trunk_name()
        assert 'Regular' in name

    @allure.story("app_operationID")
    def test_regular_future_date(self, app_driver):
        """Test admin login and logout functionality."""
        op_page = OperationIDPage(app_driver)
        op_page.select_date("2025/08/08")
        op_page.input_trunkline_id("25R07060510102923")
        name = op_page.get_course_trunk_name()
        assert "Regular" in name

    @allure.story("app_operationID")
    def test_regular_passed_date(self, app_driver):
        """Test admin login and logout functionality."""
        op_page = OperationIDPage(app_driver)
        op_page.select_date("2025/07/01")
        op_page.input_trunkline_id("25R07060510102923")
        msg = op_page.get_complete_msg()
        assert "complete" in msg
        try:
            op_page.close_complete_popup()
        except (NoSuchElementException, TimeoutException):
            pass



    @allure.story("app_operationID")
    def test_trunk_not_exist(self, app_driver):
        """Test admin login and logout functionality."""
        op_page = OperationIDPage(app_driver)
        op_page.select_date()
        op_page.input_trunkline_id("25R07060510102924")
        error_msg = op_page.get_error_msg()
        assert "not exist" in error_msg
        try:
            op_page.close_not_exist_error()
        except (NoSuchElementException, TimeoutException):
            pass
