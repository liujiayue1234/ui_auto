import time
from common.readconfig import con
from APP.base.basepage import BasePage
from common.readelement import Element
from config.config import APP_ELEMENT_PATH
from common.logger import Logger
from APP.page import app_login_page
import datetime

# Load elements
search = Element(APP_ELEMENT_PATH, 'android_app_operationID_element')


class OperationIDPage(BasePage):
    def __init__(self, driver):
        """Initialize LoginPage with Appium WebDriver."""
        super().__init__(driver)

    def input_trunkline_id(self, value):
        self.send_key(search['OperationIDInput'], value)

    def select_date(self, expected_date=datetime.datetime.now().strftime("%Y/%m/%d")):
        """
        Pick date in 'Operation ID' screen
        :param expected_date: Inputted date format : YYYY/MM/DD
        :return:
        """
        current_date_list = self.get_text(search['Date']).split("/")
        expected_date_list = expected_date.split("/")
        if current_date_list == expected_date_list:
            Logger.info("Date selected : keep default date " + expected_date)
            return
        # Date picker order of Android app: month | day | year
        self.click(search['Date'])
        self.press_key("right")
        # Scroll month
        cnt = int(expected_date_list[1]) - int(current_date_list[1])
        if cnt > 0:
            for i in range(abs(cnt)):
                self.press_key("down")
        elif cnt < 0:
            for i in range(abs(cnt)):
                self.press_key("up")
        self.press_key("right")
        # Scroll day
        cnt = int(expected_date_list[2]) - int(current_date_list[2])
        if cnt > 0:
            for i in range(abs(cnt)):
                self.press_key("down")
        elif cnt < 0:
            for i in range(abs(cnt)):
                self.press_key("up")
        self.press_key("right")
        # Scroll year
        cnt = int(expected_date_list[0]) - int(current_date_list[0])
        if cnt > 0:
            for i in range(abs(cnt)):
                self.press_key("down")
        elif cnt < 0:
            for i in range(abs(cnt)):
                self.press_key("up")
        self.press_key("right")
        self.press_key("enter")
        result = self.get_text(search['Date'])
        if result == expected_date:
            Logger.info("Date selected:" + result)
        else:
            Logger.error(
                "Date selected with error! expected date is [" + expected_date + "],result is [" + result + "]")

    def click_confirm(self):
        self.click(search['ConfirmButton'])

    def get_course_trunk_name(self):
        return self.get_text(search['CourseTrunkName'])

    def get_error_msg(self):
        return self.get_text(search['ErrorPopupMessage'])

    def close_not_exist_error(self):
        self.click(search['ErrorPopupOKButton'])

    def get_complete_msg(self):
        return self.get_text(search['CompleteMessage'])

    def close_complete_popup(self):
        self.click(search['CompleteCloseButton'])
