#!/usr/bin/env python3


# This script it to interact with the v6sonar API for managing accounts, agents, and monitors.
# TODO: Add reporting function
# TODO: Create installer
# TODO: Fix CLI flags
# TODO: Add database hooks
# TODO: Add formatting to the CLI command output
# TODO: Add ability to import sites from an Excel spreadsheet or .csv


import os
import sys
import datetime
import json
import math
import logging
import configparser
import pprint
import requests


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
API_ACCOUNT_ID = config.get('api-ecu', 'accountid')
API_CLIENT_ID = config.get('api-ecu', 'clientid')
API_SECRET = config.get('api-ecu', 'secret')

DEFAULT_LOG_LEVEL = "debug"  # Default log level

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL
          }

class API(object):
    """API Object wrapper"""
    pass

def start_logging(filename=LOG_FILENAME, format=LOG_FORMAT, level=DEFAULT_LOG_LEVEL):
    """
    Start logging with given filename and level.
    """
    logging.basicConfig(filename=filename, level=LEVELS[level], format=format)
    # log a message
    logging.info('Starting up the v6sonar API wrapper')

def _url(path):
    return API_BASEURL + ":" + API_PORT + "/" + API_VERSION + "/" + path

def auth():
    """ https://api.v6sonar.com:443/v1/authorize?{clientSecret}&{clientid} """
    data = {'clientSecret': API_SECRET, 'clientId': API_CLIENT_ID}
    try:
        r = requests.get(_url("authorize"), params=data)
        logging.debug('URL: ' + r.url)
        token = r.json()["value"]
        return token
    except requests.HTTPError as e:
        logging.error("Error: " + sys._getframe().f_code.co_name + " : Unable to complete request due to error: ", e)

def get_data(url, starttime=None, endtime=None, limit=None, offset=None):
    auth()
    data = {"start": starttime, "end": endtime, "limit": limit, "offset": offset}
    headers = {"Authorization": "Bearer" + auth()}
    results = []
    response = requests.get(url, params=data, headers=headers)
    logging.debug("200 URL: {0}".format(response.url))
    logging.debug(response.status_code)
    if response.status_code == 200:
        rdata = response.json()
        results.extend(rdata)
        return results
    if response.status_code == 206:
        rcontent = response.headers['content-range']
        a, total = rcontent.split("/")
        chunk = int(math.ceil(int(total) / limit))
        for i in range(0, chunk, 1):
            offset = i * limit
            logging.debug("Offset: {0} \nStatus Code: {1}".format(offset, response.status_code))
            data = {"start": starttime, "end": endtime, "limit": limit, "offset": offset}
            response = requests.get(url, params=data, headers=headers)
            logging.debug("206 Loop URL: {0}".format(response.url))
            rdata = response.json()
            results.extend(rdata)
    return results

def get_agents(no_systems_agents="True", get_services="False"):
    """https://api.v6sonar.com:443/v1/agents?accountId=706d6d61&noSystemAgents=true&&getServices=false&"""
    auth()
    data = {"accountId": API_ACCOUNT_ID, "noSystemAgents": no_systems_agents, "getServices": get_services}
    headers = {"Authorization": "Bearer" + auth()}
    try:
        r = requests.get(_url("agents"), params=data, headers=headers)
        logging.debug('URL: ' + r.url)
        #pprint.pprint(r.json())
        return r.json()
    except requests.HTTPError as e:
        logging.error("Error: " + sys._getframe().f_code.co_name + " : Unable to complete request due to error: ", e)

def get_agents_list(no_systems_agents="True", get_services="False"):
    """https://api.v6sonar.com:443/v1/agents?accountId=706d6d61&noSystemAgents=true&&getServices=false&"""
    data = get_agents()
    agentsbyid = [d['id'] for d in data]
    return agentsbyid

def get_agents_list_by_name(no_systems_agents="True", get_services="False"):
    """https://api.v6sonar.com:443/v1/agents?accountId=706d6d61&noSystemAgents=true&&getServices=false&"""
    data = get_agents()
    agentsbyname = [d['agentName'] for d in data]
    agentid = [d['id'] for d in data]
    pair = zip(agentsbyname, agentid)
    return pair

def get_agent_by_id(agent_id):
    """https://api.v6sonar.com:443/v1/agents?accountId=706d6d61&noSystemAgents=true&&getServices=false&"""
    auth()
    headers = {"Authorization": "Bearer" + auth()}
    try:
        r = requests.get(_url("agents/" + agent_id), headers=headers)
        logging.debug('URL: ' + r.url)
        pprint.pprint(r.json())
    except requests.HTTPError as e:
        logging.error("Error: " + sys._getframe().f_code.co_name + " : Unable to complete request due to error: ", e)


def get_measurements_by_agent_id(agent_id, starttime=None, endtime=None):
    """https://api.v6sonar.com:443/v1/agents/706d6d616b387573889FB622F5C46791/measurements?start=2017-06-22T05%3A00%3A00.00Z&end=2017-06-22T06%3A00%3A00.00Z"""
    auth()
    data = {"start": starttime, "end": endtime}
    headers = {"Authorization": "Bearer" + auth()}
    try:
        r = requests.get(_url("agents/" + agent_id + "/measurements"), params=data, headers=headers)
        logging.debug('URL: ' + r.url)
        try:
            pprint.pprint(r.json())
        except ValueError as e:
            logging.error("No measurements returned for this agent.")
    except requests.HTTPError as e:
        print("Error: " + sys._getframe().f_code.co_name + " : Unable to complete request due to error: ", e)

def get_tasks():
    """https://api.v6sonar.com:443/v1/agents?accountId=706d6d61&noSystemAgents=true&&getServices=false&"""
    auth()
    headers = {"Authorization": "Bearer" + auth()}
    try:
        r = requests.get(_url("tasks"), headers=headers)
        logging.debug('URL: ' + r.url)
        pprint.pprint(r.json())
    except requests.HTTPError as e:
        print("Error: " + sys._getframe().f_code.co_name + " : Unable to complete request due to error: ", e)

def get_services():
    """https://api.v6sonar.com:443/v1/agents?accountId=706d6d61&noSystemAgents=true&&getServices=false&"""
    auth()
    headers = {"Authorization": "Bearer" + auth()}
    try:
        r = requests.get(_url("services"), headers=headers)
        logging.debug('URL: ' + r.url)
#       pprint.pprint(r.json())
        return r.json()
    except requests.HTTPError as e:
        print("Error: " + sys._getframe().f_code.co_name + " : Unable to complete request due to error: ", e)

def get_services_list_by_id():
    """https://api.v6sonar.com:443/v1/agents?accountId=706d6d61&noSystemAgents=true&&getServices=false&"""
    data = get_services()
    servicesbyid = [d['id'] for d in data]
    return servicesbyid

def get_services_list_by_name():
    """https://api.v6sonar.com:443/v1/agents?accountId=706d6d61&noSystemAgents=true&&getServices=false&"""
    data = get_services()
    servicesbyname = [d['serviceName'] for d in data]
    return servicesbyname

def get_service_by_service_id(serviceId, getTasks="True"):
    """https://api.v6sonar.com:443/v1/agents?accountId=706d6d61&noSystemAgents=true&&getServices=false&"""
    auth()
    data = {"getTasks": getTasks}
    headers = {"Authorization": "Bearer" + auth()}
    try:
        r = requests.get(_url("services/" + serviceId), params=data, headers=headers)
        logging.debug('URL: ' + r.url)
        pprint.pprint(r.json())
    except requests.HTTPError as e:
        print("Error: " + sys._getframe().f_code.co_name + " : Unable to complete request due to error: ", e)

def get_service_by_account_id():
    """https://api.v6sonar.com:443/v1/agents?accountId=706d6d61&noSystemAgents=true&&getServices=false&"""
    auth()
    headers = {"Authorization": "Bearer" + auth()}
    try:
        r = requests.get(_url("services/account/" + API_ACCOUNT_ID), headers=headers)
        logging.debug('URL: ' + r.url)
        pprint.pprint(r.json())
    except requests.HTTPError as e:
        print("Error: " + sys._getframe().f_code.co_name + " : Unable to complete request due to error: ", e)

def get_agents_by_service_id(service_id, account_id=None, no_systems_agents="True", get_services="True", get_agents="True", agent_id=None):
    """https://api.v6sonar.com:443/v1/agents?accountId=706d6d61&noSystemAgents=true&&getServices=false&"""
    auth()
    data = {"noSystemAgents": no_systems_agents, "getServices": get_services, "get_agents": get_agents}
    headers = {"Authorization": "Bearer" + auth()}
    try:
        r = requests.get(_url("services/" + service_id + "/agents"), params= data, headers=headers)
        logging.debug('URL: ' + r.url)
        pprint.pprint(r.json())
    except requests.HTTPError as e:
        print("Error: " + sys._getframe().f_code.co_name + " : Unable to complete request due to error: ", e)

def get_measurements_by_service_id(service_id, starttime=None, endtime=None, limit=None, offset=None):
    """https://api.v6sonar.com:443/v1/services/ifb3dz9v/measurements?start=2017-08-14T11%3A11%3A58.000Z&end=2017-08-14T17%3A11%3A58.000Z"""
    url = _url("services/" + service_id + "/measurements")
    try:
        return get_data(url, starttime, endtime, limit, offset)
    except ValueError:
        logging.error("No measurements returned for this agent.")
    except requests.HTTPError as e:
        print("Error: " + sys._getframe().f_code.co_name + " : Unable to complete request due to error: ", e)

def get_service_id_history(service_id, starttime=None, endtime=None):
    """https://api.v6sonar.com:443/v1/agents?accountId=706d6d61&noSystemAgents=true&&getServices=false&"""
    auth()
    data = {"start": starttime, "end": endtime}
    headers = {"Authorization": "Bearer" + auth()}
    try:
        r = requests.get(_url("services/" + service_id + "/history"), params=data, headers=headers)
        logging.debug('URL: ' + r.url)
        try:
            pprint.pprint(r.json())
        except ValueError as e:
            logging.error("No measurements returned for this agent.")
    except requests.HTTPError as e:
        print("Error: " + sys._getframe().f_code.co_name + " : Unable to complete request due to error: ", e)

def get_measurement_by_measurement_id(measurement_id, starttime=None, endtime=None):
    """https://api.v6sonar.com:443/v1/agents?accountId=706d6d61&noSystemAgents=true&&getServices=false&"""
    auth()
    data = {"start": starttime, "end": endtime}
    headers = {"Authorization": "Bearer" + auth()}
    try:
        r = requests.get(_url("measurements/" + measurement_id), params=data, headers=headers)
        logging.debug('URL: ' + r.url)
        try:
            pprint.pprint(r.json())
        except ValueError as e:
            print("No measurements returned for this agent.")
    except requests.HTTPError as e:
        print("Error: " + sys._getframe().f_code.co_name + " : Unable to complete request due to error: ", e)

def get_jobs(account_id=API_ACCOUNT_ID, starttime=None, endtime=None, job_id=None, limit=5, ignore_account_details="True"):
    """https://api.v6sonar.com:443/v1/jobs?limit=5&ignoreAccountResults=true"""
    auth()
    data = {"accountid": account_id, "start": starttime, "end": endtime, "jobIds": job_id, "limit": limit, "ignoreAccountResults": ignore_account_details}
    headers = {"Authorization": "Bearer" + auth()}
    try:
        r = requests.get(_url("jobs"), params=data, headers=headers)
        logging.debug('URL: ' + r.url)
        try:
            pprint.pprint(r.json())
        except ValueError as e:
            print("No measurements returned for this agent.")
    except requests.HTTPError as e:
        print("Error: " + sys._getframe().f_code.co_name + " : Unable to complete request due to error: ", e)

def get_jobs_by_id(account_id=API_ACCOUNT_ID, starttime=None, endtime=None, job_id=None, limit=5, ignore_account_details="True"):
    """https://api.v6sonar.com:443/v1/jobs?limit=5&ignoreAccountResults=true"""
    auth()
    data = {"start": starttime, "end": endtime, "jobIds": job_id, "limit": limit, "ignoreAccountResults": ignore_account_details}
    headers = {"Authorization": "Bearer" + auth()}
    try:
        r = requests.get(_url("jobs/" + account_id), params=data, headers=headers)
        logging.debug('URL: ' + r.url)
        try:
            pprint.pprint(r.json())
        except ValueError as e:
            print("No measurements returned for this agent.")
    except requests.HTTPError as e:
        print("Error: " + sys._getframe().f_code.co_name + " : Unable to complete request due to error: ", e)


def get_users(email=None, username=None, deleted=None):
    """https://api.v6sonar.com:443/v1/users"""
    auth()
    data = {"email": email, "username": username, "getDeleted": deleted}
    headers = {"Authorization": "Bearer" + auth()}
    try:
        r = requests.get(_url("users"), params=data, headers=headers)
        logging.debug('URL: ' + r.url)
        try:
            pprint.pprint(r.json())
        except ValueError as e:
            print("No measurements returned for this agent.")
    except requests.HTTPError as e:
        print("Error: " + sys._getframe().f_code.co_name + " : Unable to complete request due to error: ", e)

def get_users_by_id(user_id=None):
    """https://api.v6sonar.com:443/v1/users"""
    auth()
    data = {}
    headers = {"Authorization": "Bearer" + auth()}
    try:
        r = requests.get(_url("users/" + user_id), params=data, headers=headers)
        logging.debug('URL: ' + r.url)
        try:
            pprint.pprint(r.json())
        except ValueError as e:
            print("No measurements returned for this agent.")
    except requests.HTTPError as e:
        print("Error: " + sys._getframe().f_code.co_name + " : Unable to complete request due to error: ", e)

def post_service(domain, agent):
    auth()
    headers = {"Authorization": "Bearer" + auth()}
    url = "http://" + domain
    data =  {
                "serviceName": domain,
                "url": url,
                "sendSonarNotifications": "no",
                "interval": 900,
                "monitorIpv6": "yes",
                "tasks": [
                    {
                        "taskId": "bbbbbbbb",
                        "order": "1",
                        "details": {
                            "method": "GET",
                            "url": url,
                        }
                    },
                    {
                        "taskId": "aaaaaaaa",
                        "order": "2",
                        "details": {
                            "url": url,
                        }
                    },
                    {
                        "taskId": "cccccccc",
                        "order": "3",
                        "details": {
                            "protocol": "tcp",
                            "port": "80",
                            "asn": "true",
                            "url": url,
                        }
                    }
                ],
                "endTime": "2026-09-21T18:51:03.629Z",
                "agentList": agent,
            }
    try:
        r = requests.post(_url("services"), json=data, headers=headers)
        logging.debug('URL: ' + r.url)
        try:
            pprint.pprint(r.json())
        except ValueError as e:
            print("Unable to post the value.")
    except requests.HTTPError as e:
        print("Error: " + sys._getframe().f_code.co_name + " : Unable to complete request due to error: ", e)

def delete_service_by_service_id(serviceId):
    """https://api.v6sonar.com:443/v1/agents?accountId=706d6d61&noSystemAgents=true&&getServices=false&"""
    auth()
    data = {}
    headers = {"Authorization": "Bearer" + auth()}
    try:
        r = requests.delete(_url("services/" + serviceId), params=data, headers=headers)
        logging.debug('URL: ' + r.url)
        if r.status_code == "204":
            logging.debug("Service:" + serviceId + "Successfully Deleted.")
        else:
            logging.debug("Command failed with status: {0}.", r.status_code)
    except requests.HTTPError as e:
        print("Error: " + sys._getframe().f_code.co_name + " : Unable to complete request due to error: ", e)

def put_service(service):
    auth()
    headers = {"Authorization": "Bearer" + auth()}
    data = {
                "interval": 300,
           }
    try:
        r = requests.put(_url("services/" + service), params=data, headers=headers)
        logging.debug('URL: ' + r.url)
        logging.debug('URL Details: ' + str(r.content))
        logging.debug('Status Code: ' + str(r.status_code))
        try:
            pprint.pprint(r.json())
        except ValueError as e:
            print("Unable to post the value.")
    except requests.HTTPError as e:
        print("Error: " + sys._getframe().f_code.co_name + " : Unable to complete request due to error: ", e)

if __name__ == "__main__":
    start_logging()
    #auth()
    #pprint.pprint(get_agents())
    #print(get_agents_list())
    #print(get_agents_list_by_name())
    #get_agent_by_id("706d6d616b387573E2624BE96361670E")
    #get_measurements_by_agent_id("706d6d616b387573889FB622F5C46791", "2017-06-22T05:00:00.00Z", "2017-06-22T10:00:00.00Z")
    #get_services()
    get_services_list_by_id()
    #get_services_list_by_name("facebook")
    #delete_service_by_service_id("zpskj6ej")
    #get_service_by_service_id("bh4m4jkh")
    #get_service_by_service_id("bpndjxok")
    #get_service_by_account_id()
    #get_agents_by_service_id("bh4m4jkh")
    #get_agents_by_service_id("wfjo2a0r")
    #get_measurements_by_service_id("ifb3dz9v", starttime="2017-08-14T11:11:58.000Z", endtime="2017-08-14T17:11:58.000Z")
    #get_service_id_history("bh4m4jkh", "2017-06-22T05:00:00.00Z", "2017-06-22T10:00:00.00Z" )
    #get_measurement_by_measurement_id("0e301e8e-3648-433f-b257-ecaf06fa9627", "2017-06-22T05:00:00.00Z", "2017-06-22T10:00:00.00Z")
    #get_jobs(limit="20")
    #get_jobs_by_id()
    #get_users()
    #get_users_by_id("6b71736a")
    #get_tasks()
    #print(APIGet.agents())
    #get_accts_by_id()
    #get_users()
    #post_service("facebook.com", agents)
    #put_service("ikqrq3bs")