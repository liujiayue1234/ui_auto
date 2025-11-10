from sys import excepthook

from selenium.webdriver.support.expected_conditions import element_to_be_clickable

from common.logger import Logger
from common.readconfig import con
from WEB.base.basepage import Basepage
from common.readelement import Element
from config.config import WEB_ELEMENT_PATH,DOWNLOAD_PATH
import time
import glob
import os
import pdfplumber
search = Element(WEB_ELEMENT_PATH, 'web_trunk_overview_element')


class WebTrunkOverviewPage(Basepage):
    def input_org_id(self, value):
        """
        :param value: example 流山
        :return:
        """
        self.send_key(search['OrgInput'], value)
        self.press_key(search['OrgInput'], "down")
        self.press_key(search['OrgInput'], "enter")

    def input_trunk_type(self, type=1):
        """
        :param type: 1:regular 2:irregular 3:regular shuttle 4:irregular shuttle
        :return:
        """
        self.click(search['TrunkTypeInput'])
        self.press_key(search['TrunkTypeInput'], "down")
        for i in range(type):
            self.press_key(search['TrunkTypeInput'], "down")
        self.press_key(search['TrunkTypeInput'], "enter")

    def input_location(self, value):
        self.send_key(search['ArrivalLocationInput'], value)
        self.press_key(search['ArrivalLocationInput'], "down")
        self.press_key(search['ArrivalLocationInput'], "enter")
        self.press_key(search['ArrivalLocationInput'], "tab")

    def input_op_pattern(self, value):
        """
        :param value: example [1,1,1,1] 1:select 0:unselect,  Every day|Sat,Sun|Mon-Fri|Other
        :return:
        """
        self.click(search['OpPatternInput'])
        self.press_key(search['OpPatternInput'], "down")
        if value[0]:
            self.press_key(search['OpPatternInput'], "enter")
        self.press_key(search['OpPatternInput'], "down")
        if value[1]:
            self.press_key(search['OpPatternInput'], "enter")
        self.press_key(search['OpPatternInput'], "down")
        if value[2]:
            self.press_key(search['OpPatternInput'], "enter")
        self.press_key(search['OpPatternInput'], "down")
        if value[3]:
            self.press_key(search['OpPatternInput'], "enter")
        self.press_key(search['OpPatternInput'], "tab")

    def input_carrier(self, value):
        """
        :param value: carrier
        :return:
        """
        self.send_key(search['CarrierInput'], value)
        self.press_key(search['CarrierInput'], "down")
        self.press_key(search['CarrierInput'], "enter")
        self.press_key(search['CarrierInput'], "tab")

    def input_contract_status(self, value):
        """
        :param value: example [1,1,1] 1:select 0:unselect: Prior｜Active|Post
        :return:
        """
        self.click(search['ContractStatusInput'])
        self.press_key(search['ContractStatusInput'], "down")
        self.press_key(search['ContractStatusInput'], "down")
        if value[0]:
            self.press_key(search['ContractStatusInput'], "enter")
        self.press_key(search['ContractStatusInput'], "down")
        if value[1]:
            self.press_key(search['ContractStatusInput'], "enter")
        self.press_key(search['ContractStatusInput'], "down")
        if value[2]:
            self.press_key(search['ContractStatusInput'], "enter")
        self.press_key(search['ContractStatusInput'], "tab")

    def input_course_name(self, value):
        """
        :param value: course_name
        :return:
        """
        self.send_key(search['CourseNameInput'], value)

    def input_start_date(self, value):
        """
        :param value: example 202050101
        :return:
        """
        self.driver.implicitly_wait(2)
        self.send_key(search['startDateInput'], value)

    def input_end_date(self, value):
        """
        :param value: example 202050101
        :return:
        """
        self.driver.implicitly_wait(2)
        self.send_key(search['endDateInput'], value)

    def click_search(self):
        self.click(search['SearchButton'])

    def click_export_op_tab(self):
        self.click(search['ExportOpTab'])

    def click_delete_tab(self):
        self.click(search['DeleteTab'])

    def check_trunk_line_to_export(self, trunk_line_id):
        self.click(search['export_checkbox'], trunk_line_id)

    def check_trunk_line_to_delete(self, trunk_line_id):
        self.click(search['delete_checkbox'], str(trunk_line_id),True)

    def select_all_to_export(self):
        self.click(search['selectAllExportButton'])

    def select_all_to_delete(self):
        self.click(search['selectAllDeleteButton'])

    def click_export_button(self):
        self.click(search['exportButton'],None,False)

    def click_delete_button(self):
        self.click(search['deleteButton'],None,False)

    def get_popup_title(self):
        return self.get_text(search['PopupTitle'])

    def get_popup_hint(self):
        return self.get_text(search['PopupHint'])

    def get_popup_item(self, item_order=1):
        return [self.get_text(search['PopupItemNo'], str(item_order)),
                self.get_text(search['PopupItemTrunkName'], str(item_order)),
                self.get_text(search['PopupItemCourseName'], str(item_order))]

    def proceed_to_popup(self, yes_option=True):
        if yes_option:
            self.click(search['PopupYesButton'])
        else:
            self.click(search['PopupNoButton'])

    def open_register_page(self):
        self.click(search['RegisterNewButton'],dynamic_value=None,wait_loading=False)
        self.driver.implicitly_wait(0.5)

    def trunk_line_exist(self, trunk_id):
        self.wait_loading_icon_disappear()
        try:
            return self.check_element_exist(search['trunkNameButton'], trunk_id, 2)
        except Exception as e:
            return False

    def click_trunk_name_enter_detail(self,trunk_id):
        self.click(search['trunkNameButton'],trunk_id)
        self.wait_page_load_complete()

    def get_detail_trunk_id(self):
        return self.get_text(search['detail_trunkId'])
    def get_detail_org_id(self):
        return self.get_text(search['detail_OrgId'])
    def get_detail_course_name(self):
        return self.get_text(search['detail_courseName'])
    def get_detail_trunk_name(self):
        return self.get_text(search['detail_trunkName'])
    def get_detail_trunk_type(self):
        return self.get_text(search['detail_trunkType'])
    def get_detail_op_pattern(self):
        return self.get_text(search['detail_opPattern'])
    def get_detail_carrier(self):
        return self.get_text(search['detail_carrier'])
    def get_detail_vh_type(self):
        return self.get_text(search['detail_vhType'])
    def get_detail_con_start(self):
        return self.get_text(search['detail_conStart'])
    def get_detail_con_end(self):
        return self.get_text(search['detail_conEnd'])
    def get_detail_cost(self):
        return self.get_text(search['detail_cost'])
    def get_detail_weight(self):
        return self.get_text(search['detail_weight'])
    def get_detail_phone_number(self):
        return self.get_text(search['detail_PhoneNum'])
    def get_detail_vh_num(self):
        return self.get_text(search['detail_vhNum'])
    def get_detail_driver(self):
        return self.get_text(search['detail_driver'])
    def get_detail_comment(self):
        return self.get_text(search['detail_comment'])
    def get_detail_dp_location(self):
        return self.get_text(search['detail_Dp_location'])
    def get_detail_dp_plan_arrival_time(self):
        return self.get_text(search['detail_Dp_PlanArTime'])
    def get_detail_dp_plan_depart_time(self):
        return self.get_text(search['detail_Dp_PlanDpTime'])

    def get_detail_ar_location(self,card_order):
        return self.get_text(search['detail_Ar_location'],str(card_order))
    def get_detail_ar_plan_arrival_time(self,card_order):
        return self.get_text(search['detail_Ar_planArTime'],str(card_order))
    def get_detail_ar_plan_arrival_date(self,card_order):
        return self.get_text(search['detail_Ar_planArDate'],str(card_order))
    def get_detail_ar_plan_depart_time(self,card_order):
        return self.get_text(search['detail_Ar_planDpTime'],str(card_order))
    def get_detail_ar_plan_depart_date(self,card_order):
        return self.get_text(search['detail_Ar_planDpDate'],str(card_order))
    def click_detail_back_button(self):
        self.click(search['detail_backButton'])
        self.wait_page_load_complete()
    def click_detail_edit_button(self):
        self.click(search['detail_editButton'])
        self.wait_page_load_complete()
    def click_detail_copy_register_button(self):
        self.click(search['detail_copyRegisterButton'])
        self.wait_page_load_complete()
    def input_edit_con_end(self,end_date):
        self.send_key(search['edit_conEndInput'],end_date)
    def click_edit_back_button(self):
        self.click(search['edit_backButton'])
    def click_edit_save_button(self):
        self.click(search['edit_saveButton'],None,False)

    # register
    def input_register_org_id(self, value):
        """
        :param value: 流山
        :return:
        """
        self.send_key(search['register_OrgInput'], value)
        self.press_key(search['register_OrgInput'], "down")
        self.press_key(search['register_OrgInput'], "enter")

    def input_register_course_name(self, value):
        """
        :param value: course_name
        :return:
        """
        self.send_key(search['register_CourseNameInput'], value)

    def input_register_trunk_name(self, value):
        """
        :param value: trunk_name
        :return:
        """
        self.send_key(search['register_TrunkNameInput'], value)

    def input_register_trunk_type(self, type=1):
        """
        :param type: 1:regular 2:irregular 3:regular shuttle 4:irregular shuttle
        :return:
        """
        self.click(search['register_TrunkTypeInput'])
        self.press_key(search['register_TrunkTypeInput'], "down")
        for i in range(type):
            self.press_key(search['register_TrunkTypeInput'], "down")
        self.press_key(search['register_TrunkTypeInput'], "enter")

    def input_register_op_pattern(self, type=1):
        """
        :param type: 1:every day 2:sat,sun 3:mon-fri 4:other
        :return:
        """
        self.click(search['register_PatternInput'])
        self.press_key(search['register_PatternInput'], "down")
        for i in range(0,type):
            self.press_key(search['register_PatternInput'], "down")
        self.press_key(search['register_PatternInput'], "enter")

    def input_register_carrier(self, value):
        """
        :param value: carrier
        :return:
        """
        self.send_key(search['register_CarrierInput'], value)
        self.press_key(search['register_CarrierInput'], "down")
        self.press_key(search['register_CarrierInput'], "enter")

    def input_register_vehicle_type(self, type=1):
        """
        :param type: 1:2t 2:4t 3:10t 4:その他
        :return:
        """
        self.click(search['register_VehicleTypeInput'])
        self.press_key(search['register_VehicleTypeInput'], "down")
        for i in range(type):
            self.press_key(search['register_VehicleTypeInput'], "down")
        self.press_key(search['register_VehicleTypeInput'], "enter")

    def input_register_contract_start_date(self, value):
        """
        :param value: example 202050101
        :return:
        """
        self.driver.implicitly_wait(2)
        self.send_key(search['register_StartDateInput'], value)

    def input_register_contract_end_date(self, value):
        """
        :param value: example 202050101
        :return:
        """
        self.driver.implicitly_wait(2)
        self.send_key(search['register_EndDateInput'], value)

    def input_register_cost(self, value):
        """
        :param value: example 10000
        :return:
        """
        self.driver.implicitly_wait(2)
        self.send_key(search['register_CostInput'], value)

    def input_register_load_weight(self, value):
        """
        :param value: example 10000
        :return:
        """
        self.driver.implicitly_wait(2)
        self.send_key(search['register_LoadWeightInput'], value)

    def input_register_phone_number(self, value):
        """
        :param value: example 09012345678
        :return:
        """
        self.driver.implicitly_wait(2)
        self.send_key(search['register_PhoneNumberInput'], value)

    def input_register_vehicle_number(self, value):
        """
        :param value: example 1234567890
        :return:
        """
        self.driver.implicitly_wait(2)
        self.send_key(search['register_VehicleNumberInput'], value)

    def input_register_driver_name(self, value):
        """
        :param value: example 山田太郎
        :return:
        """
        self.driver.implicitly_wait(2)
        self.send_key(search['register_DriverNameInput'], value)

    def input_register_comment(self, value):
        """
        :param value: example 備考
        :return:
        """
        self.driver.implicitly_wait(2)
        self.send_key(search['register_CommentInput'], value)
    def input_register_irregular_reason(self, type=1):
        """
        :param type: [
            {
                "reasonCode": 1,
                "reasonName": "Shipment volume Incr"
            },
            {
                "reasonCode": 2,
                "reasonName": "Operation Late"
            },
            {
                "reasonCode": 3,
                "reasonName": "Missed when register"
            },
            {
                "reasonCode": 4,
                "reasonName": "Empty Return"
            },
            {
                "reasonCode": 5,
                "reasonName": "Others"
            }
        ]
        :return:
        """
        self.click(search['register_IrregularReason'])
        self.press_key(search['register_IrregularReason'], "down")
        for i in range(type):
            self.press_key(search['register_IrregularReason'], "down")
        self.press_key(search['register_IrregularReason'], "enter")
    def input_register_dp_location(self, value):
        """
        :param value: example 東京
        :return:
        """
        self.driver.implicitly_wait(2)
        self.send_key(search['register_Dp_DpLocationInput'], value)
        self.press_key(search['register_Dp_DpLocationInput'], "down")
        self.press_key(search['register_Dp_DpLocationInput'], "enter")

    def input_register_dp_plan_arrival_time(self, value):
        """
        :param value: example 10:00
        :return:
        """
        self.driver.implicitly_wait(2)
        self.send_key(search['register_Dp_PlanArrivalTimeInput'], value)

    def input_register_dp_plan_departure_time(self, value):
        """
        :param value: example 10:00
        :return:
        """
        self.driver.implicitly_wait(2)
        self.send_key(search['register_Dp_PlanDepartureTimeInput'], value)

    def input_register_ar_location(self, value, card_order=1):
        """
        :param value: example 東京
        :return:
        """
        self.driver.implicitly_wait(2)
        self.send_key(search['register_Ar_LocationInput'], value, str(card_order))
        self.press_key(search['register_Ar_LocationInput'], "down", str(card_order))
        self.press_key(search['register_Ar_LocationInput'], "enter", str(card_order))

    def input_register_ar_plan_arrival_time(self, value, card_order=1):
        """
        :param value: example 10:00
        :return:
        """
        self.driver.implicitly_wait(2)
        self.send_key(search['register_Ar_PlanArrivalTimeInput'], value, str(card_order))

    def input_register_ar_plan_arrival_day(self, value, card_order=1):
        """
        :param value: example 10:00
        :return:
        """
        self.driver.implicitly_wait(2)
        self.send_key(search['register_Ar_PlanArrivalDayInput'], value, str(card_order))

    def input_register_ar_plan_departure_time(self, value, card_order=1):
        """
        :param value: example 10:00
        :return:
        """
        self.driver.implicitly_wait(2)
        self.send_key(search['register_Ar_PlanDepartureTimeInput'], value, str(card_order))

    def input_register_ar_plan_departure_day(self, value, card_order=1):
        """
        :param value: example 10:00
        :return:
        """
        self.driver.implicitly_wait(2)
        self.send_key(search['register_Ar_PlanDepartureDayInput'], value, str(card_order))

    def click_register_ar_delete_icon(self, card_order=1):
        """
        :param card_order: example 1
        :return:
        """
        self.click(search['register_Ar_DeleteIcon'], str(card_order))

    def click_register_add_arrival_item(self):
        """
        :return:
        """
        self.click(search['register_Ar_AddItemButton'],None,False)

    def click_register_back_button(self):
        self.click(search['register_BackButton'])

    def click_register_button(self):
        self.click(search['register_RegisterButton'],None,True)

    def get_register_start_date_error(self):
        return self.get_text(search['register_startDateError'])

    def get_register_end_date_error(self):
        return self.get_text(search['register_endDateError'])

    def get_register_backend_error(self):
        return self.get_text(search['register_backendError'])

    def close_register_backend_error(self):
        self.click(search['register_closeError'],None,False)




if __name__ == '__main__':
    pass
