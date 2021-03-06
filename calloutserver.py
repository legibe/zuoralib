# -*- coding: utf-8 -*-
import yaml
import os
import logging
from platin.httpservices.httpserver import HTTPServer
from platin.httpservices.treerouter import TreeRouter
from platin.httpservices.jsonformat import JSONFormat

class CalloutServer(object):

    actions = [
        'subscriptionCreated',
        'subscriptionStarted',
        'subscriptionEnded',
        'amendmentProcessed',
        'invoiceDue',
        'paymentBounced',
        'paymentReceived'
    ]

    def __init__(self, *args, **kwargs):
        with open('config.yaml') as f:
            config = yaml.load(f)
            self.logger = logging.getLogger('notifications')
            self.logger.setLevel(logging.DEBUG)
            server = HTTPServer(converter=JSONFormat())
            router = TreeRouter(server)
            for action in self.actions:
                router.registerAction(action, self.process, 'POST')
            for k, i in config['ssl'].items():
                config['ssl'][k] = os.path.expanduser(i)
            server.run(config['port'],router,config['ssl'])

    def process(self, response, data, path):
        info = []
        for k, i in data.items():
            info.append('%s: %s' % (k, str(i)))
        self.logger.info(str(path) + ', ' + ', '.join(info))
        return 'ok'

CalloutServer()
