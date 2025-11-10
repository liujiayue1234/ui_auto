from tkinter import NO
import requests
from common.readconfig import con
from common.logger import Logger
from datetime import datetime


class DataConstruction:
    @staticmethod
    def driver_07_login():
        LOGIN_URL = con.get("API", "HOST") + "/auth/login"
        login_payload = {
            "orgID": con.get("ACCOUNT", "DR7_GRP"),
            "username": con.get("ACCOUNT", "DR7_USER"),
            "password": con.get("ACCOUNT", "DR7_PD")
        }
        # request headers
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "DRIVER-APP"
        }

        # send login request
        try:
            response = requests.post(LOGIN_URL, json=login_payload, headers=headers, verify=True)
            response.raise_for_status()  # raise exception if status code is not 200
            Logger.info(f"Login successful at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} with status {response.status_code}")
            return response.cookies  # return CookieJar object
        except requests.exceptions.RequestException as e:
            Logger.error(f"Login failed: {e}")
            return None
    @staticmethod
    def admin_login():
        LOGIN_URL = con.get("API", "HOST") + "/auth/login"
        login_payload = {
            "orgID": con.get("ACCOUNT", "ADMIN_GRP"),
            "username": con.get("ACCOUNT", "ADMIN_USER"),
            "password": con.get("ACCOUNT", "ADMIN_PD")
        }
        # request headers
        headers = {
            "Content-Type": "application/json"
        }

        # send login request
        try:
            response = requests.post(LOGIN_URL, json=login_payload, headers=headers, verify=True)
            response.raise_for_status()  # raise exception if status code is not 200
            Logger.info(f"Login successful at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} with status {response.status_code}")
            return response.cookies  # return CookieJar object
        except requests.exceptions.RequestException as e:
            Logger.error(f"Login failed: {e}")
            return None
    @staticmethod
    def normal_shukko(trunk_id,operation_date):
        cookies = DataConstruction.driver_07_login()
        BUSINESS_API_URL = con.get("API", "HOST") + "/trunkline-mobile/api/trunk-lines/operations/shukko"
        Logger.info("BUSINESS_API_URL"+str(BUSINESS_API_URL))
        payload = {
            "organizationId": "07",
            "operationDate": operation_date,
            "trunkLineId": trunk_id,
            "driverId": con.get("ACCOUNT", "DR7_USER"),
            "status": "STARTED",
            "actualStartingTime": operation_date+"T01:00:00",
            "trunkLineOperationStopItems": []
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "DRIVER-APP"
        }
        try:
            response = requests.post(BUSINESS_API_URL, json=payload, headers=headers, cookies=cookies, verify=True, timeout=30)
            response.raise_for_status()
            Logger.info(f"Business API response status: {response.status_code} ")
            Logger.info(response.request.headers)
            Logger.info(response.text)
            Logger.info(str(response))
            return response.json()
        except requests.exceptions.RequestException as e:
            Logger.error(f"Business API failed: {e}")
            return None
    @staticmethod
    def shuttle_shukko(trunk_id,operation_date,cart=999):
        cookies = DataConstruction.driver_07_login()
        BUSINESS_API_URL = con.get("API", "HOST") + "/trunkline-mobile/api/trunk-lines/operations/shukko-shuttle"
        Logger.info("BUSINESS_API_URL"+str(BUSINESS_API_URL))
        payload = {
            "organizationId": "07",
            "operationDate": operation_date,
            "trunkLineId": trunk_id,
            "driverId": con.get("ACCOUNT", "DR7_USER"),
            "status": "STARTED",
            "operationBusinessStatus": "STARTED",
            "actualStartingTime": operation_date+"T01:00:00",
            "basketCartAmount":cart
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "DRIVER-APP"
        }
        try:
            Logger.info(1)
            response = requests.post(BUSINESS_API_URL, json=payload, headers=headers, cookies=cookies, verify=True, timeout=30)
            response.raise_for_status()
            Logger.info(f"Business API response status: {response.status_code} ")
            return response.json()
        except requests.exceptions.RequestException as e:
            Logger.error(f"Business API failed: {e}")
            return None
            
    @staticmethod
    def get_trunk_id_by_name(trunk_name,operation_date=datetime.now().strftime("%Y-%m-%d"),organization_id='07'):
        cookies = DataConstruction.admin_login()
        BUSINESS_API_URL = con.get("API", "HOST") + "/trunkline/api/trunk-lines/operations"
        params = {
            "trunkLineName": trunk_name,
            "operationDate": operation_date,
            "languageCode": "jp",
            "organizationId": organization_id
        }

        headers = {
            "Content-Type": "application/json"
            }
        try:
            response = requests.get(BUSINESS_API_URL, params=params, headers=headers, cookies=cookies, verify=True, timeout=30)
            Logger.info(response.request.headers)
            Logger.info(response.text)
            Logger.info(str(response))
            response.raise_for_status()
            data = response.json()
            trunk_line_ids = [operation["trunkLineId"] for operation in data["data"]["trunkLineOperations"]]
            if trunk_line_ids:
                first_trunk_line_id = trunk_line_ids[0]
                Logger.info("First trunkLineId:"+first_trunk_line_id)
                return first_trunk_line_id
        except requests.exceptions.RequestException as e:
            Logger.error(f"API call failed: {e}")
            return None

    @staticmethod
    def create_shuttle_trunk(trunk_name,start_date,end_date,trunk_type):
        """
        trunk_type: 3-shuttle regular , 2-shuttle irregular
        """
        cookies = DataConstruction.admin_login()
        xsrf_token = cookies.get("XSRF-TOKEN")
        tidi_access_token = cookies.get("tidi_access_token")
        tidi_refresh_token = cookies.get("tidi_refresh_token")
        Logger.info("xsrf_token:"+str(xsrf_token))
        BUSINESS_API_URL = con.get("API", "HOST") + "/trunkline/api/trunk-lines"
        payload = {
            "organizationId": "07",
            "trunkTypeCode": trunk_type,
            "vehicleTypeCode": "03",
            "operationPatternCode": 1,
            "carrierId": 1,
            "courseName": trunk_name,
            "contractStartDate": start_date,
            "contractEndDate": end_date,
            "trunkLineName": trunk_name,
            "trunkLineCost": 999999999999,
            "vehicleLoadWeight": 999999999999,
            "phoneNumber": "999-9999-9999",
            "vehicleNumber": "vh99999999",
            "driverName": "dn99999999",
            "remark": "automation API data construction",
            "departureLocationId": "270012400301",
            "destinationLocationList": [
                {"orderNumber": 1, "locationId": "104879900101"},
                {"orderNumber": 2, "locationId": "270012400301"},
                {"orderNumber": 3, "locationId": "104879900101"}
            ],
            "languageCode": "en"
        }
        if trunk_type==4:
            payload["trunkTypeReasonCode"]=1

        try:
            session = requests.Session()
            session.headers.update({
                "Content-Type": "application/json",
                "X-XSRF-TOKEN": xsrf_token,
                'Authorization':"Bearer "+tidi_access_token,
            })
            session.cookies.set("tidi_access_token", tidi_access_token)
            session.cookies.set("tidi_refresh_token", tidi_refresh_token)
            session.cookies.set("XSRF-TOKEN", xsrf_token)

            response = session.post(BUSINESS_API_URL, json=payload)
            Logger.info(response.request.headers)
            Logger.info(response.text)
            Logger.info(str(response))
            response.raise_for_status()
            data = response.json()
            trunk_line_id = data["data"]["trunkLineId"]
            return trunk_line_id
        except requests.exceptions.RequestException as e:
            Logger.error(f"API call failed: {e}")
            return None

    @staticmethod
    def create_normal_trunk(trunk_name, start_date, end_date, trunk_type):
        """
        trunk_type: 1-regular , 2-irregular
        """
        cookies = DataConstruction.admin_login()
        xsrf_token = cookies.get("XSRF-TOKEN")
        tidi_access_token = cookies.get("tidi_access_token")
        tidi_refresh_token = cookies.get("tidi_refresh_token")
        Logger.info("xsrf_token:" + str(xsrf_token))
        BUSINESS_API_URL = con.get("API", "HOST") + "/trunkline/api/trunk-lines"
        payload = {
            "organizationId": "07",
            "trunkTypeCode": trunk_type,
            "vehicleTypeCode": "03",
            "operationPatternCode": 1,
            "carrierId": 1,
            "courseName": trunk_name,
            "contractStartDate": start_date,
            "contractEndDate": end_date,
            "trunkLineName": trunk_name,
            "trunkLineCost": 999999999999,
            "vehicleLoadWeight": 999999999999,
            "phoneNumber": "999-9999-9999",
            "vehicleNumber": "vh99999999",
            "driverName": "dn99999999",
            "remark": "automation API data construction",
            "departureLocationId": "270012400301",
              "arrivalTime": "00:00:00",
              "departureTime": "00:30:00",
            "destinationLocationList": [
                {
                  "orderNumber": 1,
                  "locationId": "104879900101",
                  "plannedArrivalTime": "01:00:00",
                  "plannedArrivalDateOffset": 0,
                  "plannedDepartureTime": "01:30:00",
                  "plannedDepartureDateOffset": 0
                },
                {
                  "orderNumber": 2,
                  "locationId": "105879900101",
                  "plannedArrivalTime": "02:00:00",
                  "plannedArrivalDateOffset": 0
                }
              ],
            "languageCode": "en"
        }
        if trunk_type==2:
            payload["trunkTypeReasonCode"]=1
        try:
            session = requests.Session()
            session.headers.update({
                "Content-Type": "application/json",
                "X-XSRF-TOKEN": xsrf_token,
                'Authorization': "Bearer " + tidi_access_token,
            })
            session.cookies.set("tidi_access_token", tidi_access_token)
            session.cookies.set("tidi_refresh_token", tidi_refresh_token)
            session.cookies.set("XSRF-TOKEN", xsrf_token)

            response = session.post(BUSINESS_API_URL, json=payload)
            Logger.info(response.request.headers)
            Logger.info(response.text)
            Logger.info(str(response))
            response.raise_for_status()
            data = response.json()
            trunk_line_id = data["data"]["trunkLineId"]
            return trunk_line_id
        except requests.exceptions.RequestException as e:
            Logger.error(f"API call failed: {e}")
            return None
    @staticmethod
    def delete_trunk(trunk_id):
        cookies = DataConstruction.admin_login()
        xsrf_token = cookies.get("XSRF-TOKEN")
        tidi_access_token = cookies.get("tidi_access_token")
        tidi_refresh_token = cookies.get("tidi_refresh_token")
        Logger.info("xsrf_token:" + str(xsrf_token))
        BUSINESS_API_URL = con.get("API", "HOST") + "/trunkline/api/trunk-lines"
        organization_id = trunk_id[3:5]
        payload = {
            "trunkLineIdList": [trunk_id],
            "organizationId": organization_id
        }

        try:
            session = requests.Session()
            session.headers.update({
                "Content-Type": "application/json",
                "X-XSRF-TOKEN": xsrf_token,
                'Authorization': "Bearer " + tidi_access_token,
            })
            session.cookies.set("tidi_access_token", tidi_access_token)
            session.cookies.set("tidi_refresh_token", tidi_refresh_token)
            session.cookies.set("XSRF-TOKEN", xsrf_token)

            response = session.delete(BUSINESS_API_URL, json=payload)
            Logger.info(response.request.headers)
            Logger.info(response.text)
            Logger.info(str(response))
            response.raise_for_status()
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            Logger.error(f"API call failed: {e}")
            return None
if __name__ == "__main__":
    pass
    # for i in range(50):
    #     DataConstruction.create_normal_trunk('auto-re' + str(i), '2025-09-25', '2025-09-30', 1)
    #     DataConstruction.create_normal_trunk('auto-ir'+str(i), '2025-09-25','2025-09-30',2)
    #DataConstruction.get_trunk_id_by_name("at@can_re","2025-07-31")