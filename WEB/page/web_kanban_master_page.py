from common.logger import Logger
from common.readconfig import con
from WEB.base.basepage import Basepage
from common.readelement import Element
from config.config import WEB_ELEMENT_PATH
import os
import time
search = Element(WEB_ELEMENT_PATH, 'web_kanban_master_element')


class WebKanbanMasterPage(Basepage):
    def page_loaded(self):
        self.refresh()
        self.find_element(search['OrgInput'])
    #tab
    def click_shuttle_tab(self):
        self.click(search['shuttleTab'])
    def click_kyokuchokuso_tab(self):
        self.click(search['kyokuchokusoTab'])

    def click_shuttle_add_button(self):
        self.click(search['shuttleAddButton'])
    def click_kyokuchokuso_add_button(self):
        self.click(search['kyokuchokusoAddButton'])
    #shuttle table
    def click_shuttle_delete_icon(self, kanban_id):
        self.click(search['sh_deleteIcon'], [kanban_id, None])

    def get_shuttle_kanban_id(self, kanban_id):
        return self.get_text(search['sh_kanbanId'], dynamic_value=[str(kanban_id),None])

    def input_shuttle_depot(self, depot,kanban_id):
        self.send_key(search['sh_depot'], text=depot,dynamic_value=[str(kanban_id),None])
        self.press_key(search['sh_depot'], "down",dynamic_value=[str(kanban_id),None])
        self.press_key(search['sh_depot'], "enter",dynamic_value=[str(kanban_id),None])

    def input_shuttle_op_type(self, op_type,kanban_id):
        self.send_key(search['sh_opType'], op_type,dynamic_value=[str(kanban_id),None])

    def input_shuttle_remark1(self, remark1,kanban_id):
        self.send_key(search['sh_remark1'], remark1,dynamic_value=[str(kanban_id),None])

    def input_shuttle_end_location(self, end_location,kanban_id):
        self.send_key(search['sh_endLocation'], end_location,dynamic_value=[str(kanban_id),None])

    def input_shuttle_post_no(self, post_no,kanban_id):
        self.send_key(search['sh_postNo'], post_no,dynamic_value=[str(kanban_id),None])

    def input_shuttle_remark2_1(self,color,kanban_id): 
        """
        :param color: W | B | 白 | 黒
        :param kanban_id: kanban_id
        :return:
        """
        current_text = self.get_value(search['sh_remark2_1'], dynamic_value=[str(kanban_id),None])
        if color in ("W","白") and current_text in ("W","白"):
            pass
        elif color in ("B","黒") and current_text in ("B","黒"):
            pass
        else:
            self.click(search['sh_remark2_1'], dynamic_value=[str(kanban_id),None])
            self.press_key(search['sh_remark2_1'], "down",dynamic_value=[str(kanban_id),None])
            self.press_key(search['sh_remark2_1'], "enter",dynamic_value=[str(kanban_id),None])

    def input_shuttle_remark2_2(self, remark2_2,kanban_id):
        self.send_key(search['sh_remark2_2'], remark2_2,dynamic_value=[str(kanban_id),None])
    def input_shuttle_sort_no_1(self,color,kanban_id):
        """
        :param color: W | B | 白 | 黒
        :param kanban_id: kanban_id
        :return:
        """
        current_text = self.get_value(search['sh_sortNo_1'], dynamic_value=[str(kanban_id),None])
        if color in ("W","白") and current_text in ("W","白"):
            pass
        elif color in ("B","黒") and current_text in ("B","黒"):
            pass
        else:
            try:
                self.click(search['sh_sortNo_1'], dynamic_value=[str(kanban_id),None])
                self.press_key(search['sh_sortNo_1'], "down",dynamic_value=[str(kanban_id),None])
                self.press_key(search['sh_sortNo_1'], "enter",dynamic_value=[str(kanban_id),None])
            except:
                pass
        
    def input_shuttle_sort_no_2(self, sort_no_2,kanban_id):
        self.send_key(search['sh_sortNo_2'], sort_no_2,dynamic_value=[str(kanban_id),None])
    def input_shuttle_extra(self, extra,kanban_id):
        self.send_key(search['sh_extra'], extra,dynamic_value=[str(kanban_id),None])
    def input_shuttle_cloud(self, cloud,kanban_id):
        """
        :param cloud:  N 無 Y 有
        :param kanban_id: kanban_id
        :return:
        """
        current_text = self.get_value(search['sh_cloud'], dynamic_value=[str(kanban_id),None])
        if cloud in ("N","無") and current_text in ("N","無"):
            pass
        elif cloud in ("Y","有") and current_text in ("Y","有"):
            pass
        else:
            self.click(search['sh_cloud'], dynamic_value=[str(kanban_id),None])
            self.press_key(search['sh_cloud'], "down",dynamic_value=[str(kanban_id),None])
            self.press_key(search['sh_cloud'], "enter",dynamic_value=[str(kanban_id),None])
        
    def input_shuttle_sheet(self, sheet,kanban_id):
        self.send_key(search['sh_sheet'], sheet,dynamic_value=[str(kanban_id),None])
    #kyokuchokuso table
    def click_kyokuchokuso_delete_icon(self, kanban_id):
        self.click(search['ky_deleteIcon'], [kanban_id, None])
    def get_kyokuchokuso_kanban_id(self, kanban_id):
        return self.get_text(search['ky_kanbanId'], dynamic_value=[str(kanban_id),None])

    def input_kyokuchokuso_sort_no_1(self,value,kanban_id):
        return self.send_key(search['ky_sortNo'], value,dynamic_value=[str(kanban_id),None])

    def input_kyokuchokuso_depot(self, depot,kanban_id):
        self.send_key(search['ky_depot'], depot,dynamic_value=[str(kanban_id),None])
        self.press_key(search['ky_depot'], "down",dynamic_value=[str(kanban_id),None])
        self.press_key(search['ky_depot'], "enter",dynamic_value=[str(kanban_id),None])
    def input_kyokuchokuso_TLName(self, TLName,kanban_id):
        self.send_key(search['ky_TLName'], TLName,dynamic_value=[str(kanban_id),None])
        self.press_key(search['ky_TLName'], "down",dynamic_value=[str(kanban_id),None])
        self.press_key(search['ky_TLName'], "enter",dynamic_value=[str(kanban_id),None])
    def input_kyokuchokuso_route(self, route,kanban_id):
        self.send_key(search['ky_route'], route,dynamic_value=[str(kanban_id),None])
    def input_kyokuchokuso_startingTime(self, startingTime,kanban_id):
        self.send_key(search['ky_startingTime'], startingTime,dynamic_value=[str(kanban_id),None])
    def input_kyokuchokuso_remark(self, remark,kanban_id):
        self.send_key(search['ky_remark'], remark,dynamic_value=[str(kanban_id),None])
    def input_kyokuchokuso_sheet(self, sheet,kanban_id):
        self.send_key(search['ky_sheet'], sheet,dynamic_value=[str(kanban_id),None])
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

    def click_save(self):
        self.click(search['SaveButton'])
        
    def get_popup_hint(self):
        return self.get_text(search['popupHint'])

    def popup_action(self, action=True):
        if action :
            self.click(search['popupButtonYes'])
        else:
            self.click(search['popupButtonNo'])


    

if __name__ == '__main__':
    pass
