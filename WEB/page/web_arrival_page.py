from time import sleep

from common.logger import Logger
from common.readconfig import con
from WEB.base.basepage import Basepage
from common.readelement import Element
from config.config import WEB_ELEMENT_PATH
import os
from config.config import DOWNLOAD_PATH
import time
from datetime import datetime

search = Element(WEB_ELEMENT_PATH, 'web_arrival_element')


class WebArrivalPage(Basepage):
    def input_org_id(self, value):
        """
        :param value: 流山
        :return:
        """
        self.wait_page_load_complete()
        self.send_key(search['OrgInput'], value)
        self.press_key(search['OrgInput'], "down")
        self.press_key(search['OrgInput'], "enter")

    def input_op_date(self, value):
        """
        :param value: example 202050101
        :return:
        """
        self.driver.implicitly_wait(2)
        self.send_key(search['OpDateInput'], value)

    def input_confirm_status(self, confirm=True):
        """
        :param confirm: True
        :return:
        """
        self.click(search['ConfirmStatusInput'])
        self.press_key(search['ConfirmStatusInput'], "down")
        self.press_key(search['ConfirmStatusInput'], "down")
        if not confirm:
            self.press_key(search['ConfirmStatusInput'], "down")
        self.press_key(search['ConfirmStatusInput'], "enter")

    def input_error_status(self, value):
        """
        :param value: example [1,1,1] 1:select 0:unselect, three parameters represent three options: No error｜Late|Unloading mismatch
        :return:
        """
        self.click(search['ErrorStatusInput'],None,False)
        self.press_key(search['ErrorStatusInput'], "down")
        if value[0]:
            self.press_key(search['ErrorStatusInput'], "enter")
        self.press_key(search['ErrorStatusInput'], "down")
        if value[1]:
            self.press_key(search['ErrorStatusInput'], "enter")
        self.press_key(search['ErrorStatusInput'], "down")
        if value[2]:
            self.press_key(search['ErrorStatusInput'], "enter")
        self.press_key(search['ErrorStatusInput'], "tab")

    def input_op_status(self, value):
        """
        :param value: example [1,1,1] 1:select 0:unselect, three parameters represent three options: Not started|Ongoing|Finished
        :return:
        """
        self.click(search['OpStatusInput'],None,False)
        self.press_key(search['OpStatusInput'], "down")
        if value[0]:
            self.press_key(search['OpStatusInput'], "enter")
        self.press_key(search['OpStatusInput'], "down")
        if value[1]:
            self.press_key(search['OpStatusInput'], "enter")
        self.press_key(search['OpStatusInput'], "down")
        if value[2]:
            self.press_key(search['OpStatusInput'], "enter")
        self.press_key(search['OpStatusInput'], "tab")

    def input_trunk_type(self, type=1):
        """
        :param type: 1:regular 2:irregular 3:regular shuttle 4:irregular shuttle
        :return:
        """
        self.click(search['TrunkTypeInput'],None,False)
        self.press_key(search['TrunkTypeInput'], "down")
        for i in range(type):
            self.press_key(search['TrunkTypeInput'], "down")
        self.press_key(search['TrunkTypeInput'], "enter")

    def input_course_name(self, value):
        """
        :param value: course_name
        :return:
        """
        self.send_key(search['CourseNameInput'], value)

    def input_trunk_name(self, value):
        """
        :param value: trunk_name
        :return:
        """
        self.send_key(search['TrunkNameInput'], value)

    def input_carrier(self, value):
        """
        :param value: carrier
        :return:
        """
        self.send_key(search['CarrierInput'], value)
        self.press_key(search['CarrierInput'], "down")
        self.press_key(search['CarrierInput'], "enter")
        self.press_key(search['CarrierInput'], "tab")

    def click_search(self, ):
        self.click(search['SearchButton'])

    def csv_export(self, start_date, end_date):
        """
        :param start_date: example 20250101
        :param end_date: example 20250101
        :return:
        """
        self.send_key(search['CSVStartDate'], start_date)
        self.send_key(search['CSVEndDate'], end_date)
        self.click(search['CSVExportButton'])

        # Check if the csv file is downloaded to the specified path
        csv_file = os.path.join(DOWNLOAD_PATH, f"Confidential_Trunk_Line_Operation_History_{start_date}-{end_date}.csv")

        # Wait for the file to appear
        max_wait = 30  # Max wait 30 seconds
        wait_time = 0
        while wait_time < max_wait:
            if os.path.exists(csv_file):
                break
            time.sleep(1)
            wait_time += 1
        with open(csv_file, "r", encoding='utf-8') as f:
            content = f.readlines()
        Logger.info(f"CSV file has been successfully downloaded to: {csv_file}")  # type: ignore

    def open_register_irregular_page(self):
        self.wait_page_load_complete()
        self.click(search['RegisterButton'])
        self.wait_page_load_complete()

    def confirm_trunk_line(self, trunk_line_id=None):
        if trunk_line_id:
            self.click(search['Checkbox'], trunk_line_id,False)
        else:
            self.click(search['SelectAllButton'])

    def click_save(self):
        self.click(search['SaveButton'])

    def trunk_card_exist(self, trunk_id):
        self.wait_loading_icon_disappear()
        try:
            return self.check_element_exist(search["FirstCard"], str(trunk_id), 3)
        except Exception as e:
            return False

    def check_cancel_button_enabled(self, trunk_id):
        if self.check_element_enabled(search['CancelButton'], str(trunk_id)):
            return True
        return False

    def cancel_trunk(self, trunk_id):
        self.click(search['CancelButton'], str(trunk_id),wait_loading=False)
        self.handle_cancel_popup(Yes=True)

    def handle_cancel_popup(self, Yes=True):
        if Yes:
            self.click(search['YesButtonInAlert'],None)
            return
        self.click(search['NoButtonInAlert'],None)

    def get_card_count(self):
        return self.elements_num(search["Card"])

    def click_show_button(self, trunk_id):
        self.click(search["ShowButton"], str(trunk_id))

    def click_hide_button(self, trunk_id):
        self.click(search["HideButton"], str(trunk_id))

    def open_actual_arrival_departure_detail(self, trunk_id):
        self.wait_page_load_complete()
        self.click(search["NameButton"], str(trunk_id))
        self.enter_into_new_page(close_current=False)

    # arrival & departure detail
    def get_detail_trunk_id(self):
        return self.get_text(search['detail_Trunkid'])

    def get_detail_op_date(self):
        return self.get_text(search['detail_OpDate'])

    def get_detail_trunk_name(self):
        return self.get_text(search['detail_TrunkName'])

    def get_detail_trunk_type(self):
        return self.get_text(search['detail_TrunkType'])

    def get_detail_op_pattern(self):
        return self.get_text(search['detail_OpPattern'])

    def get_detail_carrier(self):
        return self.get_text(search['detail_Carrier'])

    def get_detail_vh_type(self):
        return self.get_text(search['detail_VhType'])

    def get_detail_con_start(self):
        return self.get_text(search['detail_ConStart'])

    def get_detail_con_end(self):
        return self.get_text(search['detail_ConEnd'])

    def get_detail_cost(self):
        return self.get_text(search['detail_Cost'])

    def get_detail_weight(self):
        return self.get_text(search['detail_Weight'])

    def get_detail_phone(self):
        return self.get_text(search['detail_PhoneNum'])

    def get_detail_vh_number(self):
        return self.get_text(search['detail_VhNum'])

    def get_detail_comment(self):
        return self.get_text(search['detail_Comment'])

    def get_detail_driver_name(self):
        return self.get_text(search['detail_DriverName'])

    def get_detail_dp_plan_arrival_time(self):
        return self.get_text(search['detail_Dp_PlanArTime'])

    def get_detail_dp_plan_depart_time(self):
        return self.get_text(search['detail_Dp_PlanDpTime'])

    def get_detail_dp_actual_arrival_time(self):
        return self.get_text(search['detail_Dp_ActualArTime'])

    def get_detail_dp_actual_depart_time(self):
        return self.get_text(search['detail_Dp_ActualDpTime'])

    def get_detail_dp_cart(self):
        return self.get_text(search['detail_Dp_cart'])

    def get_detail_ar_scan_cart(self, cart_order):
        return self.get_text(search['detail_Ar_scanCart'], str(cart_order))

    def get_detail_ar_unload_cart(self, cart_order):
        return self.get_text(search['detail_Ar_unloadCart'], str(cart_order))

    def get_detail_ar_plan_arrival_time(self, cart_order):
        return self.get_text(search['detail_Ar_planArTime'], str(cart_order))

    def get_detail_ar_plan_arrival_date(self, cart_order):
        return self.get_text(search['detail_Ar_planArDate'], str(cart_order))

    def get_detail_ar_plan_depart_time(self, cart_order):
        return self.get_text(search['detail_Ar_planDpTime'], str(cart_order))

    def get_detail_ar_plan_depart_date(self, cart_order):
        return self.get_text(search['detail_Ar_planDpDate'], str(cart_order))

    def get_detail_ar_actual_arrival_time(self, cart_order):
        return self.get_text(search['detail_Ar_actualArTime'], str(cart_order))

    def get_detail_ar_actual_depart_time(self, cart_order):
        return self.get_text(search['detail_Ar_actualDpTime'], str(cart_order))

    def click_back_in_detail(self):
        self.click(search['detail_backButton'])
        self.wait_page_load_complete()

    def click_edit_in_detail(self):
        self.click(search['detail_editButton'])
        self.wait_page_load_complete()

    # edit arrival & departure data
    def input_edit_comment(self, value):
        """
        :param value: comment
        :return:
        """
        self.send_key(search['edit_CommentInput'], value)

    def input_edit_phone_number(self, value):
        """
        :param value: phone number
        :return:
        """
        self.driver.implicitly_wait(2)
        self.send_key(search['edit_PhoneNumberInput'], value)

    def input_edit_vehicle_number(self, value):
        """
        :param value: vehicle number
        :return:
        """
        self.send_key(search['edit_VehicleNumberInput'], value)

    def input_edit_driver_name(self, value):
        """
        :param value: driver name
        :return:
        """
        self.send_key(search['edit_DriverNameInput'], value)

    def input_edit_dp_actual_departure_time(self, year, month, day, hour, minute):
        """
        :param year: year 2025
        :param month: month 08
        :param day: day 20
        :param hour: hour 20
        :param minute: minute 05
        :return:
        """
        #get current value
        sleep(2)
        current_value = self.get_edit_dp_departure_time()
        Logger.info("Current actual departure time:"+current_value)
        if current_value:
            current_year = int(current_value.split(" ")[0].split("/")[0])
            current_month = int(current_value.split(" ")[0].split("/")[1])
        else:
            current_year = int(datetime.now().year)
            current_month = int(datetime.now().month)
        self.click(search['edit_Dp_timePicker'],None,False)
        # get current year and month
        Logger.info("Current year:"+str(current_year))
        Logger.info("Expected year:"+str(year))

        Logger.info("Current_month:"+str(current_month))
        Logger.info("Expected month:"+str(int(month)))
        times = (int(year)*12+int(month))-(current_year*12+current_month)
        Logger.info("Times:" + str(int(times)))
        if times > 0:
            for i in range(times):
                self.click(search['edit_NextMonthPicker'],None,False)
        elif times < 0:
            for i in range(-times):
                self.click(search['edit_LastMonthPicker'],None,False)
        else:
            pass
        sleep(1)
        self.click(search['edit_DayPicker'], str(day),False)
        sleep(1)
        if int(hour) == 0:
            hour = "00"
        self.transform_click(search['edit_HourPicker'], str(hour))
        sleep(1)
        if int(minute) == 0:
            minute = "00"
        elif int(minute) % 5 != 0:
            minute = int(minute) - (int(minute) % 5)
        self.transform_click(search['edit_MinutePicker'], str(minute))

    def input_edit_departure_cart(self, cart_num):
        self.send_key(search['edit_Dp_loadedCarInput'], cart_num)

    def input_edit_ar_arrival_time(self, card_order, year, month, day, hour, minute):
        """
        :param year: year 2025
        :param month: month 08
        :param day: day 20
        :param hour: hour 20
        :param minute: minute 05
        :return:
        """
        sleep(2)
        current_value = self.get_edit_ar_actual_arrival_time(card_order)
        Logger.info("Current arrival card - actual arrival time:" + current_value)
        if current_value:
            current_year = int(current_value.split(" ")[0].split("/")[0])
            current_month = int(current_value.split(" ")[0].split("/")[1])
        else:
            current_year = int(datetime.now().year)
            current_month = int(datetime.now().month)
        self.click(search['edit_Ar_arrivalTimePicker'], str(card_order),False)

        Logger.info("Current year:" + str(current_year))
        Logger.info("Expected year:" + str(year))

        Logger.info("Current_month:" + str(current_month))
        Logger.info("Expected month:" + str(int(month)))
        times = (int(year) * 12 + int(month)) - (current_year * 12 + current_month)
        Logger.info("Times:" + str(int(times)))
        if times > 0:
            for i in range(times):
                self.click(search['edit_NextMonthPicker'],None,False)
        elif times < 0:
            for i in range(-times):
                self.click(search['edit_LastMonthPicker'],None,False)
        self.click(search['edit_DayPicker'], str(day),False)
        if int(hour) == 0:
            hour = "00"
        self.transform_click(search['edit_HourPicker'], str(hour))
        if int(minute) == 0:
            minute = "00"
        elif int(minute) % 5 != 0:
            minute = int(minute) - (int(minute) % 5)
        self.transform_click(search['edit_MinutePicker'], str(minute))

    def input_edit_ar_departure_time(self, card_order, year, month, day, hour, minute):
        """
        :param year: year 2025
        :param month: month 08
        :param day: day 20
        :param hour: hour 20
        :param minute: minute 05
        :return:
        """
        sleep(2)
        current_value = self.get_edit_ar_actual_depart_time(card_order)
        Logger.info("Current arrival card - actual depart time:" + current_value)
        if current_value:
            current_year = int(current_value.split(" ")[0].split("/")[0])
            current_month = int(current_value.split(" ")[0].split("/")[1])
        else:
            current_year = int(datetime.now().year)
            current_month = int(datetime.now().month)
        self.click(search['edit_Ar_departureTimePicker'], str(card_order),False)

        Logger.info("Current year:" + str(current_year))
        Logger.info("Expected year:" + str(year))

        Logger.info("Current_month:" + str(current_month))
        Logger.info("Expected month:" + str(int(month)))
        times = (int(year) * 12 + int(month)) - (current_year * 12 + current_month)
        Logger.info("Times:" + str(int(times)))
        if times > 0:
            for i in range(times):
                self.click(search['edit_NextMonthPicker'],None,False)
        elif times < 0:
            for i in range(-times):
                self.click(search['edit_LastMonthPicker'])
        self.click(search['edit_DayPicker'], str(day),False)
        if int(hour) == 0:
            hour = "00"
        self.transform_click(search['edit_HourPicker'], str(hour))
        if int(minute) == 0:
            minute = "00"
        elif int(minute) % 5 != 0:
            minute = int(minute) - (int(minute) % 5)
        self.transform_click(search['edit_MinutePicker'], str(minute))

    def input_edit_ar_scan_cart(self, card_order, cart_num):
        """
        card_order : is used to locate the card
        cart_num: is the inputted value
        """
        self.send_key(search['edit_Ar_scannedCartInput'], str(cart_num), str(card_order))

    def input_edit_ar_unload_cart(self, card_order, cart_num):
        self.send_key(search['edit_Ar_unloadedCartInput'], str(cart_num), str(card_order))

    def get_edit_trunk_id(self):
        """
        :return: trunk id
        """
        return self.get_text(search['edit_TrunkIdText'])

    def get_edit_course_name(self):
        """
        :return: course name
        """
        return self.get_text(search['edit_CourseNameText'])

    def get_edit_trunk_name(self):
        """
        :return: trunk name
        """
        return self.get_text(search['edit_TrunkNameText'])

    def get_edit_trunk_type(self):
        """
        :return: trunk type
        """
        return self.get_text(search['edit_TrunkTypeText'])

    def get_edit_op_pattern(self):
        """
        :return: op pattern
        """
        return self.get_text(search['edit_OpPatternText'])

    def get_edit_carrier(self):
        """
        :return: carrier
        """
        return self.get_text(search['edit_CarrierText'])

    def get_edit_vh_type(self):
        """
        :return: vh type
        """
        return self.get_text(search['edit_VhTypeText'])

    def get_edit_cost(self):
        """
        :return: cost
        """
        return self.get_text(search['edit_CostText'])

    def click_edit_back_button(self):
        self.click(search['edit_backButton'])

    def click_edit_save_button(self):
        self.click(search['edit_saveButton'],None,False)


    def handle_edit_confirm(self, yes=True):
        if yes:
            self.click(search['edit_YesButton'],None,True)
            Logger.info("Click on yes button in edit page popup")
            return
        self.click(search['edit_NoButton'],None,True)

    def get_edit_confirm_hint(self):
        return self.get_text(search['edit_Confirm_hint'])

    def get_edit_dp_departure_time(self):
        return self.get_value(search['edit_Dp_actualDpTime'])
        #return self.get_text(search['edit_Dp_actualDpTime'])

    def get_edit_ar_actual_arrival_time(self,card_order):
        return self.get_value(search['edit_Ar_actualArTime'],str(card_order))

    def get_edit_ar_actual_depart_time(self,card_order):
        return self.get_value(search['edit_Ar_actualDpTime'],str(card_order))
if __name__ == '__main__':
    pass
