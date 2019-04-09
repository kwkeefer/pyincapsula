#!/usr/bin/env python3

"""
Creates security, delivery, or rate rule.

https://docs.imperva.com/bundle/cloud-application-security/page/api/sites-api.htm#Add2

 site_id -- numerical site id to retrive
 api_id -- API ID to use (Default: enviroment variable)
 api_key -- API KEY to use (Default: enviroment variable)
 name -- rule name
 action -- rule action
 rule_filter -- will trigger only a request that matches this filter. For more details on filter guidelines, see Syntax Guide.
 response_code -- Redirect rule's response code. Valid values are 302, 301, 303, 307, 308.	
 protocol
 add_missing --Add cookie or header if it doesn't exist (Rewrite cookie rule only)	
 pattern_from -- pattern to rewrite
 pattern_to -- parttern to change to
 rewrite_name -- Name of cookie or header to rewrite. Applies only for RULE_ACTION_REWRITE_COOKIE and RULE_ACTION_REWRITE_HEADER.
 dc_id -- Data center to forward request to. Applies only for RULE_ACTION_FORWARD_TO_DC.	
 rate_context -- The context of the rate counter. Possible values: IP / Session. Applies only to rules using RULE_ACTION_RATE.	
 rate_interval -- 	The interval (in seconds) of the rate counter. Possible values: A multiple of 10 from 10-300. Applies only to rules using RULE_ACTION_RATE.
 is_test_mode -- Make rule apply only for IP address the API request was sent from.	
 lb_algorithm -- Data center load balancing algorithm.
"""

import os
import requests
from .com_error import errorProcess

api_endpoint = 'https://my.incapsula.com/api/'


def editRule(
        site_id, api_id=os.environ.get('API_ID'), api_key=os.environ.get('API_KEY'), name=None,
        action=None, rule_filter=None, response_code=None, protocol=None, add_missing=None,
        pattern_from=None, pattern_to=None, rewrite_name=None, dc_id=None, rate_context=None,
        rate_interval=None, is_test_mode=None, lb_algorithm=None):
    
    url = api_endpoint+'prov/v1/sites/incapRules/edit'
    try:
        payload = {
            'api_id':api_id,
            'api_key':api_key,
            'site_id':site_id
        }

        if name is not None:
            payload['name'] = name
        if action is not None:
            payload['action'] = action
        if rule_filter is not None:
            payload['filter'] = rule_filter
        if response_code is not None:
            payload['response_code'] = response_code
        if protocol is not None:
            payload['protocol'] = protocol
        if add_missing is not None:
            payload['add_missing'] = add_missing
        if pattern_from is not None:
            payload['from'] = pattern_from
        if pattern_to is not None:
            payload['to'] = pattern_to
        if rewrite_name is not None:
            payload['rewrite_name'] = rewrite_name
        if dc_id is not None:
            payload['dc_id'] = dc_id
        if rate_context is not None:
            payload['rate_context'] = rate_context
        if rate_interval is not None:
            payload['rate_interval'] = rate_interval
        if is_test_mode is not None:
            payload['is_test_mode'] = is_test_mode
        if lb_algorithm is not None:
            payload['lb_algorithm'] = lb_algorithm


        r = requests.post(url, data=payload)
        return r.text
    except Exception as error:
        return errorProcess(error)
