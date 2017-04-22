# -*- coding: utf-8 -*-
"""
Client for Zuora SOAP API
"""
import os
import logging
import time

from datetime import datetime
from datetime import timedelta

from suds import WebFault
from suds.client import Client
from suds.sax.text import Text
from suds.sax.element import Element

from transport import HttpTransportWithKeepAlive
from config import logger, config

DEFAULT_SESSION_DURATION = 115 * 60

class ZuoraException(Exception):
    """
    Base Zuora Exception.
    """
    pass


class BaseZuora(object):
    """
    SOAP Client based on Suds
    """
    retries = 0

    def __init__(self, wsdl, username, password,
                 session_duration=DEFAULT_SESSION_DURATION):
        self.wsdl = wsdl
        self.username = username
        self.password = password

        self.session = None
        self.session_duration = session_duration
        self.session_expiration = datetime.now()
        self.wsdl_path = 'file://%s' % os.path.abspath(self.wsdl)
        self.options = []
        self.headers = []

        self.client = Client(
            self.wsdl_path,
            transport=HttpTransportWithKeepAlive())
        self.client.set_options(cache=None)

    def instanciate(self, instance_type_string):
        """
        Create object for client.factory.
        """
        return self.client.factory.create(instance_type_string)

    def set_session(self, session_id):
        """
        Record the session info.
        """
        self.session = session_id
        self.session_expiration = datetime.now() + timedelta(
            seconds=self.session_duration)
        session_namespace = ('ns1', self.accesspoint)
        session = Element('session', ns=session_namespace).setText(session_id)
        header = Element('SessionHeader', ns=session_namespace)
        header.append(session)
        self.headers = []
        self.headers.append(header)
        self.client.set_options(soapheaders=self.headers+self.options)

    def single_transaction(self,on):
        cop = self.instanciate('CallOptions')
        if on:
            cop.useSingleTransaction = True
            self.options.append(cop)
        else:
            self.options = [ x for x in self.options if type(cop) != type(x) ]
        self.client.set_options(soapheaders=self.headers+self.options)

    def reset(self):
        """
        Reset the connection to the API.
        """
        self.session = None
        self.client.options.transport = HttpTransportWithKeepAlive()

    def call(self, method, *args, **kwargs):
        """
        Call a SOAP method.
        """
        if self.session is None or self.session_expiration <= datetime.now():
            self.login()

        try:
            response = method(*args, **kwargs)
            logger.info('Sent: %s', self.client.last_sent())
            logger.info('Received: %s', self.client.last_received())
            if isinstance(response, Text):  # Occasionally happens
                logger.warning('Invalid response %s, retrying...', response)
                self.reset()
                self.retries += 1
                if self.retries >= config.get('zuora_max_retries',10):
                    raise ZuoraException('Received invalid response %d times' % self.retries)
                time.sleep(self.retries)
                return self.call(method, *args, **kwargs)
        except WebFault as error:
            if error.fault.faultcode == 'fns:INVALID_SESSION':
                logger.warning('Invalid session, relogging...')
                self.reset()
                self.retries += 1
                if self.retries >= config.get('zuora_max_retries',10):
                    raise ZuoraException('Received invalid session %d times' % self.retries)
                time.sleep(self.retries)
                return self.call(method, *args, **kwargs)
            else:
                logger.info('Sent: %s', self.client.last_sent())
                logger.info('Received: %s', self.client.last_received())
                logger.error('WebFault: %s', error.__dict__)
                raise ZuoraException('WebFault: %s' % error.__dict__)
        except Exception as error:
            logger.info('Sent: %s', self.client.last_sent())
            logger.info('Received: %s', self.client.last_received())
            logger.error('Unexpected error: %s', error)
            raise ZuoraException('Unexpected error: %s' % error)

        logger.debug('Successful response %s', response)
        BaseZuora.retries = 0
        return response

    def amend(self, amend_requests):
        """
        Amend susbcriptions.
        """
        response = self.call(
            self.client.service.amend,
            amend_requests)
        return response

    def create(self, z_objects):
        """
        Create z_objects.
        """
        response = self.call(
            self.client.service.create,
            z_objects)
        return response

    def delete(self, object_string, ids=[]):
        """
        Delete z_objects by ID.
        """
        response = self.call(
            self.client.service.delete,
            object_string, ids)
        return response

    def execute(self, object_string, synchronous=False, ids=[]):
        """
        Execute a process by IDs.
        """
        response = self.call(
            self.client.service.execute,
            object_string, synchronous, ids)
        return response

    def generate(self, z_objects):
        """
        Generate z_objects.
        """
        response = self.call(
            self.client.service.execute,
            z_objects)
        return response

    def get_user_info(self):
        """
        Return current user's info.
        """
        response = self.call(
            self.client.service.get_user_info)
        return response

    def login(self):
        """
        Login on the API to get a session.
        """
        i = 0
        done = False
        while not done:
            response = self.client.service.login(self.username, self.password, entityName='EMEA')
            if response.Session is not None:
                self.set_session(response.Session)
                done = True
            else:
                time.sleep(2)
                i += 1
            if i > 100:
                raise ZuoraError('Struggling to login to Zuora, not obtaining a session ID')
        return response


    def query(self, query_string):
        """
        Execute a query.
        """
        response = self.call(
            self.client.service.query,
            query_string)
        return response

    def query_more(self, query_locator):
        """
        Execute the suite of a query.
        """
        response = self.call(
            self.client.service.queryMore,
            query_locator)
        return response

    def subscribe(self, subscribe_requests):
        """
        Subscribe accounts.
        """
        response = self.call(
            self.client.service.subscribe,
            subscribe_requests)
        return response

    def update(self, z_objects):
        """
        Update z_objects.
        """
        response = self.call(
            self.client.service.update,
            z_objects)
        return response

    def __str__(self):
        """
        Display the client __str__ method.
        """
        return self.client.__str__()


class Zuora(BaseZuora):
    """
    Final SOAP Zuora Client
    """

    def __init__(self):
        username = config['username']
        password = config['password']
        self.accesspoint = config.get('accesspoint','http://api.zuora.com/')
        super(Zuora, self).__init__(config['wsdl'], username, password, DEFAULT_SESSION_DURATION)

zclient = Zuora()
print zclient.query("select Id from Subscription where Status = 'Active'")
