from common.logger import Logger
from common.readconfig import con
from WEB.base.basepage import Basepage
from common.readelement import Element
from config.config import WEB_ELEMENT_PATH
import os
import time
search = Element(WEB_ELEMENT_PATH, 'web_operation_schedule_element')


class WebOperationSchedulePage(Basepage):
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

    def input_month(self, value):
        """
        :param value: example 202050101
        :return:
        """
        self.driver.implicitly_wait(2)
        self.send_key(search['OpMonthInput'], value)

    
    def click_search(self):
        self.click(search['SearchButton'])

    def click_save(self):
        self.click(search['SaveButton'])
    def get_popup_title(self):
        return self.get_text(search['popup_title'])
        
    def get_popup_hint(self):
        return self.get_text(search['popup_hint'])

    def popup_action(self, action=True):
        if action :
            self.click(search['popup_button_yes'])
        else:
            self.click(search['popup_button_no'])


    def check_one_month_of_one_trunk(self, trunk_line_id):
        """
        :param trunk_line_id: trunk line id
        :return:
        """
        self.click(search['selectOneMonthOfOneTrunk'], trunk_line_id)

    def check_one_date_of_one_trunk(self, trunk_line_id, date):
        """
        :param trunk_line_id: trunk line id
        :param date: date 2025-07-01
        :return:
        """
        self.click(search['selectOneDateOfOneTrunk'], [trunk_line_id, date])

    def check_all_date_of_all_trunk(self):
        self.click(search['selectAllDateAllTrunk'])
    
    def check_one_date_of_all_trunk(self, date_order):
        """
        :param date_order: date order,1-31
        :return:
        """
        self.click(search['selectOneDateAllTrunk'], str(int(date_order)+6))
    def trunk_line_exist(self, trunk_id):
        self.wait_loading_icon_disappear()
        try:
            return self.check_element_exist(search['trunkName'], trunk_id, 2)
        except Exception as e:
            return False
    def checked_status_one_month_one_trunk(self,trunk_id):
        value = self.get_value(search['selectOneMonthOfOneTrunk'],trunk_id)
        if value.lower()=='true':
            return True
        return False

    def checked_status_one_date_one_trunk(self,trunk_id,date):
        value = self.get_value(search['selectOneMonthOfOneTrunk'],[trunk_id,str(date)])
        if value.lower()=='true':
            return True
        return False
    def checked_status_all_date_all_trunk(self):
        value = self.get_value(search['selectAllDateAllTrunk'],None)
        if value.lower()=='true':
            return True
        return False
    def checked_status_one_date_all_trunk(self,date_order):
        value = self.get_value(search['selectOneDateAllTrunk'],str(6+int(date_order)))
        if value.lower()=='true':
            return True
        return False
    def click_trunk_name_enter_detail(self,trunk_id):
        self.click(search['trunkName'],trunk_id)
        self.wait_page_load_complete()

if __name__ == '__main__':
    pass
