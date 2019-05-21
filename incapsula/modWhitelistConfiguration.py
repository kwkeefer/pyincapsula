#!/usr/bin/env python3

"""Use this operation to set-up whitelists / exceptions.

Valid options are listed at:
https://docs.imperva.com/bundle/cloud-application-security/page/api/sites-api.htm#Modify5

 site_id -- numerical site id to retrive (Default: None)
 api_id -- API ID to use (Default: enviroment variable)
 api_key -- API KEY to use (Default: enviroment variable)
 rule_id -- The id of the rule (either a security or an acl rule), e.g api.acl.blacklisted_ips. 

All options below are optional:

whitelist_id -- The id (an integer) of the whitelist to be set. This field is optional - in case no id is supplied, a new whitelist will be created.
delete_whitelist -- An optional boolean parameter. If it is set to "true" and a whitelist id is sent, the whitelist will be deleted.
urls -- A comma separated list of resource paths.  For example, /home and /admin/index.html are resource paths, while http://www.example.com/home is not. 
countries -- A comma separated list of country codes.
continents -- A comma separated list of continent codes.
ips -- A comma separated list of IPs or IP ranges, e.g: 192.168.1.1, 192.168.1.1-192.168.1.100 or 192.168.1.1/24
client_app_types -- A comma separated list of client application types,
client_apps -- A comma separated list of client application IDs.
parameters -- A comma separated list of encoded parameters.
user_agents -- A comma separated list of encoded user agents.
exception_id_only -- Return only the new/edited exception id.

"""

import os
import requests
from .com_error import errorProcess

api_endpoint = 'https://my.incapsula.com/api/'


def modWhitelistConfiguration(
        site_id=None, api_id=os.environ.get('API_ID'), api_key=os.environ.get('API_KEY'),
        rule_id=None, whitelist_id=None, delete_whitelist=None, urls=None, countries=None,
        continents=None, ips=None, client_app_types=None, client_apps=None, parameters=None,
        user_agents=None, exception_id_only=None
        ):

    url = api_endpoint+'prov/v1/sites/configure/whitelists'
    try:  # Setup the payload
        assert site_id is not None
        payload = {
            'api_id': api_id,
            'api_key': api_key,
            'site_id': site_id
        }

        if rule_id is not None:
            payload['rule_id'] = rule_id
        if whitelist_id is not None:
            payload['whitelist_id'] = whitelist_id
        if delete_whitelist is not None:
            payload['delete_whitelist'] = delete_whitelist
        if urls is not None:
            payload['urls'] = urls
        if countries is not None:
            payload['countries'] = countries
        if continents is not None:
            payload['continents'] = continents
        if ips is not None:
            payload['ips'] = ips
        if client_app_types is not None:
            payload['client_app_types'] = client_app_types
        if client_apps is not None:
            payload['client_apps'] = client_apps
        if parameters is not None:
            payload['parameters'] = parameters
        if user_agents is not None:
            payload['user_agents'] = user_agents
        if exception_id_only is not None:
            payload['exception_id_only'] = exception_id_only

    except AssertionError as error:
        return errorProcess(error, site_id)
    except Exception as error:
        return errorProcess(error)
    try:  # Deliver the payload
        r = requests.post(url, data=payload)
        r.raise_for_status()
        return r.text
    except NameError as error:
        return errorProcess(error, 'Rule ID')
    except Exception as error:
        return errorProcess(error)
