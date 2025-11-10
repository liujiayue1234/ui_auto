# Trunk line Automation Testing Framework
This project provides an automation testing framework for mobile and web applications using Pytest, Appium, and Selenium. 
It supports automated UI testing, report generation with Allure, and structured test organization.
## Project Structure
    1.1 common - common tools
    1.2 config - configuration
    1.3 logs - logs are stored by every month
    1.4 report - keep the latest execution report
    1.5 APP - pytest & appium to complete mobile application automation
    1.6 WEB - pytest & selenium to complete web application automation
    1.7 conftest.py - store fixtures for app and web automation
    1.8 run_mac.sh - run web and app testcases and generate execution report , save it into report/

## Dependency installation
```pip install -r requirements.txt```

## Description for mobile application automation of Android version
    3.1 APP/base/ - store common functions
    3.2 APP/element/ - store elements locations of every screen
    3.3 APP/page/ - inherit base/basepage.py , store specific functions for every screen
    3.4 APP/testcase/ - use functions of page/**page.py to complete automation test
    3.5 APP/package/ - Android and iOS package

## Description for web application automation 
    4.1 WEB/base/ - store common functions
    4.2 WEB/element/ - store elements locations of every page
    4.3 WEB/page/ - inherit base/basepage.py , store specific functions for every page
    4.4 WEB/testcase/ - use functions of page/**page.py to complete automation test
## common functions
    5.1 common/inspect.py - ensure elements locations format is correct
    5.2 common/logger.py - define log format and log file location
    5.3 common/readcofig.py - get or set item from config/config.ini
    5.4 common/readelement.py - read elements loctions from **.yaml