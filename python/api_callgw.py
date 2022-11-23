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
    mno_endpoint = "azampay/mno/checkout"
    bank_endpoint = "azampay/bank/checkout"
    checkout_endpoint = ""
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

    def call_gw(self):
        result = {"success": False, "message": "", "trxid": ""}
        self.token = self.generate_token()
        if self.data["endpoint_type"] == "bank":
            self.checkout_endpoint = self.bank_endpoint
            checkout_data = {"provider": self.data["payment_network"], "merchantAccountNumber": self.data["payment_account"], "merchantMobileNumber": self.data["payment_number"], "merchantName": self.data["payment_name"],
                             "amount": self.data["payment_amount"], "referenceId": self.data["payment_id"], "currencyCode": self.data["currency"], "otp": self.data["otp"], "additionalProperties": self.data["additionalProperties"]}
        elif self.data["endpoint_type"] == "mno":
            self.checkout_endpoint = self.mno_endpoint
            checkout_data = {"provider": self.data["payment_network"], "accountNumber": self.data["payment_number"], "amount": self.data["payment_amount"],
                             "externalId": self.data["payment_id"], "currency": self.data["currency"], "additionalProperties": self.data["additionalProperties"]}

        if self.token is None:
            result["message"] = "Failed to get token"
        elif self.token["success"] == False:
            result["message"] = self.token["message"]
        else:
            headers_ = {"Content-Type": "application/json",
                        "Accept": "application/json", "Authorization": "Bearer "+self.token["token"]}
            response = requests.post(
                self.base_url + self.checkout_endpoint, data=json.dumps(checkout_data), headers=headers_)
            res = json.loads(response.text)
            if response == "" or res is None:
                result["message"] = "Failed to connect and process checkout"
            elif "success" in res and res["success"] == False:
                if self.data["endpoint_type"] == "bank":
                    result["message"] = res["msg"]
                else:
                    result["message"] = res["message"]
            else:
                if self.data["endpoint_type"] == "bank":
                    result["message"] = res["msg"]
                    result["trxid"] = res["data"]["properties"]["ReferenceID"]
                else:
                    result["message"] = res["message"]
                    result["trxid"] = res["transactionId"]
                result["success"] = True
        return result


## endpoint_type: mno | bank
# payment_network: Airtel | HaloPesa | Azampesa | Tigopesa | CRDB

additionalProperties = {"customer_id": "1234"}
obj_data = {"app_name": "DemoApp", "client_id": "7f2cd55d-47d3-43b4-90c4-9a98a49bb11a", "client_token": "cbba010a-175b-4c57-b6dc-c5d636b5d20f", "client_secret": "RfNxSk3mjV5T79GgQIVyPHFnDXWapi3TDKN7v5QOCCTIqnRhfXET6XPmUvTcRNKd1bYpjI9T3j+ydgDq2X/rGyDzojbvUDc6OhgWGrnfArw1+WtD3MyAYyvFI1mwb7xtUa3B6ntMlXL+FIvJziPPhwTdEeujQsHWeAQEKneHOZfZ2j9ROvQJGio+v5sQV5rSpRKOfdxFaOaZfzow/4G5n4eqh4S6WUfO3+Fj6fPKTfW8rU4iW8u4euffwi7XKYMVS68Vxf+94oG0KJ/jfzAe0DSxfbtVXIRlcu6Lnov0xHcL2qTI2dHLxqi3yvs8kevbWtW0zNFiZQnzIQSEFYKodM9HzeIk0KUuyXXV5eJ8EOPPuVVXDUZO3+0ovfjBUhZe3NtAGb9JOjZmpsC4ypfjPT4usa/DE1gYpc5gdX3RtzatpIfkG02Q1SMwFSZ3GAIUlcRxLtjNM7srLlZdni4Z+jFpLqG3z+dbiebCbNFgDculTMruE/YhRetOHG0c91tJrkGqJCYf34yDTHVdUGOFVCQsol+/vH3jZ60LDTnW8pIsLldD8a5lA+znIkJtB88LEpgYuHlO8q7vgjbsSC7KP7yDbuYQKcwu8w+RaRP0Nt4WWhAZzQsl0u2m1r9sRyfIUvteYf+R8ZlU3VZ5D8XP9kDNkSeIXunP3QdlqSjE4kM=",
            "endpoint_type": "mno", "payment_network": "Airtel", "payment_number": "0713123456", "payment_account": "12345678901", "payment_name": "John Smith", "payment_amount": "100", "payment_id": "123", "currency": "TZS", "otp": "1234", "additionalProperties": additionalProperties}

a = azampay_checkout_api(obj_data, "yes")
print(a.call_gw())
