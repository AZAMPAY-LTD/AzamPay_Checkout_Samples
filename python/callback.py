#!/usr/bin/env python3
# coding: utf-8

import json
import socketserver
from http.server import BaseHTTPRequestHandler
import datetime


class azampay_checkout_callback(BaseHTTPRequestHandler):

    def log_my_data(self, data):
        try:
            file = open("./log_callback.log", "a")
            file.write(datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S") + " | " + json.dumps(data) + "\n")
            file.close()
        except Exception as error:
            print("Error: " + repr(error))

    def my_callback_endpoint(self, req_data):
        res = json.loads(req_data)
        if "transactionstatus" in res:
            print(res["transactionstatus"])
        print(res)
        self.log_my_data(res)

    def do_POST(self):
        global req_data
        response = "ok"
        if self.path == "/my_callback_endpoint":
            content_length = int(self.headers["Content-Length"])
            req_data = self.rfile.read(content_length)
            self.my_callback_endpoint(req_data.decode("utf-8"))
            response = "ok data"
        self.send_response(200,)
        self.end_headers()
        self.wfile.write(bytes(response, "utf-8"))


httpd = socketserver.TCPServer(("localhost", 8080), azampay_checkout_callback)
httpd.serve_forever()
