import requests
import json
import time
import utils

class Core:
    # Configuration
    BASE_URL : str
    LOCAL_HOST : str
    ENDPOINTS_PATH : str
    CREDENTIALS_PATH : str
    STATE : str
    CITY : str
    MODULE : str
    AUTHORIZATION : str

    def __init__(self, module_code, env_config_path="env_configs.json"):
        env_conf = utils.read_json(env_config_path)
        self.BASE_URL = env_conf["BASE_URL"]
        self.LOCAL_HOST = env_conf["LOCAL_HOST"]
        self.ENDPOINTS_PATH = env_conf["ENDPOINTS_PATH"]
        self.CREDENTIALS_PATH = env_conf["CREDENTIALS_PATH"]
        self.STATE = env_conf["STATE"]
        self.CITY = env_conf["CITY"]
        self.AUTHORIZATION = env_conf["AUTHORIZATION"]
        self.MODULE = module_code

    def get_endpoint(self, api_name, module_code=None):
        module_code = module_code or self.MODULE
        with open(self.ENDPOINTS_PATH) as file: 
            endpoint = json.load(file)
        return endpoint[module_code][api_name]
    
    def get_creds(self, user, module_code=None):
        module_code = module_code or self.MODULE
        with open(self.CREDENTIALS_PATH) as file: 
            creds = json.load(file)
        return creds[module_code][user]

    def call_api(self, RequestInfo, payload, api, params={}, delay=2):
        """
        payload can be either string path or dictionary object
        api needs to be a string path
        """
        if isinstance(payload, str):
            payload = utils.read_json(payload)
        else:
            payload=payload
        payload["RequestInfo"] = RequestInfo

        headers = {"Content-Type": "application/json"}

        time.sleep(delay)

        response = requests.post(url=self.BASE_URL+api, 
                                headers=headers, 
                                params=params,
                                json=payload)
        utils.log_response(response)
        return response.json()

    def fetch_bill(self, RequestInfo, App_ID, businessService, tenantId=None):
        tenantId = tenantId or self.CITY
        params = {
            "tenantId": tenantId,
            "consumerCode": App_ID,
            "businessService": businessService
        }

        response = self.call_api(RequestInfo, payload={}, 
                                api="/billing-service/bill/v2/_fetchbill", 
                                params=params)
        return response

    def login(self, user):
        payload = {
                    "username": self.get_creds(user)["username"],
                    "password": self.get_creds(user)["password"],
                    "userType": self.get_creds(user)["userType"],
                    "tenantId": self.get_creds(user)["tenantId"],
                    "scope": "read",
                    "grant_type": "password"
                }
        
        header = {
                    "accept": "application/json, text/plain, */*",
                    "authorization": self.AUTHORIZATION,
                    "content-type": "application/x-www-form-urlencoded"
                }
        
        response = requests.post(url = self.BASE_URL + self.get_endpoint("login", "User"), 
                                headers = header, 
                                data = payload)
        utils.log_response(response)
        # Some identity servers return 'access_token', others return 'refresh_token'
        resp_json = response.json()
        token = resp_json.get("access_token") or resp_json.get("refresh_token")
        RequestInfo = utils.generate_RequestInfo(token, resp_json.get("UserRequest"))
        return RequestInfo

    def logout(self, RequestInfo):
        payload = {
                    "access_token": RequestInfo["authToken"],
                    "RequestInfo": {
                        "apiId": "",
                        "authToken": RequestInfo["authToken"],
                        "msgId": "1731957339904|en_IN",
                        "plainAccessRequest": {}
                    }
                }
        
        params = {
            "tenantId": self.STATE
        }

        response = requests.post(url = self.BASE_URL + self.get_endpoint("logout", "User"),
                                data = payload)

        # print("logged out sesson of: ", RequestInfo["userInfo"]["userName"], "\n\n")

    def collect_fee(self, RequestInfo, fetchBillResponse, tenantId=None):
        tenantId = tenantId or self.CITY
        from CollectionService import payload_builder

        bill_data = fetchBillResponse["Bill"][0]
        payload = payload_builder.create(bill_data, RequestInfo)
        
        params = {
            "tenantId": tenantId
        }

        response = self.call_api(RequestInfo, payload, 
                                "/collection-services/payments/_create", 
                                params)
