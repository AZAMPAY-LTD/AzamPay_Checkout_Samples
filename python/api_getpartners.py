#!/usr/bin/env python3
# coding: utf-8

import requests
import json


class azampay_checkout_api:
    token = ""
    data = ""
    url = ""
    base_url = ""
    auth_url = ""
    partners_endpoint = "api/v1/Partner/GetPaymentPartners"
    token_endpoint = "AppRegistration/GenerateToken"

    def __init__(self, data, test_mode):
        if test_mode == "yes" or test_mode == "on" or test_mode:
            self.base_url = "https://sandbox.azampay.co.tz/"
            self.auth_url = "https://authenticator-sandbox.azampay.co.tz/"
        else:
            self.base_url = "https://checkout.azampay.co.tz/"
            self.auth_url = "https://authenticator.azampay.co.tz/"
        self.data = data

    def generate_token(self):
        result = {"success": False, "message": "", "token": "", "code": ""}
        data_to_retrieve_token = {"appName": self.data["app_name"],
                                  "clientId": self.data["client_id"], "clientSecret": self.data["client_secret"]}
        headers_ = {"Content-Type": "application/json",
                    "Accept": "application/json", "X-API-KEY": self.data["client_token"]}
        response = requests.post(
            self.auth_url + self.token_endpoint, data=json.dumps(data_to_retrieve_token), headers=headers_)
        res = json.loads(response.text)
        if response == "" or ("statusCode" in res and res["statusCode"] != 200) or ("status" in res and res["status"] != 200):
            if response == "":
                result["message"] = "Something went wrong. Contact support team for more details."
            elif "statusCode" in res and res["statusCode"] == 423:
                result["message"] = "Provided detail is not valid for this app or secret key has expired."
            elif "statusCode" in res and res["statusCode"] == 500:
                result["message"] = "Internal Server Error."
            elif "errors" in res and "ClientSecret" in res["errors"]:
                result["message"] = res["errors"]["ClientSecret"][0]
            elif "errors" in res and "ClientId" in res["errors"]:
                result["message"] = res["errors"]["ClientId"][0]
            elif "errors" in res and "AppName" in res["errors"]:
                result["message"] = res["errors"]["AppName"][0]
            else:
                result["message"] = "Something went wrong. Contact support team for more details."
        else:
            result["code"] = "200"
            result["token"] = res["data"]["accessToken"]
            result["success"] = True
        return result

    def get_partners(self):
        result = {"success": False, "message": "", "token": "", "code": ""}
        self.token = self.generate_token()
        if self.token is None:
            result["message"] = "Failed to get token"
        elif self.token["success"] == False:
            result["message"] = self.token["message"]
        else:
            headers_ = {"Authorization": "Bearer " + self.token["token"]}
            response = requests.get(
                self.base_url + self.partners_endpoint, headers=headers_)
            res = json.loads(response.text)
            if res is None:
                result["message"] = "Could not get payment partners."
            elif res[0]["id"] is None:
                if res["message"] is not None:
                    result["message"] = res["message"]
                else:
                    result["message"] = "Could not get payment partners."
            else:
                result["success"] = True
                result["message"] = "Successful getting payment partners."
                result["partners"] = res
        return result


obj_data = {"app_name": "DemoApp", "client_id": "7f2cd55d-47d3-43b4-90c4-9a98a49bb11a", "client_token": "cbba010a-175b-4c57-b6dc-c5d636b5d20f", "client_secret": "RfNxSk3mjV5T79GgQIVyPHFnDXWapi3TDKN7v5QOCCTIqnRhfXET6XPmUvTcRNKd1bYpjI9T3j+ydgDq2X/rGyDzojbvUDc6OhgWGrnfArw1+WtD3MyAYyvFI1mwb7xtUa3B6ntMlXL+FIvJziPPhwTdEeujQsHWeAQEKneHOZfZ2j9ROvQJGio+v5sQV5rSpRKOfdxFaOaZfzow/4G5n4eqh4S6WUfO3+Fj6fPKTfW8rU4iW8u4euffwi7XKYMVS68Vxf+94oG0KJ/jfzAe0DSxfbtVXIRlcu6Lnov0xHcL2qTI2dHLxqi3yvs8kevbWtW0zNFiZQnzIQSEFYKodM9HzeIk0KUuyXXV5eJ8EOPPuVVXDUZO3+0ovfjBUhZe3NtAGb9JOjZmpsC4ypfjPT4usa/DE1gYpc5gdX3RtzatpIfkG02Q1SMwFSZ3GAIUlcRxLtjNM7srLlZdni4Z+jFpLqG3z+dbiebCbNFgDculTMruE/YhRetOHG0c91tJrkGqJCYf34yDTHVdUGOFVCQsol+/vH3jZ60LDTnW8pIsLldD8a5lA+znIkJtB88LEpgYuHlO8q7vgjbsSC7KP7yDbuYQKcwu8w+RaRP0Nt4WWhAZzQsl0u2m1r9sRyfIUvteYf+R8ZlU3VZ5D8XP9kDNkSeIXunP3QdlqSjE4kM="}

a = azampay_checkout_api(obj_data, "yes")
print(a.get_partners())
