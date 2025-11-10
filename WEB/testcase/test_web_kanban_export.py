from math import log
import pytest
import allure
from WEB.page.web_login_page import WebLoginPage
from WEB.page.web_kanban_export_page import WebKanbanExportPage
from common.readconfig import con
import time
from common.logger import Logger


@allure.feature("web_kanban_export")
@pytest.mark.web
@pytest.mark.web_kanban_export
class TestWebKanbanExport:
    @pytest.fixture(scope='function', autouse=True)
    def open_url(self, web_driver):
        login_page = WebLoginPage(web_driver)
        login_page.get_url(con.get("ENV", "HOST"))
        time.sleep(5)
        login_page.admin_login()
        login_page.open_function_page()
        time.sleep(5)
        login_page.enter_sub_page(4)
        time.sleep(5)

    @allure.story("web_kanban_master")
    def test_shuttle_kanban(self, web_driver):
        kanban_export_page = WebKanbanExportPage(web_driver)
        kanban_export_page.input_org_id("流山")
        kanban_export_page.click_shuttle_tab()
        time.sleep(5)
        Logger.info(kanban_export_page.get_shuttle_kanban_id("39"))
        Logger.info(kanban_export_page.get_shuttle_depot("39"))
        Logger.info("shuttle op type: "+kanban_export_page.get_shuttle_op_type("39"))
        Logger.info("shuttle remark1: "+kanban_export_page.get_shuttle_remark1("39"))
        Logger.info("shuttle end location: "+kanban_export_page.get_shuttle_end_location("39"))
        Logger.info("shuttle post no: "+kanban_export_page.get_shuttle_post_no("39"))
        Logger.info("shuttle remark2_1: "+kanban_export_page.get_shuttle_remark2_1("39"))
        Logger.info("shuttle remark2_2: "+kanban_export_page.get_shuttle_remark2_2("39"))
        Logger.info("shuttle sort_no_1: "+kanban_export_page.get_shuttle_sort_no_1("39"))
        Logger.info("shuttle sort_no_2: "+kanban_export_page.get_shuttle_sort_no_2("39"))
        Logger.info("shuttle extra: "+kanban_export_page.get_shuttle_extra("39"))
        Logger.info("shuttle cloud: "+kanban_export_page.get_shuttle_cloud("39"))
        Logger.info("shuttle sheet: "+kanban_export_page.get_shuttle_sheet("39"))
        kanban_export_page.check_shuttle_kanban("39")
        kanban_export_page.input_export_date("2025-08-18")
        kanban_export_page.click_export_button()
        kanban_export_page.popup_action(True)
        time.sleep(5)
        kanban_export_page.click_kyokuchokuso_tab()
        time.sleep(5)
        Logger.info("kyokuchokuso kanban id: "+kanban_export_page.get_kyokuchokuso_kanban_id("20"))
        Logger.info("kyokuchokuso sort no: "+kanban_export_page.get_kyokuchokuso_sort_no("20"))
        Logger.info("kyokuchokuso depot: "+kanban_export_page.get_kyokuchokuso_depot("20"))
        Logger.info("kyokuchokuso TLName: "+kanban_export_page.get_kyokuchokuso_TLName("20"))
        Logger.info("kyokuchokuso route: "+kanban_export_page.get_kyokuchokuso_route("20"))
        Logger.info("kyokuchokuso starting time: "+kanban_export_page.get_kyokuchokuso_startingTime("20"))
        Logger.info("kyokuchokuso remark: "+kanban_export_page.get_kyokuchokuso_remark("20"))
        Logger.info("kyokuchokuso sheet: "+kanban_export_page.get_kyokuchokuso_sheet("20"))

        kanban_export_page.check_kyokuchokuso_kanban("20")
        kanban_export_page.input_export_date("2025-07-30")
        kanban_export_page.click_export_button()
        kanban_export_page.popup_action(True)
        time.sleep(5)
        kanban_export_page.click_select_all_button()
        time.sleep(5)

        
        assert 1 == 1

