# -*- coding: utf-8 -*-
"""
Transport for Zuora SOAP API
"""
import requests
from suds.transport import Reply
from suds.transport.http import HttpTransport
from suds.transport.http import HttpAuthenticated


class HttpTransportWithKeepAlive(HttpAuthenticated, object):

    def __init__(self):
        super(HttpTransportWithKeepAlive, self).__init__()

    def open(self, request):
        return HttpTransport.open(self, request)


    def send(self, request):
        print(request.url)
        print(request.message)
        r = requests.post(request.url, data=request.message, headers=request.headers)
        response = Reply(r.status_code, r.headers, r.text)
        return response
