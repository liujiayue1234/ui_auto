import pytest
import allure
from WEB.page.web_login_page import WebLoginPage
from WEB.page.web_trunk_overview_page import WebTrunkOverviewPage
from common.readconfig import con
from common.logger import Logger
from common.data_construction import DataConstruction

@allure.feature("web_trunk_overview")
@pytest.mark.web
@pytest.mark.web_trunk_overview
class TestWebTrunkOverview:
    @pytest.fixture(scope='class', autouse=True)
    def user_login(self, web_driver):
        login_page = WebLoginPage(web_driver)
        login_page.get_url(con.get("ENV", "HOST"))
        login_page.admin_login()
        login_page.open_function_page()
        login_page.enter_sub_page(2)
        yield

    @pytest.fixture(scope='function', autouse=True)
    def refresh_url(self, web_driver):
        yield
        login_page = WebLoginPage(web_driver)
        login_page.refresh()


    @allure.story("web_trunk_overview_search")
    def test_42_search_by_org_course(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_page.input_org_id("流山")
        trunkname = 'at@TO_ir'
        trunk_page.input_course_name(trunkname)
        trunk_page.click_search()
        trunk_id = DataConstruction.get_trunk_id_by_name(trunkname)
        assert trunk_page.trunk_line_exist(trunk_id) is True

    @allure.story("web_trunk_overview_search")
    def test_43_search_by_org_pattern_carrier_course(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_page.input_org_id("流山")
        trunk_page.input_op_pattern([1,1,0,0])
        trunk_page.input_carrier('日本')
        trunkname = 'at@TO_ir'
        trunk_page.input_course_name(trunkname)
        trunk_page.click_search()
        trunk_id = DataConstruction.get_trunk_id_by_name(trunkname)
        assert trunk_page.trunk_line_exist(trunk_id) is True

    @allure.story("web_trunk_overview_search")
    def test_44_search_by_all_conditions(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_page.input_org_id("流山")
        trunk_page.input_trunk_type(3)
        trunk_page.input_location("晴海")
        trunk_page.input_op_pattern([1,1,1,1])
        trunk_page.input_carrier("日本")
        trunk_page.input_contract_status([1,1,1])
        trunkname = 'at@TO_sr'
        trunk_id = DataConstruction.get_trunk_id_by_name(trunkname)
        trunk_page.input_course_name(trunkname)
        trunk_page.input_start_date('20350101')
        trunk_page.input_end_date('20350101')
        trunk_page.click_search()
        assert trunk_page.trunk_line_exist(trunk_id) is True

    @allure.story("web_trunk_overview_export_op_id")
    def test_45_export_one_op_id(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_page.input_org_id("流山")
        trunk_page.input_course_name('at@TO')
        trunk_page.click_search()
        trunkname = 'at@TO_ir'
        trunk_id = DataConstruction.get_trunk_id_by_name(trunkname)
        trunk_page.click_export_op_tab()
        trunk_page.select_all_to_export()
        trunk_page.check_trunk_line_to_export(trunk_id)
        trunk_page.click_export_button()
        trunk_page.proceed_to_popup(True)
        assert trunkname in trunk_page.extract_text_from_pdf(trunk_page.get_date_with_offset())

    @allure.story("web_trunk_overview_export_op_id")
    def test_46_export_multiple_op_id(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_page.input_org_id("流山")
        trunk_page.input_course_name('at@TO')
        trunk_page.click_search()
        trunkname1 = 'at@TO_ir'
        trunk_id1 = DataConstruction.get_trunk_id_by_name(trunkname1)
        trunkname2 = 'at@TO_sr'
        trunk_id2 = DataConstruction.get_trunk_id_by_name(trunkname2)
        trunk_page.click_export_op_tab()
        trunk_page.select_all_to_export()
        trunk_page.check_trunk_line_to_export(trunk_id1)
        trunk_page.check_trunk_line_to_export(trunk_id2)
        trunk_page.click_export_button()
        trunk_page.proceed_to_popup(True)
        assert trunkname1 in trunk_page.extract_text_from_pdf(trunk_page.get_date_with_offset())
        assert trunkname2 in trunk_page.extract_text_from_pdf(trunk_page.get_date_with_offset())

    @allure.story("web_trunk_overview_export_op_id")
    def test_47_export_all_op_id(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_page.input_org_id("流山")
        trunk_page.input_course_name('at@TO')
        trunk_page.click_search()
        trunkname1 = 'at@TO_re'
        trunk_id1 = DataConstruction.get_trunk_id_by_name(trunkname1)
        trunkname2 = 'at@TO_sr'
        trunk_id2 = DataConstruction.get_trunk_id_by_name(trunkname2)
        trunkname3 = 'at@TO_ir'
        trunk_id3 = DataConstruction.get_trunk_id_by_name(trunkname2)
        trunkname4 = 'at@TO_si'
        trunk_id4 = DataConstruction.get_trunk_id_by_name(trunkname2)
        trunk_page.click_export_op_tab()
        trunk_page.click_export_button()
        trunk_page.proceed_to_popup(True)
        assert trunkname1 in trunk_page.extract_text_from_pdf(trunk_page.get_date_with_offset())
        assert trunkname2 in trunk_page.extract_text_from_pdf(trunk_page.get_date_with_offset())
        assert trunkname3 in trunk_page.extract_text_from_pdf(trunk_page.get_date_with_offset())
        assert trunkname4 in trunk_page.extract_text_from_pdf(trunk_page.get_date_with_offset())

    @allure.story("web_trunk_overview_delete")
    def test_48_delete_one_trunk(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunkname = 'at@DL1'
        target_date = trunk_page.get_date_with_offset('-',2)
        trunk_id = DataConstruction.create_normal_trunk(trunkname, target_date,target_date,1)
        Logger.info("Trunk id:"+str(trunk_id))
        trunk_page.input_org_id("流山")
        trunk_page.input_course_name(trunkname)
        trunk_page.click_search()
        trunk_page.click_delete_tab()
        trunk_page.check_trunk_line_to_delete(trunk_id)
        trunk_page.click_delete_button()
        trunk_page.proceed_to_popup(True)
        trunk_page.click_search()
        assert trunk_page.trunk_line_exist(trunk_id) is False

    @allure.story("web_trunk_overview_delete")
    def test_49_delete_multiple_trunk(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        target_date = trunk_page.get_date_with_offset('-',2)
        trunkname1 = 'at@DL1'
        trunk_id1 = DataConstruction.create_normal_trunk(trunkname1, target_date, target_date, 1)
        trunkname2 = 'at@DL2'
        trunk_id2 = DataConstruction.create_normal_trunk(trunkname2, target_date, target_date, 2)
        trunk_page.input_org_id("流山")
        trunk_page.input_course_name('at@DL')
        trunk_page.click_search()
        trunk_page.click_delete_tab()
        trunk_page.check_trunk_line_to_delete(trunk_id1)
        trunk_page.check_trunk_line_to_delete(trunk_id2)
        trunk_page.click_delete_button()
        trunk_page.proceed_to_popup(True)
        trunk_page.click_search()
        assert trunk_page.trunk_line_exist(trunk_id1) is False
        assert trunk_page.trunk_line_exist(trunk_id2) is False

    @allure.story("web_trunk_overview_delete")
    def test_50_delete_all(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        target_date = trunk_page.get_date_with_offset('-',2)
        trunkname1 = 'at@DL1'
        trunk_id1 = DataConstruction.create_normal_trunk(trunkname1, target_date, target_date, 1)
        trunkname2 = 'at@DL2'
        trunk_id2 = DataConstruction.create_normal_trunk(trunkname2, target_date, target_date, 2)
        trunkname3 = 'at@DL3'
        trunk_id3 = DataConstruction.create_shuttle_trunk(trunkname3, target_date, target_date, 3)
        trunkname4 = 'at@DL4'
        trunk_id4 = DataConstruction.create_shuttle_trunk(trunkname4, target_date, target_date, 4)
        trunk_page.input_org_id("流山")
        trunk_page.input_course_name('at@DL')
        trunk_page.click_search()
        trunk_page.click_delete_tab()
        trunk_page.select_all_to_delete()
        trunk_page.click_delete_button()
        trunk_page.proceed_to_popup(True)
        trunk_page.click_search()
        assert trunk_page.trunk_line_exist(trunk_id1) is False
        assert trunk_page.trunk_line_exist(trunk_id2) is False
        assert trunk_page.trunk_line_exist(trunk_id3) is False
        assert trunk_page.trunk_line_exist(trunk_id4) is False

    @allure.story("web_trunk_overview_detail")
    def test_51_trunk_detail(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_name = 'at@TO_re'
        trunk_page.input_org_id("流山")
        trunk_page.input_course_name(trunk_name)
        trunk_page.click_search()
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name)
        trunk_page.click_trunk_name_enter_detail(trunk_id)
        assert trunk_page.get_detail_trunk_id() == trunk_id
        assert trunk_page.get_detail_trunk_type() in ('Regular','定期便')
        assert "流山" in trunk_page.get_detail_org_id()
        assert trunk_page.get_detail_trunk_name() == trunk_name
        assert trunk_page.get_detail_course_name() == trunk_name
        assert trunk_page.get_detail_op_pattern() in ('Every day','毎日')
        assert trunk_page.get_detail_vh_type() == '2t'
        trunk_page.click_detail_back_button()

    @allure.story("web_trunk_overview_edit")
    def test_52_shorten_end_date(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_name = 'at@TO_re'
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name)
        trunk_page.input_org_id("流山")
        trunk_page.input_course_name(trunk_name)
        trunk_page.click_search()
        trunk_page.click_trunk_name_enter_detail(trunk_id)
        trunk_page.click_detail_edit_button()
        current_date = trunk_page.get_date_with_offset()
        trunk_page.input_edit_con_end(current_date)
        trunk_page.click_edit_save_button()
        trunk_page.proceed_to_popup(True)
        assert trunk_page.get_detail_trunk_id() == trunk_id
        assert trunk_page.get_detail_con_end() == trunk_page.get_date_with_offset("/")
        trunk_page.click_detail_back_button()

    @allure.story("web_trunk_overview_edit")
    def test_53_expand_end_date(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_name = 'at@TO_re'
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name)
        trunk_page.input_org_id("流山")
        trunk_page.input_course_name(trunk_name)
        trunk_page.click_search()
        trunk_page.click_trunk_name_enter_detail(trunk_id)
        trunk_page.click_detail_edit_button()
        trunk_page.input_edit_con_end('20550101')
        trunk_page.click_edit_save_button()
        trunk_page.proceed_to_popup(True)
        assert trunk_page.get_detail_trunk_id() == trunk_id
        assert trunk_page.get_detail_con_end() == '2055/01/01'
        trunk_page.click_detail_back_button()

    @allure.story("web_trunk_overview_copy_register")
    def test_54_copy_active_regular_failure(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_name = 'at@TO_re'
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name)
        trunk_page.input_org_id("流山")
        trunk_page.input_course_name(trunk_name)
        trunk_page.click_search()
        trunk_page.click_trunk_name_enter_detail(trunk_id)
        trunk_page.click_detail_copy_register_button()
        trunk_page.click_register_button()
        trunk_page.proceed_to_popup(True)
        assert trunk_page.get_register_start_date_error() in ('Please input date at least 1 day in the future.','1日後以降の日付を入力してください。')
        trunk_page.click_register_back_button()
        trunk_page.click_detail_back_button()

    @allure.story("web_trunk_overview_copy_register")
    def test_55_copy_active_irregular_failure(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_name = 'at@TO_ir'
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name)
        trunk_page.input_org_id("流山")
        trunk_page.input_course_name(trunk_name)
        trunk_page.click_search()
        trunk_page.click_trunk_name_enter_detail(trunk_id)
        trunk_page.click_detail_copy_register_button()
        trunk_page.click_register_button()
        trunk_page.proceed_to_popup(True)
        yesterday = trunk_page.get_date_with_offset("/",offset=-1)
        assert trunk_page.get_register_start_date_error() in (
        'The Con. Start should be after the {}'.format(yesterday), '適用開始日は{}より後に設定してください'.format(yesterday))
        trunk_page.click_register_back_button()
        trunk_page.click_detail_back_button()

    @allure.story("web_trunk_overview_copy_register")
    def test_56_copy_prior_trunk_failure(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_name = 'at@TO_copy'
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name,'2055-01-01')
        trunk_page.input_org_id("流山")
        trunk_page.input_course_name(trunk_name)
        trunk_page.click_search()
        trunk_page.click_trunk_name_enter_detail(trunk_id)
        trunk_page.click_detail_copy_register_button()
        trunk_page.click_register_button()
        trunk_page.proceed_to_popup(True)
        assert '重複' in trunk_page.get_register_backend_error() or 'same' in trunk_page.get_register_backend_error()
        #'TL1001: 必須項目が重複しています。登録できません。'
        #'TL1001: You cannot register a Trunk Line with the exact same required fields as another Trunk Line'
        trunk_page.close_register_backend_error()
        trunk_page.click_register_back_button()
        trunk_page.click_detail_back_button()

    @allure.story("web_trunk_overview_copy_register")
    def test_57_copy_trunk_modify_success(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_name = 'at@TO_copy'
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name,'2055-01-01')
        trunk_page.input_org_id("流山")
        trunk_page.input_course_name(trunk_name)
        trunk_page.click_search()
        trunk_page.click_trunk_name_enter_detail(trunk_id)
        trunk_page.click_detail_copy_register_button()
        copy_name = "at@copy1"
        trunk_page.input_register_trunk_name(copy_name)
        trunk_page.input_register_course_name(copy_name)
        trunk_page.input_register_contract_end_date('2055-01-02')
        trunk_page.click_register_button()
        trunk_page.proceed_to_popup(True)
        trunk_page.input_course_name(copy_name)
        trunk_page.click_search()
        trunk_id = DataConstruction.get_trunk_id_by_name(copy_name,'2055-01-01')
        assert trunk_page.trunk_line_exist(trunk_id) is True
        DataConstruction.delete_trunk(trunk_id)

    @allure.story("web_trunk_overview_register")
    def test_58_register_failure_regular_today(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_page.open_register_page()
        trunk_name = 'at@new_re1'
        trunk_page.input_register_org_id("流山")
        trunk_page.input_register_course_name(trunk_name)
        trunk_page.input_register_trunk_name(trunk_name)
        trunk_page.input_register_trunk_type(1)
        trunk_page.input_register_op_pattern(1)
        trunk_page.input_register_carrier('日本')
        trunk_page.input_register_vehicle_type(1)
        today = trunk_page.get_date_with_offset()
        trunk_page.input_register_contract_start_date(today)
        trunk_page.input_register_contract_end_date(today)
        trunk_page.input_register_comment("Registered by automation")
        trunk_page.input_register_dp_location('流山')
        trunk_page.input_register_dp_plan_arrival_time("0000")
        trunk_page.input_register_dp_plan_departure_time("0030")
        trunk_page.input_register_ar_location('晴海',card_order=1)
        trunk_page.input_register_ar_plan_arrival_time("0100",card_order=1)
        trunk_page.click_register_button()
        trunk_page.proceed_to_popup(True)
        assert trunk_page.get_register_start_date_error() in (
        'Please input date at least 1 day in the future.', '1日後以降の日付を入力してください。')
        trunk_page.click_register_back_button()

    @allure.story("web_trunk_overview_register")
    def test_59_register_success_regular_tomorrow(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_page.open_register_page()
        trunk_name = 'at@new_re2'
        trunk_page.input_register_org_id("流山")
        trunk_page.input_register_course_name(trunk_name)
        trunk_page.input_register_trunk_name(trunk_name)
        trunk_page.input_register_trunk_type(1)
        trunk_page.input_register_op_pattern(1)
        trunk_page.input_register_carrier('日本')
        trunk_page.input_register_vehicle_type(1)
        tomorrow = trunk_page.get_date_with_offset('',1)
        trunk_page.input_register_contract_start_date(tomorrow)
        trunk_page.input_register_contract_end_date(tomorrow)
        trunk_page.input_register_comment("Registered by automation")
        trunk_page.input_register_dp_location('流山')
        trunk_page.input_register_dp_plan_arrival_time("0000")
        trunk_page.input_register_dp_plan_departure_time("0030")
        trunk_page.input_register_ar_location('晴海',card_order=1)
        trunk_page.input_register_ar_plan_arrival_time("0100",card_order=1)
        trunk_page.click_register_button()
        trunk_page.proceed_to_popup(True)
        # search to verify the result
        trunk_page.input_course_name(trunk_name)
        trunk_page.click_search()
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name,trunk_page.get_date_with_offset('-',1))
        assert trunk_page.trunk_line_exist(trunk_id) is True
        DataConstruction.delete_trunk(trunk_id)

    @allure.story("web_trunk_overview_register")
    def test_60_register_failure_irregular_yesterday(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_page.open_register_page()
        trunk_name = 'at@new_ir1'
        trunk_page.input_register_org_id("流山")
        trunk_page.input_register_course_name(trunk_name)
        trunk_page.input_register_trunk_name(trunk_name)
        trunk_page.input_register_trunk_type(2)
        trunk_page.input_register_op_pattern(1)
        trunk_page.input_register_carrier('日本')
        trunk_page.input_register_vehicle_type(1)
        yesterday = trunk_page.get_date_with_offset('',-1)
        trunk_page.input_register_contract_start_date(yesterday)
        trunk_page.input_register_contract_end_date(yesterday)
        trunk_page.input_register_comment("Registered by automation")
        trunk_page.input_register_irregular_reason(1)
        trunk_page.input_register_dp_location('流山')
        trunk_page.input_register_dp_plan_arrival_time("0000")
        trunk_page.input_register_dp_plan_departure_time("0030")
        trunk_page.input_register_ar_location('晴海',card_order=1)
        trunk_page.input_register_ar_plan_arrival_time("0100",card_order=1)
        trunk_page.click_register_button()
        trunk_page.proceed_to_popup(True)
        yesterday = trunk_page.get_date_with_offset('/', -1)
        assert trunk_page.get_register_start_date_error() in (
            'The Con. Start should be after the {}'.format(yesterday),
            '適用開始日は{}より後に設定してください'.format(yesterday))
        assert trunk_page.get_register_end_date_error() in (
            'The Con. End should be after the {}'.format(yesterday),
            '適用終了日は{}より後に設定してください'.format(yesterday))
        trunk_page.click_register_back_button()

    @allure.story("web_trunk_overview_register")
    def test_61_register_success_irregular_today(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_page.open_register_page()
        trunk_name = 'at@new_ir2'
        trunk_page.input_register_org_id("流山")
        trunk_page.input_register_course_name(trunk_name)
        trunk_page.input_register_trunk_name(trunk_name)
        trunk_page.input_register_trunk_type(2)
        trunk_page.input_register_op_pattern(1)
        trunk_page.input_register_carrier('日本')
        trunk_page.input_register_vehicle_type(1)
        today = trunk_page.get_date_with_offset('',0)
        trunk_page.input_register_contract_start_date(today)
        trunk_page.input_register_contract_end_date(today)
        trunk_page.input_register_comment("Registered by automation")
        trunk_page.input_register_irregular_reason(1)
        trunk_page.input_register_dp_location('流山')
        trunk_page.input_register_dp_plan_arrival_time("0000")
        trunk_page.input_register_dp_plan_departure_time("0030")
        trunk_page.input_register_ar_location('晴海',card_order=1)
        trunk_page.input_register_ar_plan_arrival_time("0100",card_order=1)
        trunk_page.click_register_button()
        trunk_page.proceed_to_popup(True)
        # search to verify the result
        trunk_page.input_course_name(trunk_name)
        trunk_page.click_search()
        today =  trunk_page.get_date_with_offset('-',0)
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name,today)
        assert trunk_page.trunk_line_exist(trunk_id) is True
        DataConstruction.delete_trunk(trunk_id)

    @allure.story("web_trunk_overview_register")
    def test_62_register_success_normal_13_location(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_page.open_register_page()
        trunk_name = 'at@new_13'
        trunk_page.input_register_org_id("流山")
        trunk_page.input_register_course_name(trunk_name)
        trunk_page.input_register_trunk_name(trunk_name)
        trunk_page.input_register_trunk_type(2)
        trunk_page.input_register_op_pattern(1)
        trunk_page.input_register_carrier('日本')
        trunk_page.input_register_vehicle_type(1)
        tomorrow = trunk_page.get_date_with_offset('',1)
        trunk_page.input_register_contract_start_date(tomorrow)
        trunk_page.input_register_contract_end_date(tomorrow)
        trunk_page.input_register_comment("Registered by automation")
        trunk_page.input_register_irregular_reason(3)
        trunk_page.input_register_dp_location('流山')
        trunk_page.input_register_dp_plan_arrival_time("0000")
        trunk_page.input_register_dp_plan_departure_time("0030")
        for i in range(12):
            trunk_page.click_register_add_arrival_item()
        # 1
        trunk_page.input_register_ar_location('晴海',card_order=1)
        trunk_page.input_register_ar_plan_arrival_time("0100",card_order=1)
        trunk_page.input_register_ar_plan_departure_time('0130',card_order=1)
        # 2
        trunk_page.input_register_ar_location('芝',card_order=2)
        trunk_page.input_register_ar_plan_arrival_time("0200",card_order=2)
        trunk_page.input_register_ar_plan_departure_time('0230',card_order=2)
        # 3
        trunk_page.input_register_ar_location('高輪',card_order=3)
        trunk_page.input_register_ar_plan_arrival_time("0300",card_order=3)
        trunk_page.input_register_ar_plan_departure_time('0330',card_order=3)
        # 4
        trunk_page.input_register_ar_location('上野',card_order=4)
        trunk_page.input_register_ar_plan_arrival_time("0400",card_order=4)
        trunk_page.input_register_ar_plan_departure_time('0430',card_order=4)
        # 5
        trunk_page.input_register_ar_location('浅草',card_order=5)
        trunk_page.input_register_ar_plan_arrival_time("0500",card_order=5)
        trunk_page.input_register_ar_plan_departure_time('0530',card_order=5)
        # 6
        trunk_page.input_register_ar_location('小石川',card_order=6)
        trunk_page.input_register_ar_plan_arrival_time("0600",card_order=6)
        trunk_page.input_register_ar_plan_departure_time('0630',card_order=6)
        # 7
        trunk_page.input_register_ar_location('王子',card_order=7)
        trunk_page.input_register_ar_plan_arrival_time("0700",card_order=7)
        trunk_page.input_register_ar_plan_departure_time('0730',card_order=7)
        # 8
        trunk_page.input_register_ar_location('赤羽',card_order=8)
        trunk_page.input_register_ar_plan_arrival_time("0800",card_order=8)
        trunk_page.input_register_ar_plan_departure_time('0830',card_order=8)
        # 9
        trunk_page.input_register_ar_location('荒川',card_order=9)
        trunk_page.input_register_ar_plan_arrival_time("0900",card_order=9)
        trunk_page.input_register_ar_plan_departure_time('0930',card_order=9)
        # 10
        trunk_page.input_register_ar_location('足立北',card_order=10)
        trunk_page.input_register_ar_plan_arrival_time("1000",card_order=10)
        trunk_page.input_register_ar_plan_departure_time('1030',card_order=10)
        # 11
        trunk_page.input_register_ar_location('足立西',card_order=11)
        trunk_page.input_register_ar_plan_arrival_time("1100",card_order=11)
        trunk_page.input_register_ar_plan_departure_time('1130',card_order=11)
        # 12
        trunk_page.input_register_ar_location('葛飾新宿',card_order=12)
        trunk_page.input_register_ar_plan_arrival_time("1200",card_order=12)
        trunk_page.input_register_ar_plan_departure_time('1230',card_order=12)
        # 13
        trunk_page.input_register_ar_location('本所',card_order=13)
        trunk_page.input_register_ar_plan_arrival_time("1300",card_order=13)
        trunk_page.click_register_button()
        trunk_page.proceed_to_popup(True)
        # search to verify the result
        trunk_page.input_course_name(trunk_name)
        trunk_page.click_search()
        tomorrow = trunk_page.get_date_with_offset('-',1)
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name,tomorrow)
        assert trunk_page.trunk_line_exist(trunk_id) is True
        DataConstruction.delete_trunk(trunk_id)

    @allure.story("web_trunk_overview_register")
    def test_63_register_failure_shuttle_regular_yesterday(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_page.open_register_page()
        trunk_name = 'at@new_sr1'
        trunk_page.input_register_org_id("流山")
        trunk_page.input_register_course_name(trunk_name)
        trunk_page.input_register_trunk_name(trunk_name)
        trunk_page.input_register_trunk_type(3)
        trunk_page.input_register_op_pattern(1)
        trunk_page.input_register_carrier('日本')
        trunk_page.input_register_vehicle_type(1)
        yesterday = trunk_page.get_date_with_offset('',-1)
        trunk_page.input_register_contract_start_date(yesterday)
        trunk_page.input_register_contract_end_date(yesterday)
        trunk_page.input_register_comment("Registered by automation")
        trunk_page.input_register_dp_location('流山')
        trunk_page.input_register_ar_location('晴海', card_order=1)
        trunk_page.click_register_button()
        trunk_page.proceed_to_popup(True)
        yesterday = trunk_page.get_date_with_offset('/', -1)
        assert trunk_page.get_register_start_date_error() in (
            'The Con. Start should be after the {}'.format(yesterday),
            '適用開始日は{}より後に設定してください'.format(yesterday))
        assert trunk_page.get_register_end_date_error() in (
            'The Con. End should be after the {}'.format(yesterday),
            '適用終了日は{}より後に設定してください'.format(yesterday))
        trunk_page.click_register_back_button()

    @allure.story("web_trunk_overview_register")
    def test_64_register_success_shuttle_regular_today(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_page.open_register_page()
        trunk_name = 'at@new_sr2'
        trunk_page.input_register_org_id("流山")
        trunk_page.input_register_course_name(trunk_name)
        trunk_page.input_register_trunk_name(trunk_name)
        trunk_page.input_register_trunk_type(3)
        trunk_page.input_register_op_pattern(1)
        trunk_page.input_register_carrier('日本')
        trunk_page.input_register_vehicle_type(1)
        tomorrow = trunk_page.get_date_with_offset('',1)
        trunk_page.input_register_contract_start_date(tomorrow)
        trunk_page.input_register_contract_end_date(tomorrow)
        trunk_page.input_register_comment("Registered by automation")
        trunk_page.input_register_dp_location('流山')
        trunk_page.input_register_ar_location('晴海', card_order=1)
        trunk_page.click_register_button()
        trunk_page.proceed_to_popup(True)
        # search to verify the result
        trunk_page.input_course_name(trunk_name)
        trunk_page.click_search()
        tomorrow = trunk_page.get_date_with_offset('-', 1)
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name,tomorrow)
        assert trunk_page.trunk_line_exist(trunk_id) is True
        DataConstruction.delete_trunk(trunk_id)

    @allure.story("web_trunk_overview_register")
    def test_65_register_failure_shuttle_irregular_yesterday(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_page.open_register_page()
        trunk_name = 'at@new_sr1'
        trunk_page.input_register_org_id("流山")
        trunk_page.input_register_course_name(trunk_name)
        trunk_page.input_register_trunk_name(trunk_name)
        trunk_page.input_register_trunk_type(4)
        trunk_page.input_register_op_pattern(1)
        trunk_page.input_register_carrier('日本')
        trunk_page.input_register_vehicle_type(1)
        yesterday = trunk_page.get_date_with_offset('',-1)
        trunk_page.input_register_contract_start_date(yesterday)
        trunk_page.input_register_contract_end_date(yesterday)
        trunk_page.input_register_comment("Registered by automation")
        trunk_page.input_register_irregular_reason(2)
        trunk_page.input_register_dp_location('流山')
        trunk_page.input_register_ar_location('晴海', card_order=1)
        trunk_page.click_register_button()
        trunk_page.proceed_to_popup(True)
        yesterday = trunk_page.get_date_with_offset('/', -1)
        assert trunk_page.get_register_start_date_error() in (
            'The Con. Start should be after the {}'.format(yesterday),
            '適用開始日は{}より後に設定してください'.format(yesterday))
        assert trunk_page.get_register_end_date_error() in (
            'The Con. End should be after the {}'.format(yesterday),
            '適用終了日は{}より後に設定してください'.format(yesterday))
        trunk_page.click_register_back_button()

    @allure.story("web_trunk_overview_register")
    def test_66_register_success_shuttle_irregular_today(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_page.open_register_page()
        trunk_name = 'at@new_sr2'
        trunk_page.input_register_org_id("流山")
        trunk_page.input_register_course_name(trunk_name)
        trunk_page.input_register_trunk_name(trunk_name)
        trunk_page.input_register_trunk_type(4)
        trunk_page.input_register_op_pattern(1)
        trunk_page.input_register_carrier('日本')
        trunk_page.input_register_vehicle_type(1)
        today = trunk_page.get_date_with_offset('',0)
        trunk_page.input_register_contract_start_date(today)
        trunk_page.input_register_contract_end_date(today)
        trunk_page.input_register_comment("Registered by automation")
        trunk_page.input_register_irregular_reason(2)
        trunk_page.input_register_dp_location('流山')
        trunk_page.input_register_ar_location('晴海', card_order=1)
        trunk_page.click_register_button()
        trunk_page.proceed_to_popup(True)
        # search to verify the result
        trunk_page.input_course_name(trunk_name)
        trunk_page.click_search()
        today = trunk_page.get_date_with_offset('-',0)
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name,today)
        assert trunk_page.trunk_line_exist(trunk_id) is True
        DataConstruction.delete_trunk(trunk_id)

    @allure.story("web_trunk_overview_register")
    def test_67_register_success_shuttle_19_location(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_page.open_register_page()
        trunk_name = 'at@new_19'
        trunk_page.input_register_org_id("流山")
        trunk_page.input_register_course_name(trunk_name)
        trunk_page.input_register_trunk_name(trunk_name)
        trunk_page.input_register_trunk_type(4)
        trunk_page.input_register_op_pattern(1)
        trunk_page.input_register_carrier('日本')
        trunk_page.input_register_vehicle_type(1)
        tomorrow = trunk_page.get_date_with_offset('',1)
        trunk_page.input_register_contract_start_date(tomorrow)
        trunk_page.input_register_contract_end_date(tomorrow)
        trunk_page.input_register_comment("Registered by automation")
        trunk_page.input_register_irregular_reason(2)
        trunk_page.input_register_dp_location('流山')
        for i in range(18):
            trunk_page.click_register_add_arrival_item()
        # 1
        trunk_page.input_register_ar_location('晴海', card_order=1)
        # 2
        trunk_page.input_register_ar_location('流山', card_order=2)
        # 3
        trunk_page.input_register_ar_location('晴海', card_order=3)
        # 4
        trunk_page.input_register_ar_location('流山', card_order=4)
        # 5
        trunk_page.input_register_ar_location('晴海', card_order=5)
        # 6
        trunk_page.input_register_ar_location('流山', card_order=6)
        # 7
        trunk_page.input_register_ar_location('晴海', card_order=7)
        # 8
        trunk_page.input_register_ar_location('流山', card_order=8)
        # 9
        trunk_page.input_register_ar_location('晴海', card_order=9)
        # 10
        trunk_page.input_register_ar_location('流山', card_order=10)
        # 11
        trunk_page.input_register_ar_location('晴海', card_order=11)
        # 12
        trunk_page.input_register_ar_location('流山', card_order=12)
        # 13
        trunk_page.input_register_ar_location('晴海', card_order=13)
        # 14
        trunk_page.input_register_ar_location('流山', card_order=14)
        # 15
        trunk_page.input_register_ar_location('晴海', card_order=15)
        # 16
        trunk_page.input_register_ar_location('流山', card_order=16)
        # 17
        trunk_page.input_register_ar_location('晴海', card_order=17)
        # 18
        trunk_page.input_register_ar_location('流山', card_order=18)
        # 19
        trunk_page.input_register_ar_location('晴海', card_order=19)
        trunk_page.click_register_button()
        trunk_page.proceed_to_popup(True)
        # search to verify the result
        trunk_page.input_course_name(trunk_name)
        trunk_page.click_search()
        tomorrow = trunk_page.get_date_with_offset('-', 1)
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name,tomorrow)
        assert trunk_page.trunk_line_exist(trunk_id) is True
        DataConstruction.delete_trunk(trunk_id)

    @allure.story("web_trunk_overview_register")
    def test_68_register_jp_characters(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_page.open_register_page()
        trunk_name = 'at@日本'
        trunk_page.input_register_org_id("流山")
        trunk_page.input_register_course_name(trunk_name)
        trunk_page.input_register_trunk_name(trunk_name)
        trunk_page.input_register_trunk_type(3)
        trunk_page.input_register_op_pattern(1)
        trunk_page.input_register_carrier('日本')
        trunk_page.input_register_vehicle_type(1)
        tomorrow = trunk_page.get_date_with_offset('',1)
        trunk_page.input_register_contract_start_date(tomorrow)
        trunk_page.input_register_contract_end_date(tomorrow)
        #allow to input JP characters
        trunk_page.input_register_comment(trunk_name)
        trunk_page.input_register_vehicle_number(trunk_name)
        trunk_page.input_register_driver_name(trunk_name)

        trunk_page.input_register_dp_location('流山')
        trunk_page.input_register_ar_location('晴海', card_order=1)
        trunk_page.click_register_button()
        trunk_page.proceed_to_popup(True)
        # search to verify the result
        trunk_page.input_course_name(trunk_name)
        trunk_page.click_search()
        tomorrow = trunk_page.get_date_with_offset('-', 1)
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name,tomorrow)
        assert trunk_page.trunk_line_exist(trunk_id) is True
        DataConstruction.delete_trunk(trunk_id)

    @allure.story("web_trunk_overview_register")
    def test_69_register_en_characters(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_page.open_register_page()
        trunk_name = 'at@English'
        trunk_page.input_register_org_id("流山")
        trunk_page.input_register_course_name(trunk_name)
        trunk_page.input_register_trunk_name(trunk_name)
        trunk_page.input_register_trunk_type(3)
        trunk_page.input_register_op_pattern(1)
        trunk_page.input_register_carrier('日本')
        trunk_page.input_register_vehicle_type(1)
        tomorrow = trunk_page.get_date_with_offset('',1)
        trunk_page.input_register_contract_start_date(tomorrow)
        trunk_page.input_register_contract_end_date(tomorrow)
        # allow to input EN characters
        trunk_page.input_register_comment(trunk_name)
        trunk_page.input_register_vehicle_number(trunk_name)
        trunk_page.input_register_driver_name(trunk_name)

        trunk_page.input_register_dp_location('流山')
        trunk_page.input_register_ar_location('晴海', card_order=1)
        trunk_page.click_register_button()
        trunk_page.proceed_to_popup(True)
        # search to verify the result
        trunk_page.input_course_name(trunk_name)
        trunk_page.click_search()
        tomorrow = trunk_page.get_date_with_offset('-',1)
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name,tomorrow)
        assert trunk_page.trunk_line_exist(trunk_id) is True
        DataConstruction.delete_trunk(trunk_id)

    @allure.story("web_trunk_overview_register")
    def test_70_register_special_characters(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_page.open_register_page()
        trunk_name = 'at@#$%&'
        trunk_page.input_register_org_id("流山")
        trunk_page.input_register_course_name(trunk_name)
        trunk_page.input_register_trunk_name(trunk_name)
        trunk_page.input_register_trunk_type(3)
        trunk_page.input_register_op_pattern(1)
        trunk_page.input_register_carrier('日本')
        trunk_page.input_register_vehicle_type(1)
        tomorrow = trunk_page.get_date_with_offset('',1)
        trunk_page.input_register_contract_start_date(tomorrow)
        trunk_page.input_register_contract_end_date(tomorrow)
        # allow to input special characters
        trunk_page.input_register_comment(trunk_name)
        trunk_page.input_register_vehicle_number(trunk_name)
        trunk_page.input_register_driver_name(trunk_name)
        trunk_page.input_register_dp_location('流山')
        trunk_page.input_register_ar_location('晴海', card_order=1)
        trunk_page.click_register_button()
        trunk_page.proceed_to_popup(True)
        # search to verify the result
        trunk_page.input_course_name(trunk_name)
        trunk_page.click_search()
        tomorrow = trunk_page.get_date_with_offset('-', 1)
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name,tomorrow)
        assert trunk_page.trunk_line_exist(trunk_id) is True
        DataConstruction.delete_trunk(trunk_id)

    @allure.story("web_trunk_overview_register")
    def test_71_register_numbers(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_page.open_register_page()
        trunk_name = 'at@123456'
        trunk_page.input_register_org_id("流山")
        trunk_page.input_register_course_name(trunk_name)
        trunk_page.input_register_trunk_name(trunk_name)
        trunk_page.input_register_trunk_type(3)
        trunk_page.input_register_op_pattern(1)
        trunk_page.input_register_carrier('日本')
        trunk_page.input_register_vehicle_type(1)
        tomorrow = trunk_page.get_date_with_offset('',1)
        trunk_page.input_register_contract_start_date(tomorrow)
        trunk_page.input_register_contract_end_date(tomorrow)
        # allow to input numbers
        trunk_page.input_register_comment(trunk_name)
        trunk_page.input_register_vehicle_number(trunk_name)
        trunk_page.input_register_driver_name(trunk_name)
        trunk_page.input_register_cost(123456789)
        trunk_page.input_register_load_weight(123456789)
        trunk_page.input_register_phone_number(12345678901)
        trunk_page.input_register_dp_location('流山')
        trunk_page.input_register_ar_location('晴海', card_order=1)
        trunk_page.click_register_button()
        trunk_page.proceed_to_popup(True)
        # search to verify the result
        trunk_page.input_course_name(trunk_name)
        trunk_page.click_search()
        tomorrow = trunk_page.get_date_with_offset('-', 1)
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name,tomorrow)
        assert trunk_page.trunk_line_exist(trunk_id) is True
        DataConstruction.delete_trunk(trunk_id)

    @allure.story("web_trunk_overview_register")
    def test_72_register_trunk_max_length(self, web_driver):
        trunk_page = WebTrunkOverviewPage(web_driver)
        trunk_page.open_register_page()
        trunk_name = 'at@max_len'
        trunk_page.input_register_org_id("流山")
        trunk_page.input_register_course_name(trunk_name)
        trunk_page.input_register_trunk_name(trunk_name)
        trunk_page.input_register_trunk_type(3)
        trunk_page.input_register_op_pattern(1)
        trunk_page.input_register_carrier('日本')
        trunk_page.input_register_vehicle_type(1)
        tomorrow = trunk_page.get_date_with_offset('',1)
        trunk_page.input_register_contract_start_date(tomorrow)
        trunk_page.input_register_contract_end_date(tomorrow)
        # allow to input max length
        trunk_page.input_register_comment('1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890')
        trunk_page.input_register_vehicle_number(1234567890)
        trunk_page.input_register_driver_name(1234567890)
        trunk_page.input_register_cost(1234567890)
        trunk_page.input_register_load_weight(123456789012)
        trunk_page.input_register_phone_number(12345678901)
        trunk_page.input_register_dp_location('流山')
        trunk_page.input_register_ar_location('晴海', card_order=1)
        trunk_page.click_register_button()
        trunk_page.proceed_to_popup(True)
        # search to verify the result
        trunk_page.input_course_name(trunk_name)
        trunk_page.click_search()
        tomorrow = trunk_page.get_date_with_offset('-', 1)
        trunk_id = DataConstruction.get_trunk_id_by_name(trunk_name,tomorrow)
        assert trunk_page.trunk_line_exist(trunk_id) is True
        DataConstruction.delete_trunk(trunk_id)

