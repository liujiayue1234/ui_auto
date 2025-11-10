from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config.config import LOCATE_MODE_APP
from common.logger import Logger

from config.config import APP_ELEMENT_PATH
from common.readelement import Element

search = Element(APP_ELEMENT_PATH, 'android_app_login_element')


class BasePage:
    """
        All other pages require to inherit basepage
        """

    def __init__(self, driver):
        self.driver = driver
        self.timeout = 30
        self.wait = WebDriverWait(self.driver, self.timeout)

    def find_element(self, locator):
        """Find one element."""
        key, value = locator
        try:
            element = self.wait.until(EC.presence_of_element_located((LOCATE_MODE_APP[key], value)))
            Logger.info("Locate to the element: {}".format(locator))
            return element
        except Exception as e:
            Logger.error("Failed to find the element: {}".format(locator))
            raise

    def find_elements(self, locator):
        """Find multiple elements."""
        key, value = locator
        try:
            element = self.wait.until(EC.presence_of_element_located((LOCATE_MODE_APP[key], value)))
            Logger.info("Locate to the element: {}".format(locator))
            return element
        except Exception as e:
            Logger.error("Failed to find the element: {}".format(locator))
            raise

    def elements_num(self, locator):
        """Get count of the same elements."""
        count = len(self.find_elements(locator))
        Logger.info("The same elements: {}".format((locator, count)))
        return count

    def click(self, locator):
        """Click an element."""
        element = self.find_element(locator)
        try:
            element.click()
            Logger.info("Clicked element: {}".format(locator))
        except Exception as e:
            Logger.error("Failed to click element: {}".format(e))
            raise

    def send_key(self, locator, text):
        """Clear and input text into an element."""
        element = self.find_element(locator)
        try:
            element.clear()
            element.send_keys(text)
            Logger.info("Input text: {}".format(text))
        except Exception as e:
            Logger.error("Failed to send keys: {}".format(e))
            raise

    def get_text(self, locator):
        """Get text from an element."""
        element_text = self.find_element(locator).text
        Logger.info("Get text: {}".format(element_text))
        return element_text

    def swipe(self, start_x, start_y, end_x, end_y):
        """Swipe on the screen using W3C actions."""
        window_size = self.driver.get_window_size()
        if not (0 <= start_x <= window_size['width'] and 0 <= start_y <= window_size['height'] and
                0 <= end_x <= window_size['width'] and 0 <= end_y <= window_size['height']):
            raise ValueError("Coordinates out of screen bounds")
        try:
            pointer = PointerInput(interaction.POINTER_TOUCH, "touch")
            actions = ActionBuilder(self.driver, mouse=pointer)
            actions.pointer_action.move_to_location(start_x, start_y)
            actions.pointer_action.pointer_down()
            actions.pointer_action.move_to_location(end_x, end_y).pause(1.0)  # 控制速度
            actions.pointer_action.release()
            actions.perform()
            Logger.info(f"Swiped from ({start_x}, {start_y}) to ({end_x}, {end_y})")
        except Exception as e:
            Logger.error(f"Failed to swipe: {e}")
            raise

    def press_key(self, key="up"):
        if key.lower() == "up":
            self.driver.press_keycode(keycode=19)
        elif key.lower() == "down":
            self.driver.press_keycode(keycode=20)
        elif key.lower() == "left":
            self.driver.press_keycode(keycode=21)
        elif key.lower() == "right":
            self.driver.press_keycode(keycode=22)
        elif key.lower() == "enter":
            self.driver.press_keycode(keycode=66)
        else:
            Logger.error("Unsupported key: " + key)

    def logout(self):
        """
        Common for multiple screens
        :return:
        """
        self.click(search['logoutButton'])
        self.click(search['logoutYes'])


if __name__ == "__main__":
    pass
