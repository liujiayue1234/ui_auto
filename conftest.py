from common.inspect_element import inspect_element
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from common.logger import Logger  # type: ignore
import pytest
from appium.options.common.base import AppiumOptions
import logging
import appium.webdriver as appium_driver
from common.readconfig import con
from config.config import DOWNLOAD_PATH
import os

driver = None


@pytest.fixture(scope='session')
def web_driver(request):
    global driver
    browser = request.config.getoption("--browser", default="chrome")
    if driver is None:
        try:
            if browser.lower() == 'firefox':
                options = FirefoxOptions()
                options.set_preference("dom.disable_beforeunload", True)
                
                # set Firefox download path
                if not os.path.exists(DOWNLOAD_PATH):
                    os.makedirs(DOWNLOAD_PATH)
                
                # Firefox download preference
                options.set_preference("browser.download.folderList", 2)  # 0=desktop, 1=download folder, 2=custom
                options.set_preference("browser.download.dir", DOWNLOAD_PATH)
                options.set_preference("browser.download.useDownloadDir", True)
                options.set_preference("browser.download.viewableInternally.enabledTypes", "")
                options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/csv,text/csv,application/vnd.ms-excel")
                options.set_preference("browser.download.manager.showWhenStarting", False)
                
                driver = webdriver.Firefox(options=options)
                Logger.info(driver.service.path)  # type: ignore
                Logger.info("Firefox driver initialized with Selenium Manager")  # type: ignore
            else:  # default = chrome
                options = ChromeOptions()
                options.add_argument('--disable-desktop-notifications')
                
                # set download path
                if not os.path.exists(DOWNLOAD_PATH):
                    os.makedirs(DOWNLOAD_PATH)
                
                prefs = {
                    "download.default_directory": DOWNLOAD_PATH,
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "safebrowsing.enabled": True
                }
                options.add_experimental_option("prefs", prefs)
                
                driver = webdriver.Chrome(options=options)
                Logger.info(driver.service.path)  # type: ignore
                Logger.info("Chrome driver initialized with Selenium Manager")  # type: ignore
        except Exception as e:
            Logger.error(f"Driver initialization failed: {e}")  # type: ignore
            raise

    inspect_element()
    yield driver
    driver.quit()


@pytest.fixture(scope='session')
def app_driver(request):
    global driver
    if driver is None:
        try:
            device = request.config.getoption("--device", default="android")
            if device.lower() == "android":
                options = AppiumOptions()
                options.set_capability("platformName", "Android")
                options.set_capability("deviceName", con.get("ANDROID", "DEVICE_NAME"))
                options.set_capability("platformVersion", con.get("ANDROID", "VERSION"))
                options.set_capability("appPackage", con.get("ANDROID", "PACKAGE_NAME"))
                options.set_capability("appActivity", con.get("ANDROID", "MAIN_SCREEN"))
                options.set_capability("automationName", "UiAutomator2")
                options.set_capability("noReset", False)
                driver = appium_driver.Remote('http://localhost:' + con.get("ANDROID", "PORT"), options=options)

            elif device.lower() == "ios":
                options = AppiumOptions()
                options.set_capability("platformName", "iOS")
                options.set_capability("udid", con.get("IOS", "UDID"))
                options.set_capability("bundleId", con.get("IOS", "BUNDLE_ID"))
                options.set_capability("automationName", "XCUITest")
                options.set_capability("noReset", True)
                driver = appium_driver.Remote("http://localhost:" + con.get("IOS", "PORT"), options=options)
            else:
                raise ValueError(f"Unsupported platform: {device}")


        except Exception as e:
            Logger.error(f"Driver initialization failed: {e}")  # type: ignore
            raise
    yield driver
    driver.quit()


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--device", action="store", default="android")