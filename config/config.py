import os
from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy

# project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# config directory
INI_PATH = os.path.join(BASE_DIR, 'config', 'config.ini')

# web element directory
WEB_ELEMENT_PATH = os.path.join(BASE_DIR, 'WEB', 'element')

# app element directory
APP_ELEMENT_PATH = os.path.join(BASE_DIR, 'APP', 'element')

# log directory
LOG_PATH = os.path.join(BASE_DIR, 'logs')

# APP package path
APP_PATH = os.path.join(BASE_DIR, 'APP', 'package')

# DOWNLOAD directory
DOWNLOAD_PATH = os.path.join(BASE_DIR, 'WEB', 'DOWNLOAD')

# Type of locations
LOCATE_MODE_WEB = {
    'css': By.CSS_SELECTOR,
    'xpath': By.XPATH,
    'name': By.NAME,
    'id': By.ID,
    'class': By.CLASS_NAME
}
LOCATE_MODE_APP = {
    'id': AppiumBy.ID,
    'xpath': AppiumBy.XPATH,
    'accessibility_id': AppiumBy.ACCESSIBILITY_ID,
    'class_name': AppiumBy.CLASS_NAME
}

if __name__ == '__main__':
    print(BASE_DIR)
