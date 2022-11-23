#!/usr/bin/env python3
# coding: utf-8

import requests
import json


class azampay_checkout_pages:
    url = ""
    data = ""

    def __init__(self, data, test_mode):
        if test_mode == "yes" or test_mode == "on" or test_mode:
            self.url = "https://sandbox.azampay.co.tz/api/v1/Partner/PostCheckout"
        else:
            self.url = "https://checkout.azampay.co.tz/api/v1/Partner/PostCheckout"
        self.data = data

    def call_gw(self):
        headers_ = {"Content-Type": "application/json-patch+json"}
        response = requests.post(
            self.url, data=json.dumps(self.data), headers=headers_)
        return response.text


items = {"items": [{"name": "Invoide 2"}]}
obj_data = {"appName": "DemoApp", "clientId": "7f2cd55d-47d3-43b4-90c4-9a98a49bb11a", "vendorName": "DemoApp",
            "amount": "100", "externalId": "123", "currency": "TZS", "language": "English", "cart": items, "redirectSuccessURL": "http://192.168.116.79/php/checkout/pages_callback.php", "redirectFailURL": "http://192.168.116.79/php/checkout/pages_callback.php"}

a = azampay_checkout_pages(obj_data, "yes")

print(a.call_gw())
