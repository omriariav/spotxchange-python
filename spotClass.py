__author__ = 'omriariav'
import requests

#CONSTS:
SPOTXCHANGE_API_URL = "https://publisher-api.spotxchange.com" #SANDBOX
# SPOTXCHANGE_API_URL = "https://publisher.spotxchange.com" #PRODUCTION
REVENUE_REPORT_TEMPLATE = "/1.0/Publisher!(publisher_id)!/Channels/RevenueReport"
ADVERTISER_LEVEL_TEMPLATE = "/1.0/Publisher!(publisher_id)!/Channels/AdvertiserReport"

class spotXChangeClass():

    def __init__(self):
        self._publisher_id = ""
        self._active_publishers = {}
        self._login_flag = False
        self._cookie = ""
        self._headers = {
            'User-Agent': 'customPython/0.0.1',
            'Accept': ' application/json'
        }

    def _get(self,rest_path, payload={}):
        _request_url = SPOTXCHANGE_API_URL + rest_path
        if self._cookie == "":
            r = requests.get(_request_url, params=payload, headers=self._headers)
        else:
            r = requests.get(_request_url, params=payload, cookies=self._cookie, headers=self._headers)
        return r

    def _post(self,rest_path, payload={}):
        _request_url = SPOTXCHANGE_API_URL + rest_path
        if self._cookie == "":
            r = requests.post(_request_url, data=payload, headers=self._headers)
        else:
            r = requests.post(_request_url, data=payload, cookies=self._cookie, headers=self._headers)
        print r.content
        return r

    def login(self,login_object):
        response = self._post("/1.0/Publisher/Login", login_object)
        self._cookie = response.cookies
        login_response = response.json()
        if login_response.has_key("value"):
            self._login_flag = True
            self._active_publishers[login_response['value']['publisher']['publisher_id']] = \
                login_response['value']['publisher']['active']
            self._publisher_id = login_response['value']['publisher']['publisher_id']
        else:
            print login_response


    def advertisersReport(self, publisher_id="",**kwargs):
        query_string = ""
        query = []
        if self._publisher_id != "" and publisher_id == "":
            publisher_id = self._publisher_id
        _rest_path = ADVERTISER_LEVEL_TEMPLATE .replace("!(publisher_id)!","(" +publisher_id + ")")
        if not self._login_flag:
            return ["_loging_flag ERROR"]
        if kwargs.has_key("date_range"):
            query.append("date_range=" + kwargs["date_range"])
        if kwargs.has_key("orderby"):
            query.append("$orderby=" + kwargs["orderby"])
        if kwargs.has_key("publisher_id"):
            query.append("publisher_id=" + kwargs["publisher_id"])
        if kwargs.has_key("currency_code"):
            query.append("currency_code=" + kwargs["currency_code"])
        if len(query) > 0:
            query_string = "?" + "&".join(query)
        response = self._get(_rest_path + query_string)
        return response.json()

    def revenueReport(self, publisher_id="",**kwargs):
        query_string = ""
        query = []
        if self._publisher_id != "" and publisher_id == "":
            publisher_id = self._publisher_id
        _rest_path = REVENUE_REPORT_TEMPLATE.replace("!(publisher_id)!","(" +publisher_id + ")")
        if not self._login_flag:
            return ["_loging_flag ERROR"]
        if kwargs.has_key("date_range"):
            query.append("date_range=" + kwargs["date_range"])
        if kwargs.has_key("orderby"):
            query.append("$orderby=" + kwargs["orderby"])
        if kwargs.has_key("publisher_id"):
            query.append("publisher_id=" + kwargs["publisher_id"])
        if kwargs.has_key("currency_code"):
            query.append("currency_code=" + kwargs["currency_code"])
        if len(query) > 0:
            query_string = "?" + "&".join(query)
        response = self._get(_rest_path + query_string)
        return response.json()

