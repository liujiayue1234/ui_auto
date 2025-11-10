from sqlite3 import Date
from time import sleep
import pytest
import allure
from WEB.page.web_login_page import WebLoginPage
from WEB.page.web_arrival_page import WebArrivalPage
from WEB.page.web_trunk_overview_page import WebTrunkOverviewPage
from common.readconfig import con
import time
from common.logger import Logger
from common.data_construction import DataConstruction


@allure.feature("web_arrival")
@pytest.mark.web
@pytest.mark.web_arrival
class TestWebArrival:
    @pytest.fixture(scope='class', autouse=True)
    def user_login(self, web_driver):
        login_page = WebLoginPage(web_driver)
        login_page.get_url(con.get("ENV", "HOST"))
        login_page.admin_login()
        login_page.open_function_page()
        yield

    @pytest.fixture(scope='function', autouse=True)
    def refresh_url(self, web_driver):
        yield
        login_page = WebLoginPage(web_driver)
        login_page.refresh()

    @allure.story("web_arrival_search")
    def test_10_search_by_org_date_trunk(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        arrival_page.input_op_date("20350101")
        trunk_name = 'at@can_re'
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name=trunk_name)
        arrival_page.input_trunk_name(trunk_name)
        arrival_page.click_search()
        assert arrival_page.trunk_card_exist(trunk_id)

    @allure.story("web_arrival_search")
    def test_11_search_by_org_date_trunk_confirm_error(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        arrival_page.input_op_date("20350101")
        arrival_page.input_confirm_status(False)
        arrival_page.input_error_status([1,0,0])
        trunk_name = 'at@can_re'
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name=trunk_name)
        arrival_page.input_trunk_name(trunk_name)
        arrival_page.click_search()
        assert arrival_page.trunk_card_exist(trunk_id)

    @allure.story("web_arrival_search")
    def test_12_search_by_all_conditions(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        arrival_page.input_op_date("20350101")
        arrival_page.input_confirm_status(False)
        arrival_page.input_error_status([1, 0, 0])
        arrival_page.input_op_status([1,1,1])
        arrival_page.input_trunk_type(1)
        trunk_name = 'at@can_re'
        arrival_page.input_trunk_name(trunk_name)
        arrival_page.input_course_name(trunk_name)
        arrival_page.input_carrier('日本')
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name=trunk_name)
        arrival_page.click_search()
        assert arrival_page.trunk_card_exist(trunk_id)

    @allure.story("web_arrival_confirm")
    def test_13_confirm_one_trunk(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        arrival_page.input_op_date(arrival_page.get_date_with_offset())
        trunk_name = 'at@con_ir1'
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name=trunk_name)
        Logger.info("trunk id :"+str(trunk_id))
        DataConstruction.normal_shukko(trunk_id=trunk_id, operation_date=arrival_page.get_date_with_offset("-"))
        arrival_page.input_trunk_name(trunk_name)
        arrival_page.click_search()
        arrival_page.confirm_trunk_line(trunk_line_id=trunk_id)
        arrival_page.click_save()
        arrival_page.input_confirm_status(True)
        arrival_page.click_search()
        assert arrival_page.trunk_card_exist(trunk_id)

    @allure.story("web_arrival_confirm")
    # @pytest.mark.skip(reason="Already run , no data")
    def test_14_confirm_multiple_trunks(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        arrival_page.input_op_date(arrival_page.get_date_with_offset())
        arrival_page.input_trunk_name('at@con')
        #arrival_page.input_op_status([0,1,0])
        trunkname1 = 'at@con_ir2'
        trunkid1 = DataConstruction.get_trunk_id_by_name(trunk_name=trunkname1)
        DataConstruction.normal_shukko(trunk_id=trunkid1, operation_date=arrival_page.get_date_with_offset("-"))
        trunkname2 = 'at@con_re1'
        trunkid2 = DataConstruction.get_trunk_id_by_name(trunk_name=trunkname2)
        DataConstruction.normal_shukko(trunk_id=trunkid2, operation_date=arrival_page.get_date_with_offset("-"))
        trunkname3 = 'at@con_sr1'
        trunkid3 = DataConstruction.get_trunk_id_by_name(trunk_name=trunkname3)
        DataConstruction.shuttle_shukko(trunk_id=trunkid3, operation_date=arrival_page.get_date_with_offset("-"),cart=99)
        trunkname4 = 'at@con_si1'
        trunkid4 = DataConstruction.get_trunk_id_by_name(trunk_name=trunkname4)
        DataConstruction.shuttle_shukko(trunk_id=trunkid4, operation_date=arrival_page.get_date_with_offset("-"),cart=99)
        arrival_page.click_search()
        arrival_page.confirm_trunk_line(trunk_line_id=trunkid1)
        arrival_page.confirm_trunk_line(trunk_line_id=trunkid2)
        arrival_page.confirm_trunk_line(trunk_line_id=trunkid3)
        arrival_page.confirm_trunk_line(trunk_line_id=trunkid4)
        arrival_page.click_save()
        arrival_page.input_confirm_status(True)
        arrival_page.click_search()
        assert arrival_page.trunk_card_exist(trunkid1)
        assert arrival_page.trunk_card_exist(trunkid2)
        assert arrival_page.trunk_card_exist(trunkid3)
        assert arrival_page.trunk_card_exist(trunkid4)

    @allure.story("web_arrival_confirm")
    #@pytest.mark.skip(reason="Already run , no data")
    def test_15_confirm_by_select_all(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        arrival_page.input_op_date(arrival_page.get_date_with_offset())
        trunkname = 'at@con'
        arrival_page.input_trunk_name(trunkname)
        arrival_page.input_confirm_status(False)
        arrival_page.click_search()
        trunkname3 = 'at@con_ir3'
        trunkid3 = DataConstruction.get_trunk_id_by_name(trunk_name=trunkname3)
        DataConstruction.normal_shukko(trunk_id=trunkid3, operation_date=arrival_page.get_date_with_offset("-"))
        trunkname4 = 'at@con_ir4'
        trunkid4 = DataConstruction.get_trunk_id_by_name(trunk_name=trunkname4)
        DataConstruction.normal_shukko(trunk_id=trunkid4, operation_date=arrival_page.get_date_with_offset("-"))
        arrival_page.confirm_trunk_line()
        sleep(2)
        arrival_page.click_save()
        arrival_page.input_confirm_status(True)
        arrival_page.click_search()
        assert arrival_page.trunk_card_exist(trunkid3) is True
        assert arrival_page.trunk_card_exist(trunkid4) is True

    @allure.story("web_arrival_csv_export")
    def test_16_csv_export_past_date(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.csv_export(arrival_page.get_date_with_offset(offset=-1),
                                arrival_page.get_date_with_offset(offset=-1))
        trunkname = 'at@con_ir1'
        result = arrival_page.read_csv_file(arrival_page.get_date_with_offset(offset=-1), trunkname)
        Logger.info("RESULT"+str(result))
        assert trunkname in result[0][3]
        assert result[0][1] == arrival_page.get_date_with_offset(Delimiter="/", offset=-1)

    @allure.story("web_arrival_csv_export")
    def test_17_csv_export_current_date(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.csv_export(arrival_page.get_date_with_offset(offset=0),
                                arrival_page.get_date_with_offset(offset=0))
        trunkname = 'at@con_ir1'
        result = arrival_page.read_csv_file(arrival_page.get_date_with_offset(offset=0), trunkname)
        assert trunkname in result[0][3]
        assert result[0][1] == arrival_page.get_date_with_offset(Delimiter="/", offset=0)

    @allure.story("web_arrival_csv_export")
    def test_18_csv_export_future_date(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.csv_export(arrival_page.get_date_with_offset(offset=1),
                                arrival_page.get_date_with_offset(offset=1))
        trunkname = 'at@con_ir1'
        result = arrival_page.read_csv_file(arrival_page.get_date_with_offset(offset=1), trunkname)
        assert trunkname in result[0][3]
        assert result[0][1] == arrival_page.get_date_with_offset(Delimiter="/", offset=1)

    @allure.story("web_arrival_register_irregular")
    def test_19_register_irregular_default(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id('流山')
        arrival_page.open_register_irregular_page()
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_name = 'at@reg_1'
        trunk_page.input_register_course_name(trunk_name)
        trunk_page.input_register_trunk_name(trunk_name)
        trunk_page.input_register_carrier('日本')
        trunk_page.input_register_vehicle_type(1)
        trunk_page.input_register_comment("Registered by automation")
        trunk_page.input_register_irregular_reason(1)
        trunk_page.input_register_dp_location('流山')
        trunk_page.input_register_dp_plan_arrival_time("0000")
        trunk_page.input_register_dp_plan_departure_time("0030")
        trunk_page.input_register_ar_location('晴海', card_order=1)
        trunk_page.input_register_ar_plan_arrival_time("0100", card_order=1)
        trunk_page.click_register_button()
        trunk_page.proceed_to_popup(True)
        # search to verify the result
        arrival_page.input_course_name(trunk_name)
        arrival_page.click_search()
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name)
        assert arrival_page.trunk_card_exist(trunk_id) is True
        DataConstruction.delete_trunk(trunk_id)

    @allure.story("web_arrival_register_irregular")
    def test_20_register_irregular_modify(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id('流山')
        arrival_page.open_register_irregular_page()
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_name = 'at@reg_2'
        trunk_page.input_register_org_id('枚方')
        trunk_page.input_register_org_id('流山')
        trunk_page.input_register_trunk_type(2)
        trunk_page.input_register_course_name(trunk_name)
        trunk_page.input_register_trunk_name(trunk_name)
        trunk_page.input_register_op_pattern(3)
        trunk_page.input_register_carrier('日本')
        trunk_page.input_register_vehicle_type(1)
        trunk_page.input_register_comment("Registered by automation")
        trunk_page.input_register_irregular_reason(1)
        trunk_page.input_register_dp_location('流山')
        trunk_page.input_register_dp_plan_arrival_time("0000")
        trunk_page.input_register_dp_plan_departure_time("0030")
        trunk_page.input_register_ar_location('晴海', card_order=1)
        trunk_page.input_register_ar_plan_arrival_time("0100", card_order=1)
        trunk_page.click_register_button()
        trunk_page.proceed_to_popup(True)
        # search to verify the result
        arrival_page.input_course_name(trunk_name)
        arrival_page.click_search()
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name)
        assert arrival_page.trunk_card_exist(trunk_id) is True
        DataConstruction.delete_trunk(trunk_id)

    @allure.story("web_arrival_cancel_trunk_line")
    def test_21_cancel_regular_past_date(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        arrival_page.input_op_date(arrival_page.get_date_with_offset(offset=-1))
        trunkname = 'at@can_re'
        arrival_page.input_trunk_name(trunkname)
        arrival_page.click_search()
        trunk_id = DataConstruction.get_trunk_id_by_name(trunkname)
        arrival_page.cancel_trunk(trunk_id=trunk_id)
        assert arrival_page.check_cancel_button_enabled(trunk_id) is False

    @allure.story("web_arrival_cancel_trunk_line")
    def test_22_cancel_regular_current_date(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        arrival_page.input_op_date(arrival_page.get_date_with_offset(offset=0))
        trunkname = 'at@can_re1'
        arrival_page.input_trunk_name(trunkname)
        arrival_page.click_search()
        trunk_id = DataConstruction.get_trunk_id_by_name(trunkname)
        arrival_page.cancel_trunk(trunk_id=trunk_id)
        assert arrival_page.check_cancel_button_enabled(trunk_id) is False

    @allure.story("web_arrival_cancel_trunk_line")
    def test_23_cancel_regular_future_date(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        arrival_page.input_op_date(arrival_page.get_date_with_offset(offset=1))
        trunkname = 'at@can_re2'
        arrival_page.input_trunk_name(trunkname)
        arrival_page.click_search()
        trunk_id = DataConstruction.get_trunk_id_by_name(trunkname)
        assert arrival_page.check_cancel_button_enabled(trunk_id) is False

    @allure.story("web_arrival_cancel_trunk_line")
    def test_24_cancel_irregular_past_date(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        arrival_page.input_op_date(arrival_page.get_date_with_offset(offset=-1))
        trunkname = 'at@can_ir'
        arrival_page.input_trunk_name(trunkname)
        arrival_page.click_search()
        trunk_id = DataConstruction.get_trunk_id_by_name(trunkname)
        arrival_page.cancel_trunk(trunk_id=trunk_id)
        assert arrival_page.check_cancel_button_enabled(trunk_id) is False

    @allure.story("web_arrival_cancel_trunk_line")
    def test_25_cancel_regular_current_date(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        arrival_page.input_op_date(arrival_page.get_date_with_offset(offset=0))
        trunkname = 'at@can_ir1'
        arrival_page.input_trunk_name(trunkname)
        arrival_page.click_search()
        trunk_id = DataConstruction.get_trunk_id_by_name(trunkname)
        arrival_page.cancel_trunk(trunk_id=trunk_id)
        assert arrival_page.check_cancel_button_enabled(trunk_id) is False

    @allure.story("web_arrival_cancel_trunk_line")
    def test_26_cancel_regular_future_date(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        arrival_page.input_op_date(arrival_page.get_date_with_offset(offset=1))
        trunkname = 'at@can_ir2'
        arrival_page.input_trunk_name(trunkname)
        arrival_page.click_search()
        trunk_id = DataConstruction.get_trunk_id_by_name(trunkname)
        assert arrival_page.check_cancel_button_enabled(trunk_id) is False


    @allure.story("web_arrival_cancel_trunk_line")
    def test_27_cancel_shuttle_regular_past_date(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        arrival_page.input_op_date(arrival_page.get_date_with_offset(offset=-1))
        trunkname = 'at@can_sr'
        arrival_page.input_trunk_name(trunkname)
        arrival_page.click_search()
        trunk_id = DataConstruction.get_trunk_id_by_name(trunkname)
        arrival_page.cancel_trunk(trunk_id=trunk_id)
        assert arrival_page.check_cancel_button_enabled(trunk_id) is False

    @allure.story("web_arrival_cancel_trunk_line")
    def test_28_cancel_shuttle_regular_current_date(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        arrival_page.input_op_date(arrival_page.get_date_with_offset(offset=0))
        trunkname = 'at@can_sr1'
        arrival_page.input_trunk_name(trunkname)
        arrival_page.click_search()
        trunk_id = DataConstruction.get_trunk_id_by_name(trunkname)
        arrival_page.cancel_trunk(trunk_id=trunk_id)
        assert arrival_page.check_cancel_button_enabled(trunk_id) is False

    @allure.story("web_arrival_cancel_trunk_line")
    def test_29_cancel_shuttle_regular_future_date(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        arrival_page.input_op_date(arrival_page.get_date_with_offset(offset=1))
        trunkname = 'at@can_sr2'
        arrival_page.input_trunk_name(trunkname)
        arrival_page.click_search()
        trunk_id = DataConstruction.get_trunk_id_by_name(trunkname)
        assert arrival_page.check_cancel_button_enabled(trunk_id) is False

    @allure.story("web_arrival_cancel_trunk_line")
    def test_30_cancel_shuttle_regular_past_date(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        arrival_page.input_op_date(arrival_page.get_date_with_offset(offset=-1))
        trunkname = 'at@can_si'
        arrival_page.input_trunk_name(trunkname)
        arrival_page.click_search()
        trunk_id = DataConstruction.get_trunk_id_by_name(trunkname)
        arrival_page.cancel_trunk(trunk_id=trunk_id)
        assert arrival_page.check_cancel_button_enabled(trunk_id) is False

    @allure.story("web_arrival_cancel_trunk_line")
    def test_31_cancel_shuttle_regular_current_date(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        arrival_page.input_op_date(arrival_page.get_date_with_offset(offset=0))
        trunkname = 'at@can_si1'
        arrival_page.input_trunk_name(trunkname)
        arrival_page.click_search()
        trunk_id = DataConstruction.get_trunk_id_by_name(trunkname)
        arrival_page.cancel_trunk(trunk_id=trunk_id)
        assert arrival_page.check_cancel_button_enabled(trunk_id) is False

    @allure.story("web_arrival_cancel_trunk_line")
    def test_32_cancel_shuttle_regular_future_date(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        arrival_page.input_op_date(arrival_page.get_date_with_offset(offset=1))
        trunkname = 'at@can_si2'
        arrival_page.input_trunk_name(trunkname)
        arrival_page.click_search()
        trunk_id = DataConstruction.get_trunk_id_by_name(trunkname)
        assert arrival_page.check_cancel_button_enabled(trunk_id) is False

    @allure.story("web_arrival_show_hide")
    def test_33_show_hide_normal_trunk(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        trunkname = 'at@re13loc'
        trunk_id = DataConstruction.get_trunk_id_by_name(trunkname)
        arrival_page.input_trunk_name(trunkname)
        arrival_page.click_search()
        arrival_page.click_show_button(trunk_id)
        assert arrival_page.get_card_count() == 14
        arrival_page.click_hide_button(trunk_id)
        assert arrival_page.get_card_count() == 7

    @allure.story("web_arrival_show_hide")
    def test_34_show_hide_shuttle_trunk(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        trunkname = 'at@sr19loc'
        trunk_id = DataConstruction.get_trunk_id_by_name(trunkname)
        arrival_page.input_trunk_name(trunkname)
        arrival_page.click_search()
        arrival_page.click_show_button(trunk_id)
        assert arrival_page.get_card_count() == 20
        arrival_page.click_hide_button(trunk_id)
        assert arrival_page.get_card_count() == 7

    @allure.story("web_arrival_trunk_detail")
    def test_35_detail_data(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        trunkname = 'at@con_ir1'
        trunk_id = DataConstruction.get_trunk_id_by_name(trunkname)
        arrival_page.input_trunk_name(trunkname)
        arrival_page.click_search()
        arrival_page.open_actual_arrival_departure_detail(trunk_id)
        assert arrival_page.get_detail_trunk_name() == trunkname
        assert arrival_page.get_detail_trunk_id() == DataConstruction.get_trunk_id_by_name(trunkname)
        assert arrival_page.get_detail_trunk_type() in ('Irregular', '臨時便')
        assert arrival_page.get_detail_comment() == 'automation irregular'
        arrival_page.enter_sub_page(1)

    @allure.story("web_arrival_trunk_edit")
    def test_36_edit_comment_normal_trunk(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        trunkname = 'at@edit_ir'
        trunk_id = DataConstruction.get_trunk_id_by_name(trunkname)
        arrival_page.input_trunk_name(trunkname)
        arrival_page.click_search()
        arrival_page.open_actual_arrival_departure_detail(trunk_id)
        arrival_page.click_edit_in_detail()
        arrival_page.input_edit_comment("CHANGED")
        arrival_page.click_edit_save_button()
        arrival_page.handle_edit_confirm(yes=True) #
        arrival_page.open_actual_arrival_departure_detail(trunk_id)
        assert arrival_page.get_detail_comment() == "CHANGED"
        arrival_page.click_back_in_detail()

    @allure.story("web_arrival_trunk_edit")
    def test_37_edit_departure_data_normal_trunk(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        trunkname = 'at@edit_ir'
        trunk_id = DataConstruction.get_trunk_id_by_name(trunkname)
        arrival_page.input_trunk_name(trunkname)
        arrival_page.click_search()
        arrival_page.open_actual_arrival_departure_detail(trunk_id)
        arrival_page.click_edit_in_detail()
        current_date = arrival_page.get_date_with_offset("/").split("/")
        Logger.info("Current data list"+str(current_date))
        arrival_page.input_edit_dp_actual_departure_time(year=current_date[0], month=current_date[1], day=current_date[2],
                                               hour=1, minute=35)
        arrival_page.input_edit_departure_cart(99)
        arrival_page.click_edit_save_button()
        arrival_page.handle_edit_confirm(yes=True)
        arrival_page.open_actual_arrival_departure_detail(trunk_id)
        assert arrival_page.get_detail_dp_actual_depart_time() == arrival_page.get_date_with_offset("/") + " 01:35"
        assert arrival_page.get_detail_dp_cart() == "99"
        arrival_page.click_back_in_detail()

    @allure.story("web_arrival_trunk_edit")
    def test_38_edit_arrival_data_normal_trunk(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        trunkname = 'at@edit_ir'
        trunk_id = DataConstruction.get_trunk_id_by_name(trunkname)
        arrival_page.input_trunk_name(trunkname)
        arrival_page.click_search()
        arrival_page.open_actual_arrival_departure_detail(trunk_id)
        arrival_page.click_edit_in_detail()
        current_date = arrival_page.get_date_with_offset("/").split("/")
        arrival_page.input_edit_ar_arrival_time(card_order=1, year=current_date[0], month=current_date[1],
                                                day=current_date[2], hour="1", minute="05")
        arrival_page.input_edit_ar_departure_time(card_order=1, year=current_date[0], month=current_date[1],
                                               day=current_date[2], hour="1", minute="35")
        arrival_page.input_edit_ar_scan_cart(card_order=1, cart_num=99)
        arrival_page.input_edit_ar_unload_cart(card_order=1, cart_num=99)
        arrival_page.click_edit_save_button()
        arrival_page.handle_edit_confirm(yes=True)
        arrival_page.open_actual_arrival_departure_detail(trunk_id)
        current_date = arrival_page.get_date_with_offset("/")
        assert arrival_page.get_detail_ar_actual_arrival_time(cart_order=1) == current_date + " 01:05"
        assert arrival_page.get_detail_ar_actual_depart_time(cart_order=1) == current_date + " 01:35"
        assert arrival_page.get_detail_ar_scan_cart(cart_order=1) == "99"
        assert arrival_page.get_detail_ar_unload_cart(cart_order=1) == "99"
        arrival_page.click_back_in_detail()

    @allure.story("web_arrival_trunk_edit")
    def test_39_edit_comment_shuttle_trunk(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        trunkname = 'at@edit_si'
        trunk_id = DataConstruction.get_trunk_id_by_name(trunkname)
        arrival_page.input_trunk_name(trunkname)
        arrival_page.click_search()
        arrival_page.open_actual_arrival_departure_detail(trunk_id)
        arrival_page.click_edit_in_detail()
        arrival_page.input_edit_comment("CHANGE")
        arrival_page.click_edit_save_button()
        arrival_page.handle_edit_confirm(yes=True)
        arrival_page.open_actual_arrival_departure_detail(trunk_id)
        assert arrival_page.get_detail_comment() == "CHANGE"
        arrival_page.click_back_in_detail()

    @allure.story("web_arrival_trunk_edit")
    def test_40_edit_departure_data_shuttle_trunk(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        trunkname = 'at@edit_si'
        trunk_id = DataConstruction.get_trunk_id_by_name(trunkname)
        arrival_page.input_trunk_name(trunkname)
        arrival_page.click_search()
        arrival_page.open_actual_arrival_departure_detail(trunk_id)
        arrival_page.click_edit_in_detail()
        current_date = arrival_page.get_date_with_offset("/").split("/")
        arrival_page.input_edit_dp_actual_departure_time(year=current_date[0], month=current_date[1], day=current_date[2],
                                               hour="00", minute="35")
        arrival_page.input_edit_departure_cart(99)
        arrival_page.click_edit_save_button()
        arrival_page.handle_edit_confirm(yes=True)
        arrival_page.open_actual_arrival_departure_detail(trunk_id)
        current_date = arrival_page.get_date_with_offset("/")
        sleep(2)
        assert arrival_page.get_detail_dp_actual_depart_time() == current_date + " 00:35"
        assert arrival_page.get_detail_dp_cart() == "99"
        arrival_page.click_back_in_detail()

    @allure.story("web_arrival_trunk_edit")
    def test_41_edit_arrival_data_shuttle_trunk(self, web_driver):
        arrival_page = WebArrivalPage(web_driver)
        arrival_page.input_org_id("流山")
        trunkname = 'at@edit_si'
        trunk_id = DataConstruction.get_trunk_id_by_name(trunkname)
        arrival_page.input_trunk_name(trunkname)
        arrival_page.click_search()
        arrival_page.open_actual_arrival_departure_detail(trunk_id)
        arrival_page.click_edit_in_detail()
        current_date = arrival_page.get_date_with_offset("/").split("/")
        arrival_page.input_edit_ar_arrival_time(card_order=1, year=current_date[0], month=current_date[1],
                                                day=current_date[2], hour="1", minute="05")
        arrival_page.input_edit_ar_departure_time(card_order=1, year=current_date[0], month=current_date[1],
                                               day=current_date[2], hour="1", minute="35")
        arrival_page.input_edit_ar_unload_cart(card_order=1, cart_num=99)
        arrival_page.click_edit_save_button()
        arrival_page.handle_edit_confirm(yes=True)
        arrival_page.open_actual_arrival_departure_detail(trunk_id)
        current_date = arrival_page.get_date_with_offset("/")
        assert arrival_page.get_detail_ar_actual_arrival_time(cart_order=1) == current_date + " 01:05"
        assert arrival_page.get_detail_ar_actual_depart_time(cart_order=1) == current_date + " 01:35"
        assert arrival_page.get_detail_ar_unload_cart(cart_order=1) == "99"
        arrival_page.click_back_in_detail()
