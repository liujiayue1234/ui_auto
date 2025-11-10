#!/usr/bin/env bash
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT_DIR="report/Report_$TIMESTAMP"
rm -rf report/*
rm -rf WEB/DOWNLOAD/*

# Run testcases with @pytest.mark.web ,browser=chrome
python3 -m pytest --alluredir=report/allure-results-web-web_login --clean-alluredir -m web_login --browser=chrome WEB/testcase/
python3 -m pytest --alluredir=report/allure-results-web-web_arrival --clean-alluredir -m web_arrival --browser=chrome WEB/testcase/
python3 -m pytest --alluredir=report/allure-results-web-web_trunk_overview --clean-alluredir -m web_trunk_overview --browser=chrome WEB/testcase/
python3 -m pytest --alluredir=report/allure-results-web-web_operation_schedule --clean-alluredir -m web_operation_schedule --browser=chrome WEB/testcase/

# Run testcases with @pytest.mark.web ,browser=firefox
#python3 -m pytest --alluredir=report/allure-results-web-firefox --clean-alluredir -m web --browser=firefox WEB/testcase/

# Run testcases  device=android
#python3 -m pytest --alluredir=report/allure-results-android --clean-alluredir -m app --device=android APP/testcase/

# Generate the combined report
allure generate report/allure-results-web-web_login report/allure-results-web-web_arrival report/allure-results-web-web_trunk_overview report/allure-results-web-web_operation_schedule  -o "$REPORT_DIR" --clean

# Open report
allure open "$REPORT_DIR"

