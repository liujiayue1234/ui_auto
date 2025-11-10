import datetime,timedelta
from logging import setLogRecordFactory
from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import LOCATE_MODE_WEB
from common.logger import Logger
from selenium.webdriver.support.ui import Select
import time
from common.readelement import Element
from config.config import WEB_ELEMENT_PATH,DOWNLOAD_PATH
from selenium.webdriver.common.keys import Keys
import platform
from selenium.webdriver.common.by import By
import os
import csv
import glob
import pdfplumber
from typing import List

search = Element(WEB_ELEMENT_PATH, 'web_login_element')


class Basepage(object):
    """
    All other pages require to inherit Basepage
    """

    def __init__(self, driver):
        self.driver = driver
        self.timeout = 30
        self.poll_frequency = 1
        self.wait = WebDriverWait(self.driver, self.timeout,self.poll_frequency)

    def find_element(self, locator, dynamic_value=None):
        """Find one element"""
        key, value = self.handle_locator(locator, dynamic_value)
        try:
            self.wait_page_load_complete()
            element = self.wait.until(EC.visibility_of_element_located((LOCATE_MODE_WEB[key], value)))
            Logger.info("Locate to the element: {}".format((key, value)))

        except Exception as e:
            element = self.driver.find_element(LOCATE_MODE_WEB[key], value)
            Logger.error("Failed to find the element: {}".format((key, value)))
        return element

    def find_elements(self, locator, dynamic_value=None):
        """Find multiple elements, wait until at least one appears"""
        key, value = self.handle_locator(locator, dynamic_value)
        try:
            self.wait_page_load_complete()
            # wait until at least one element appears   
            self.wait.until(EC.presence_of_element_located((LOCATE_MODE_WEB[key], value)))
            # then find all elements
            elements = self.driver.find_elements(LOCATE_MODE_WEB[key], value)
            Logger.info("Locate to the elements: {}".format((key, value)))
            return elements
        except Exception as e:
            Logger.error("Failed to find the elements: {}".format((key, value)))
            raise

    def elements_num(self, locator, dynamic_value=None):
        """Get account of the same elements"""
        self.wait_page_load_complete()
        number = len(self.find_elements(locator, dynamic_value))
        Logger.info("The same elements:{}".format((locator, number)))
        return number

    def click(self, locator, dynamic_value=None,wait_loading=True):
        key, value = self.handle_locator(locator, dynamic_value)
        try:
            element = WebDriverWait(self.driver, 5, self.poll_frequency).until(
                EC.presence_of_element_located((LOCATE_MODE_WEB[key], value)))
            element.click()
            Logger.info("Click element by selenium: {}".format((key, value)))
        except Exception as e:
            self.driver.execute_script("arguments[0].click();",
                                            self.driver.find_element(LOCATE_MODE_WEB[key], value))
            Logger.info("Click element by JS: {}".format((LOCATE_MODE_WEB[key], value)))
        if wait_loading:
            self.wait_loading_icon_disappear()
            self.wait_page_load_complete()
            self.close_network_error()
    def transform_click(self, locator, dynamic_value=None):
        element = self.find_element(locator, dynamic_value)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(1)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().perform()
    def on_page(self, page_title):
        return page_title in self.driver.title

    def set_win_size(self, width=None, height=None):
        if width and height:
            self.driver.set_window_size(width, height)
        else:
            self.driver.maximize_window()

    def get_url(self, base_url):
        """Open the url then verify"""
        self.set_win_size()
        self.driver.set_page_load_timeout(60)
        try:
            self.driver.get(base_url)
            self.driver.implicitly_wait(10)
            Logger.info("Open the url:{}".format(base_url))
            self.wait_page_load_complete()
        except TimeoutException:
            raise TimeoutException("Open {} time out".format(base_url))

    def switch_frame(self, loc):
        self.wait_page_load_complete()
        return self.driver.switch_to.frame(loc)

    def script(self, src):
        self.wait_page_load_complete()
        self.driver.execute_script(src)

    def refresh(self):
        """Refresh page """
        self.driver.refresh()
        self.wait_loading_icon_disappear()
        self.wait_page_load_complete()
        self.driver.implicitly_wait(30)

    def send_key(self, locator, text, dynamic_value=None):
        """Clear , then input """
        ele = self.find_element(locator, dynamic_value)
        try:
            ele.clear()
        except Exception:
            pass  # For elements that 'clear' doesn't work

        try:
            self.driver.execute_script("arguments[0].value = '';", ele)
        except Exception:
            pass  # For elements that doesn't support JS

        try:
        # Select all than clear
            ele.click()
            if platform.system() == "Darwin":
                ele.send_keys(Keys.COMMAND, 'a')
            else:
                ele.send_keys(Keys.CONTROL, 'a')
            ele.send_keys(Keys.BACKSPACE)
        except Exception:
            pass
        ele.send_keys(text)
        Logger.info("Input text: {}".format(text))

    def focus(self, locator, dynamic_value=None):
        target = self.find_element(locator, dynamic_value)
        self.driver.execute_script("arguments[0].scrollIntoView();", target)

    def option(self, locator, dynamic_value=None):
        select = self.driver.find_element(locator, dynamic_value)
        Select(select).select_by_index(1)

    def get_text(self, locator, dynamic_value=None):
        """Get text"""
        _text = self.find_element(locator, dynamic_value).text
        Logger.info("Get text:{}".format(_text))
        return _text

    def get_value(self, locator, dynamic_value=None):
        """Get value"""
        key, value = self.handle_locator(locator, dynamic_value)
        ele = WebDriverWait(self.driver, 5, self.poll_frequency).until(EC.presence_of_element_located((LOCATE_MODE_WEB[key], value)))
        value = ele.get_attribute("value")
        if value.strip()=="":
            value = self.driver.execute_script("return arguments[0].value;", ele)
        Logger.info("Get value:{}".format(value))
        return value

    def handle_alert(self, option_accept=True):
        alert = self.driver.switch_to.alert
        if option_accept:
            alert.accpet()
        else:
            alert.dismiss()

    def enter_into_new_page(self, close_current=True):
        original_win = self.driver.current_window_handle
        all_win = self.driver.window_handles
        for win in all_win:
            if win == original_win and close_current:
                self.driver.close()
            elif win != original_win:
                self.driver.switch_to.window(win)
                self.wait_page_load_complete()
                break

    def press_key(self, locator, key="up",dynamic_value=None):
        element = self.find_element(locator,dynamic_value)
        if key.lower() == "up":
            element.send_keys(Keys.ARROW_UP)
        elif key.lower() == "down":
            element.send_keys(Keys.ARROW_DOWN)
        elif key.lower() == "left":
            element.send_keys(Keys.ARROW_LEFT)
        elif key.lower() == "right":
            element.send_keys(Keys.ARROW_RIGHT)
        elif key.lower() == "enter":
            element.send_keys(Keys.ENTER)
        elif key.lower() == "home":
            element.send_keys(Keys.HOME)
        elif key.lower() == "end":
            element.send_keys(Keys.END)
        elif key.lower() == "delete":
            element.send_keys(Keys.DELETE)
        elif key.lower() == "backspace":
            element.send_keys(Keys.BACK_SPACE)
        elif key.lower() == "tab":
            element.send_keys(Keys.TAB)
        else:
            Logger.error("Unsupported key: " + key) # type: ignore

    def get_date_with_offset(self,Delimiter='',offset=0):
        current_date = datetime.datetime.now()  
        offset_date = current_date + datetime.timedelta(days=offset)
        return offset_date.strftime("%Y"+Delimiter+"%m"+Delimiter+"%d")

    def read_csv_file(self, file_name, trunk_name):
        matching_rows = []
        file_path_pattern = os.path.join(DOWNLOAD_PATH, f"*{file_name}*.csv")
        matching_files = glob.glob(file_path_pattern)

        if not matching_files:
            raise ValueError(f"No CSV file matching '{file_name}' found in {DOWNLOAD_PATH}")

        # get the latest file
        file_path = max(matching_files, key=os.path.getmtime)

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                next(csv_reader, None)  # skip the first row
                for row in csv_reader:
                    if len(row) > 3 and row[3].strip() in (trunk_name,("'"+trunk_name)):
                        matching_rows.append(row)
        except Exception as e:
            raise ValueError(f"Error reading {file_path}: {e}")
        Logger.info("CSV result:"+str(matching_rows))
        return matching_rows

    def extract_text_from_pdf(self,file_name):
        file_path_pattern = os.path.join(DOWNLOAD_PATH, f"*{file_name}*.pdf")
        pdf_files = glob.glob(file_path_pattern, recursive=True)

        matching_files = [f for f in pdf_files if file_name.lower() in os.path.basename(f).lower()]
        if not matching_files:
            return f"No PDF files found containing '{file_name}'"

        # Get the latest file
        latest_pdf = max(matching_files, key=os.path.getmtime)
        # Extract text
        text_content = ""
        try:
            with pdfplumber.open(latest_pdf) as pdf:
                for page in pdf.pages:
                    text_content += page.extract_text() or ""
            return text_content
        except Exception as e:
            return f"Failed to extract text from {latest_pdf}: {e}"
    def get_title(self):
        self.wait_page_load_complete()
        return self.driver.title

    def check_element_enabled(self, locator, dynamic_value=None):
        element = self.find_element(locator, dynamic_value)
        return element.is_enabled()

    def check_element_exist(self,locator, dynamic_value=None,time_limit=5):
        key, value = self.handle_locator(locator, dynamic_value)
        try:
            WebDriverWait(self.driver, time_limit, self.poll_frequency).until(EC.presence_of_element_located((LOCATE_MODE_WEB[key], value)))
            return True
        except Exception as e:
            return False
    def wait_loading_icon_disappear(self):
        try:
            for i in range(120):
                if self.check_element_exist(search['RefreshIcon'],None,1):
                    sleep(1)
                else:
                    return
        except Exception as e:
            pass
    def close_network_error(self):
        key, value = search["NetworkError"]
        try:
            WebDriverWait(self.driver, 0.5,self.poll_frequency).until(EC.presence_of_element_located((LOCATE_MODE_WEB[key], value)))
            self.click(search['NetworkErrorClose'])
        except:
            pass
    def wait_page_load_complete(self):
        try:
            self.driver.implicitly_wait(2)
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME,"body")))
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        except TimeoutException:
            Logger.error("Time out for page loading.")

    def element_is_checked(self,locator,dynamic_value=None):
        key, value = self.handle_locator(locator,dynamic_value)
        try:
            e=WebDriverWait(self.driver, 5, self.poll_frequency).until(
                EC.element_to_be_clickable((LOCATE_MODE_WEB[key], value)))
            return e.is_selected()
        except Exception as e:
            return False

    def handle_locator(self,locator,dynamic_value=None):
        """
        dynamic_value: example [value1,value2] ,#### of locator will be replaced by value1 , @@@@ of locator will be replaced by value2
        """
        key, value = locator
        if dynamic_value is None:
            pass
        elif isinstance(dynamic_value, str):
            value = value.replace("####", dynamic_value)
        elif isinstance(locator, (tuple, list)) and len(locator) >= 2:
            if "####" in value:
                value = value.replace("####", dynamic_value[0])
            if "@@@@" in value:
                value = value.replace("@@@@", dynamic_value[1])
        Logger.info("Locator-method :"+str(key))
        Logger.info("Locator-value :"+str(value))
        return key,value

    # Common functions
    def logout(self):
        """
        Common for all pages
        :return:
        """
        self.click(search['logoutIcon'])
        time.sleep(1)
        self.click(search['logoutOption'])

    def change_to_JP(self, ):
        """
        Common for all pages
        :return:
        """
        self.click(search['languageButton'])
        self.click(search['JPOption'])

    def change_to_EN(self, ):
        """
        Common for all pages
        :return:
        """
        self.click(search['languageButton'])
        self.click(search['ENOption'])

    def enter_sub_page(self, page_no):
        """
        Input page number ,then go to corresponding page
        :param page_no: 1~Actual arrival , 2~Trunk overview , 3~Operation schedule , 4~Kanban export , 5~Kanban master , 6~User master
        :return:
        """
        self.click(search['Sidebar'])
        if page_no == 1:
            self.click(search['SidebarActualArrival'])
        elif page_no == 2:
            self.click(search['SidebarTrunkOverview'])
        elif page_no == 3:
            self.click(search['SidebarOperationSchedule'])
        elif page_no == 4:
            self.click(search['SidebarKanbanExport'])
        elif page_no == 5:
            self.click(search['SidebarKanbanMaster'])
        elif page_no == 6:
            self.click(search['SidebarUserMaster'])
        else:
            Logger.error("No such pages") # type: ignore
        self.wait_page_load_complete()
        self.click(search['Sidebar'])


if __name__ == '__main__':
    pass
