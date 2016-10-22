# -*- coding: utf-8 -*-
"""
Transport for Zuora SOAP API
"""
import httplib2
import requests
from suds.transport import Reply
from suds.transport.http import HttpTransport
from suds.transport.http import HttpAuthenticated


class HttpTransportWithKeepAlive(HttpAuthenticated, object):

    def __init__(self):
        super(HttpTransportWithKeepAlive, self).__init__()
        self.http = httplib2.Http(timeout=30,
                                  disable_ssl_certificate_validation=True)

    def open(self, request):
        return HttpTransport.open(self, request)

    def send(self, request):
        headers = request.headers
        r = requests.post(request.url, data=request.message, headers=request.headers)
        """
        headers, message = self.http.request(request.url, "POST",
                                             body=request.message,
                                             headers=request.headers)
        """
        response = Reply(200, headers, r.text)
        return response
