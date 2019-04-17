#!/usr/bin/env python3

"""Returns the JSON status for one site

 site_id -- numerical site id to retrive
 api_id -- API ID to use (Default: enviroment variable)
 api_key -- API KEY to use (Default: enviroment variable)
 tests -- List of tests to run on site before returning its status. A comma separated list of one of: domain_validation, services, dns.
"""

import os
import requests
from .com_error import errorProcess

api_endpoint = 'https://my.incapsula.com/api/'

def getSiteStatus(
        site_id, api_id=os.environ.get('API_ID'),
        api_key=os.environ.get('API_KEY'), tests=None):
    url = api_endpoint + 'prov/v1/sites/status'
    try:
        payload = {
            'api_id':api_id,
            'api_key':api_key,
            'site_id':site_id
        }

        if tests is not None:
            payload['tests'] = tests

        r = requests.post(url, data=payload)
        return r.text
    except Exception as error:
        return errorProcess(error)