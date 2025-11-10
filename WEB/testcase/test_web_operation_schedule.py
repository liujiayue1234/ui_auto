import pytest
import allure
from WEB.page.web_login_page import WebLoginPage
from WEB.page.web_operation_schedule_page import WebOperationSchedulePage
from WEB.page.web_trunk_overview_page import WebTrunkOverviewPage
from common.data_construction import DataConstruction
from common.readconfig import con
from common.logger import Logger


@allure.feature("web_operation_schedule")
@pytest.mark.web
@pytest.mark.web_operation_schedule
class TestWebOperationSchedule:
    @pytest.fixture(scope='class', autouse=True)
    def user_login(self, web_driver):
        login_page = WebLoginPage(web_driver)
        login_page.get_url(con.get("ENV", "HOST"))
        login_page.admin_login()
        login_page.open_function_page()
        login_page.enter_sub_page(3)
        yield

    @pytest.fixture(scope='function', autouse=True)
    def refresh_url(self, web_driver):
        yield
        login_page = WebLoginPage(web_driver)
        login_page.refresh()

    @allure.story("web_operation_schedule_search")
    def test_73_search_by_org_type_course(self, web_driver):
        schedule_page = WebOperationSchedulePage(web_driver)
        schedule_page.input_org_id("流山")
        schedule_page.input_trunk_type(1)
        trunk_name = 'at@TO_re'
        schedule_page.input_course_name(trunk_name)
        schedule_page.click_search()
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name)
        assert schedule_page.trunk_line_exist(trunk_id) is True

    @allure.story("web_operation_schedule_search")
    def test_74_search_by_all_conditions(self, web_driver):
        schedule_page = WebOperationSchedulePage(web_driver)
        schedule_page.input_org_id("流山")
        trunk_name = 'at@TO_ir'
        schedule_page.input_trunk_type(2)
        schedule_page.input_location("晴海")
        schedule_page.input_op_pattern([1,1,1,1])
        schedule_page.input_carrier("日本")
        schedule_page.input_contract_status([1,1,1])
        schedule_page.input_course_name(trunk_name)
        current = schedule_page.get_date_with_offset()
        schedule_page.input_month(current)
        schedule_page.click_search()
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name)
        assert schedule_page.trunk_line_exist(trunk_id) is True

    @allure.story("web_operation_schedule_update")
    def test_75_schedule_update_one_date_one_trunk(self, web_driver):
        schedule_page = WebOperationSchedulePage(web_driver)
        schedule_page.input_org_id("流山")
        schedule_page.input_course_name('at@TO')
        target_month = schedule_page.get_date_with_offset('', 31)
        schedule_page.input_month(target_month)
        schedule_page.click_search()
        trunk_name = 'at@TO_ir'
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name)
        target_date = str(schedule_page.get_date_with_offset('-', 31))[:7] + str("-03")  # 2025-10
        schedule_page.check_one_date_of_one_trunk(trunk_id, target_date)
        schedule_page.click_save()
        schedule_page.popup_action(True)
        assert schedule_page.checked_status_one_date_one_trunk(trunk_id, target_date) is False
        schedule_page.check_one_date_of_one_trunk(trunk_id, target_date)
        schedule_page.click_save()
        schedule_page.popup_action(True)
        assert schedule_page.checked_status_one_date_one_trunk(trunk_id, target_date) is True
    @allure.story("web_operation_schedule_update")
    def test_76_schedule_update_one_month_one_trunk(self, web_driver):
        schedule_page = WebOperationSchedulePage(web_driver)
        schedule_page.input_org_id("流山")
        schedule_page.input_course_name('at@TO')
        target_month = schedule_page.get_date_with_offset('',31)
        schedule_page.input_month(target_month)
        schedule_page.click_search()
        trunk_name ='at@TO_re'
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name)
        schedule_page.check_one_month_of_one_trunk(trunk_id)
        schedule_page.click_save()
        schedule_page.popup_action(True)
        assert schedule_page.checked_status_one_month_one_trunk(trunk_id) is False
        schedule_page.check_one_month_of_one_trunk(trunk_id)
        schedule_page.click_save()
        schedule_page.popup_action(True)
        assert schedule_page.checked_status_one_month_one_trunk(trunk_id) is True



    @allure.story("web_operation_schedule_update")
    def test_77_schedule_update_one_date_all_trunk(self, web_driver):
        schedule_page = WebOperationSchedulePage(web_driver)
        schedule_page.input_org_id("流山")
        schedule_page.input_course_name('at@TO')
        target_month = schedule_page.get_date_with_offset('', 31)
        schedule_page.input_month(target_month)
        schedule_page.click_search()
        schedule_page.check_one_date_of_all_trunk(5)
        schedule_page.click_save()
        schedule_page.popup_action(True)
        assert schedule_page.checked_status_one_date_all_trunk(5) is False
        schedule_page.check_one_date_of_all_trunk(5)
        schedule_page.click_save()
        schedule_page.popup_action(True)
        assert schedule_page.checked_status_one_date_all_trunk(5) is True

    @allure.story("web_operation_schedule_update")
    def test_78_schedule_update_all_date_all_trunk(self, web_driver):
        schedule_page = WebOperationSchedulePage(web_driver)
        schedule_page.input_org_id("流山")

        schedule_page.input_course_name('at@TO')
        target_month = schedule_page.get_date_with_offset('', 31)
        schedule_page.input_month(target_month)
        schedule_page.click_search()

        schedule_page.check_all_date_of_all_trunk()
        schedule_page.click_save()
        schedule_page.popup_action(True)
        assert schedule_page.checked_status_all_date_all_trunk() is False
        schedule_page.check_all_date_of_all_trunk()
        schedule_page.click_save()
        schedule_page.popup_action(True)
        assert schedule_page.checked_status_all_date_all_trunk() is True

    @allure.story("web_operation_schedule_detail")
    def test_79_trunk_detail(self, web_driver):
        schedule_page = WebOperationSchedulePage(web_driver)
        trunk_name = 'at@TO_re'
        schedule_page.input_org_id("流山")
        schedule_page.input_course_name(trunk_name)
        schedule_page.click_search()
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name)
        schedule_page.click_trunk_name_enter_detail(trunk_id)

        trunk_detail_page = WebTrunkOverviewPage(web_driver)
        assert trunk_detail_page.get_detail_trunk_id() == trunk_id
        assert trunk_detail_page.get_detail_trunk_type() in ('Regular','定期便')
        assert "流山" in trunk_detail_page.get_detail_org_id()
        assert trunk_detail_page.get_detail_trunk_name() == trunk_name
        assert trunk_detail_page.get_detail_course_name() == trunk_name
        assert trunk_detail_page.get_detail_op_pattern() in ('Every day','毎日')
        assert trunk_detail_page.get_detail_vh_type() == '2t'
        trunk_detail_page.click_detail_back_button()
    @allure.story("web_operation_schedule_edit")
    def test_80_update_end_date(self, web_driver):
        schedule_page = WebOperationSchedulePage(web_driver)
        trunk_name = 'at@TO_re'
        schedule_page.input_org_id("流山")
        schedule_page.input_course_name(trunk_name)
        schedule_page.click_search()
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name)
        schedule_page.click_trunk_name_enter_detail(trunk_id)

        trunk_detail_page = WebTrunkOverviewPage(web_driver)
        trunk_detail_page.click_detail_edit_button()
        current_date = trunk_detail_page.get_date_with_offset()
        trunk_detail_page.input_edit_con_end(current_date)
        trunk_detail_page.click_edit_save_button()
        trunk_detail_page.proceed_to_popup(True)
        assert trunk_detail_page.get_detail_trunk_id() == trunk_id
        assert trunk_detail_page.get_detail_con_end() == trunk_detail_page.get_date_with_offset("/")
        trunk_detail_page.click_detail_edit_button()
        future_date = '20550101'
        trunk_detail_page.input_edit_con_end(future_date)
        trunk_detail_page.click_edit_save_button()
        trunk_detail_page.proceed_to_popup(True)
        assert trunk_detail_page.get_detail_trunk_id() == trunk_id
        assert trunk_detail_page.get_detail_con_end() == '2055/01/01'
        trunk_detail_page.click_detail_back_button()

    @allure.story("web_operation_schedule_copy_register")
    def test_81_copy_active_regular_failure(self, web_driver):
        schedule_page = WebOperationSchedulePage(web_driver)
        trunk_name = 'at@TO_re'
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name)
        schedule_page.input_org_id("流山")
        schedule_page.input_course_name(trunk_name)
        schedule_page.click_search()
        schedule_page.click_trunk_name_enter_detail(trunk_id)

        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_page.click_detail_copy_register_button()
        trunk_page.click_register_button()
        trunk_page.proceed_to_popup(True)
        assert trunk_page.get_register_start_date_error() in (
        'Please input date at least 1 day in the future.', '1日後以降の日付を入力してください。')
        trunk_page.click_register_back_button()
        trunk_page.click_detail_back_button()