from math import log
import pytest
import allure
from WEB.page.web_login_page import WebLoginPage
from WEB.page.web_kanban_master_page import WebKanbanMasterPage
from common.readconfig import con
import time
from common.logger import Logger


@allure.feature("web_kanban_master")
@pytest.mark.web
@pytest.mark.web_kanban_master
class TestWebKanbanMaster:
    @pytest.fixture(scope='function', autouse=True)
    def open_url(self, web_driver):
        login_page = WebLoginPage(web_driver)
        login_page.get_url(con.get("ENV", "HOST"))
        time.sleep(5)
        login_page.admin_login()
        login_page.open_function_page()
        time.sleep(5)
        login_page.enter_sub_page(5)
        time.sleep(5)

    @allure.story("web_kanban_master")
    def test_shuttle_kanban(self, web_driver):
        kanban_master_page = WebKanbanMasterPage(web_driver)
        kanban_master_page.input_org_id("流山")
        kanban_master_page.click_shuttle_tab()
        time.sleep(5)
        kanban_master_page.click_shuttle_add_button()
        kanban_master_page.input_shuttle_depot("芝","add-1")
        kanban_master_page.input_shuttle_op_type("shuttle","add-1")
        kanban_master_page.input_shuttle_remark1("test","add-1")
        kanban_master_page.input_shuttle_end_location("test","add-1")
        kanban_master_page.input_shuttle_post_no("test","add-1")
        time.sleep(5)
        kanban_master_page.input_shuttle_remark2_1("B","add-1")
        time.sleep(5)
        kanban_master_page.input_shuttle_remark2_2("B-test","add-1")
        time.sleep(5)
        kanban_master_page.input_shuttle_extra("B-test","add-1")
        time.sleep(5)
        kanban_master_page.input_shuttle_sort_no_1("B","add-1")
        time.sleep(5)
        kanban_master_page.input_shuttle_cloud("N","add-1")
        time.sleep(5)
        kanban_master_page.input_shuttle_sheet("1","add-1")
        time.sleep(5)
        kanban_master_page.click_save()
        time.sleep(5)
        kanban_master_page.popup_action(True)
        time.sleep(5)
        
        kanban_master_page.input_op_type("shuttle")
        kanban_master_page.input_depot("芝")
        kanban_master_page.click_search()
        time.sleep(10)
        #ky
        kanban_master_page.click_kyokuchokuso_tab()
        kanban_master_page.click_kyokuchokuso_delete_icon("15")
        kanban_master_page.click_save()
        kanban_master_page.popup_action(True)

        time.sleep(5)
        kanban_master_page.click_kyokuchokuso_add_button()
        kanban_master_page.input_kyokuchokuso_sort_no_1("test","add-1")
        kanban_master_page.input_kyokuchokuso_depot("芝","add-1")
        kanban_master_page.input_kyokuchokuso_TLName("test","add-1")
        kanban_master_page.input_kyokuchokuso_route("test","add-1")
        kanban_master_page.input_kyokuchokuso_startingTime("11:00","add-1")
        kanban_master_page.input_kyokuchokuso_remark("test","add-1")
        kanban_master_page.input_kyokuchokuso_sheet("2","add-1")
        kanban_master_page.click_save()
        kanban_master_page.popup_action(True)
        time.sleep(5)
        
        assert 1 == 1

