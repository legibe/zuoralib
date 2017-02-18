# -*- coding: utf-8 -*-
from platin.httpservices.httpserver import HTTPServer
from platin.httpservices.treerouter import TreeRouter
from platin.httpservices.jsonformat import JSONFormat


class CalloutServer(object):

    def __init__(self, *args, **kwargs):
        server = HTTPServer(converter=JSONFormat())
        router = TreeRouter(server)
        router.registerAction('start', self.process, 'POST')
        ssl_options = {
            'keyfile': '/Users/claude/.ssl/privateKey.key',
            'certfile': '/Users/claude/.ssl/certificate.cert'
        }
        port = 443
        server.run(port,router,ssl_options)

    def process(self, response, data, path):
        print data
        return 'ok'

CalloutServer()
