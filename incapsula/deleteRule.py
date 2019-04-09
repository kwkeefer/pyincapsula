#!/usr/bin/env python3

"""
Edits security, delivery, or rate rule.

https://docs.imperva.com/bundle/cloud-application-security/page/api/sites-api.htm#Delete2

 api_id -- API ID to use (Default: enviroment variable)
 api_key -- API KEY to use (Default: enviroment variable)
 rule_id -- rule id
"""

import os
import requests
from .com_error import errorProcess

api_endpoint = 'https://my.incapsula.com/api/'


def deleteRule(
        site_id, rule_id, api_id=os.environ.get('API_ID'), api_key=os.environ.get('API_KEY')):
    
    url = api_endpoint+'prov/v1/sites/incapRules/delete'
    try:
        payload = {
            'api_id': api_id,
            'api_key': api_key,
            'site_id': site_id,
            'rule_id': rule_id
        }

        r = requests.post(url, data=payload)
        return r.text
    except Exception as error:
        return errorProcess(error)
