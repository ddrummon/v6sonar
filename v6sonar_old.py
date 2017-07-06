#!/usr/bin/env python3

"""
This script it to interact with the v6sonar API for managing accounts, agents, and monitors.
TODO: Add reporting function
TODO: Create installer
TODO: Fix CLI flags
TODO: Add database hooks
TODO: Add formatting to the CLI command output
TODO: Add ability to import sites from an Excel spreadsheet or .csv
"""

import os
import sys
import datetime
import json
import logging
from collections import OrderedDict
import configparser
import requests
import urllib.request
import urllib.error
import urllib.parse

cfg_filename = os.path.join(os.path.dirname(__file__), 'conf/v6sonar.conf')
config = configparser.RawConfigParser()
config.read(cfg_filename)

#  Log file information
LOG_FILENAME = (os.path.join(os.path.dirname(__file__), config.get('log', 'output')))
LOG_FORMAT = config.get('log', 'format')

#  Basic API information
API_BASEURL = config.get('api-base', 'baseurl')
API_VERSION = config.get('api-base', 'version')
API_PORT = config.get('api-base', 'port')

#  Account specific API information
API_ACCOUNT_ID = config.get('api-mcnc', 'accountid')
API_CLIENT_ID = config.get('api-mcnc', 'clientid')
API_SECRET = config.get('api-mcnc', 'secret')

DEFAULT_LOG_LEVEL = "debug"  # Default log level

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL
          }

def start_logging(filename=LOG_FILENAME, format=LOG_FORMAT, level=DEFAULT_LOG_LEVEL):
    """
    Start logging with given filename and level.
    """
    logging.basicConfig(filename=filename, level=LEVELS[level], format=format)
    # log a message
    logging.info('Starting up the v6sonar API wrapper')

"Create the url for the request"
#url = API_BASEURL + ":" + API_PORT + "/" + API_VERSION + "/" + path

def _url(path):
    return API_BASEURL + ":" + API_PORT + "/" + API_VERSION + "/" + path

class APIGet(object):

    def auth(self):
        pass

    def account_by_id(self):
        """ https://api.v6sonar.com:443/v1/accounts/{accountid} """
        jresult = get_auth()
        request = urllib.request.Request(_url("accounts") + "/" + API_ACCOUNT_ID)
        request.add_header('Authorization', 'Bearer ' + jresult['value'])
        logging.debug('URL: ' + _url("accounts") + "/" + API_ACCOUNT_ID)

        try:
            response = urllib.request.urlopen(request)
            results = response.read()
            print(results)
        except urllib.error.HTTPError as e:
            print("Error: " + sys._getframe().f_code.co_name + " : Unable to complete request due to error: ", e)

    def accounts(self):
        pass

    def agents():
        """https://api.v6sonar.com:443/v1/agents?accountId=706d6d61&noSystemAgents=true&&getServices=false&"""
        jresult = get_auth()
        request = urllib.request.Request(_url("agents") + "?" + "accountId=" + API_ACCOUNT_ID)
        request.add_header('Authorization', 'Bearer ' + jresult['value'])
        logging.debug('URL: ' + _url("agents") + "?" + "accountId=" + API_ACCOUNT_ID)

        try:
            response = urllib.request.urlopen(request)
            results = response.read()
            print(results)
        except urllib.error.HTTPError as e:
            print("Error: " + sys._getframe().f_code.co_name + " : Unable to complete request due to error: ", e)
        pass

    def agent_by_id(self):
        pass


class APIPut(object):
    pass


class APIDelete(object):
    pass


def api_put():
    pass


def api_post():
    pass


def api_del():
    pass


def get_auth():
    """ https://api.v6sonar.com:443/v1/authorize?{clientSecret}&{clientid} """
    data = {'clientSecret': API_SECRET, 'clientId': API_CLIENT_ID}
    url_values = urllib.parse.urlencode(data)
    logging.debug('URL: ' + _url("authorize") + "?" + url_values)

    try:
        response = urllib.request.urlopen(_url("authorize") + "?" + url_values)
        results = response.read()
        jresult = json.loads(results.decode('utf-8'))
        eresult = results.json()
        print(eresult)
        return jresult, exp
    except urllib.error.HTTPError as e:
        print("Error: " + sys._getframe().f_code.co_name + " : Unable to complete request due to error: ", e)


def put_acct_by_id():
    pass


def del_acct_by_id():
    pass

def post_accounts():
    pass

def put_agent_by_id():
    pass


def del_agent_by_id():
    pass


def get_monitor_by_agent():
    pass


def get_tasks():
    pass


def get_services():
    pass


def post_services():
    pass


def get_services_by_service_id():
    pass


def put_services_by_service_id():
    pass


def del_services_by_service_id():
    pass


def get_services_by_acct_id():
    pass


def get_agents_with_servie_id():
    pass


def get_measurements_by_service_id():
    pass


def get_history_by_service_id():
    pass


def get_measurement_by_id():
    pass


def get_jobs():
    pass


def post_jobs():
    pass


def get_job_by_id():
    pass


def get_users():
    data = {'clientSecret': API_SECRET, 'clientId': API_CLIENT_ID}
    url_values = urllib.parse.urlencode(data)
    logging.debug('URL: ' + _url("authorize") + "?" + url_values)
    resp = urllib.request.urlopen(_url("authorize") + "?" + url_values)
    res = resp.read()
    j = json.loads(res.decode('utf-8'))
    logging.debug("URL: " + _url("users"))
    request = urllib.request.Request(_url("users"))
    request.add_header('Authorization', 'Bearer ' + j['value'])

    try:
        response = urllib.request.urlopen(request)
        results = response.read()
        print(results)
    except urllib.error.HTTPError as e:
        print("Error: " + sys._getframe().f_code.co_name + " : Unable to complete request due to error: ", e)


def post_users():
    pass


def get_user_by_id():
    pass


def put_user_by_id():
    pass


def del_user_by_id():
    pass


def print_results():
    pass

if __name__ == "__main__":
    start_logging()
    print(APIGet.agents())
    #get_accts_by_id()
    #get_users()