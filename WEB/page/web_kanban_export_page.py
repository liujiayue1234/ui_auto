from common.logger import Logger
from common.readconfig import con
from WEB.base.basepage import Basepage
from common.readelement import Element
from config.config import WEB_ELEMENT_PATH
import os
import time
search = Element(WEB_ELEMENT_PATH, 'web_kanban_export_element')


class WebKanbanExportPage(Basepage):
    def page_loaded(self):
        self.refresh()
        self.find_element(search['OrgInput'])
    #tab
    def click_shuttle_tab(self):
        self.click(search['shuttleTab'])
    def click_kyokuchokuso_tab(self):
        self.click(search['kyokuchokusoTab'])
    def input_export_date(self, date):
        self.send_key(search['ExportDateInput'], date)

    def click_export_button(self):
        self.click(search['ExportButton'])
    def click_select_all_button(self):
        self.click(search['selectAllButton'])

    #shuttle table
    def check_shuttle_kanban(self, kanban_id):
        self.click(search['sh_checkbox'], dynamic_value=[str(kanban_id),None])

    def get_shuttle_kanban_id(self, kanban_id):
        return self.get_text(search['sh_kanbanId'], dynamic_value=[str(kanban_id),None])

    def get_shuttle_depot(self, kanban_id):
        return self.get_text(search['sh_depot'], dynamic_value=[str(kanban_id),None])

    def get_shuttle_op_type(self, kanban_id):
        return self.get_text(search['sh_opType'], dynamic_value=[str(kanban_id),None])

    def get_shuttle_remark1(self, kanban_id):
        return self.get_text(search['sh_remark1'], dynamic_value=[str(kanban_id),None])

    def get_shuttle_end_location(self, kanban_id):
        return self.get_text(search['sh_endLocation'], dynamic_value=[str(kanban_id),None])

    def get_shuttle_post_no(self, kanban_id):
        return self.get_text(search['sh_postNo'], dynamic_value=[str(kanban_id),None])

    def get_shuttle_remark2_1(self, kanban_id): 
        return self.get_text(search['sh_remark2_1'], dynamic_value=[str(kanban_id),None])

    def get_shuttle_remark2_2(self, kanban_id):
        return self.get_text(search['sh_remark2_2'], dynamic_value=[str(kanban_id),None])

    def get_shuttle_sort_no_1(self, kanban_id):
        return self.get_text(search['sh_sortNo_1'], dynamic_value=[str(kanban_id),None])
        
    def get_shuttle_sort_no_2(self, kanban_id):
        return self.get_text(search['sh_sortNo_2'], dynamic_value=[str(kanban_id),None])
    def get_shuttle_extra(self, kanban_id):
        return self.get_text(search['sh_extra'], dynamic_value=[str(kanban_id),None])
    def get_shuttle_cloud(self, kanban_id):
        return self.get_text(search['sh_cloud'], dynamic_value=[str(kanban_id),None])
        
    def get_shuttle_sheet(self, kanban_id):
        return self.get_text(search['sh_sheet'], dynamic_value=[str(kanban_id),None])
    #kyokuchokuso table
    def check_kyokuchokuso_kanban(self, kanban_id):
        self.click(search['ky_checkbox'], dynamic_value=[str(kanban_id),None])
    def get_kyokuchokuso_kanban_id(self, kanban_id):
        return self.get_text(search['ky_kanbanId'], dynamic_value=[str(kanban_id),None])

    def get_kyokuchokuso_sort_no(self, kanban_id):
        return self.get_text(search['ky_sortNo'], dynamic_value=[str(kanban_id),None])

    def get_kyokuchokuso_depot(self, kanban_id):
        return self.get_text(search['ky_depot'], dynamic_value=[str(kanban_id),None])

    def get_kyokuchokuso_TLName(self, kanban_id):
        return self.get_text(search['ky_TLName'], dynamic_value=[str(kanban_id),None])

    def get_kyokuchokuso_route(self, kanban_id):
        return self.get_text(search['ky_route'], dynamic_value=[str(kanban_id),None])   

    def get_kyokuchokuso_startingTime(self, kanban_id):
        return self.get_text(search['ky_startingTime'], dynamic_value=[str(kanban_id),None])

    def get_kyokuchokuso_remark(self, kanban_id):
        return self.get_text(search['ky_remark'], dynamic_value=[str(kanban_id),None])

    def get_kyokuchokuso_sheet(self, kanban_id):
        return self.get_text(search['ky_sheet'], dynamic_value=[str(kanban_id),None])
     # search   
    def input_org_id(self, value):
        """
        :param value: example 流山
        :return:
        """
        self.send_key(search['OrgInput'], value)
        self.press_key(search['OrgInput'], "down")
        self.press_key(search['OrgInput'], "enter")
    def input_op_type(self,value):
        """
        :param value: value
        :return:
        """
        self.send_key(search['shuttleOpTypeInput'], value)
    def input_depot(self, value):
        self.send_key(search['DepotInput'], value)
        self.press_key(search['DepotInput'], "down")
        self.press_key(search['DepotInput'], "enter")
        self.press_key(search['DepotInput'], "tab")

    def input_TLName(self, value):
        self.send_key(search['TLNameInput'], value)
        self.press_key(search['TLNameInput'], "down")
        self.press_key(search['TLNameInput'], "enter")
        self.press_key(search['TLNameInput'], "tab")
    def click_search(self):
        self.click(search['SearchButton'])   
        
    def get_popup_hint(self):
        return self.get_text(search['popupHint'])

    def popup_action(self, action=True):
        if action :
            self.click(search['popupButtonYes'])
        else:
            self.click(search['popupButtonNo'])


    

if __name__ == '__main__':
    pass
