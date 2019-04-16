#!/usr/bin/env python3

"""
Valid options are listed at:
https://docs.imperva.com/bundle/cloud-application-security/page/api/sites-api.htm#Modify

 site_id -- numerical site id to retrive (Default: None)
 api_id -- API ID to use (Default: enviroment variable)
 api_key -- API KEY to use (Default: enviroment variable)
 param -- see list of parameters below
 value -- according to params below

 Parameter values

 active -- Whether the site is active or bypassed by the Incapsula network. One of: active | bypass.
 site_ip -- Comma separated list of IPs. For example: 8.8.8.8,1.2.2.2
 domain_validation -- Sets the domain validation method that will be used to generate an SSL certificate. One of: email | html | dns
 approver -- Sets the approver e-mail address that will be used to perform SSL domain validation.
 ignore_ssl -- Sets the ignore SSL flag (if the site is in pending-select-approver state). Pass "true" in the value parameter.
 acceleration_level -- Sets the acceleration level of the site, one of: none | standard | aggressive. It is advised to use the newer Modify caching mode API call instead, as it provides enhanced functionality.
 seal_location -- Sets the seal location, e.g. "api.seal_location.bottom_right".
 domain_redirect_to_full -- Sets the redirect naked to full flag. Pass "true" in the value parameter.
 remove_ssl -- Sets the remove SSL from site flag. Pass "true" in the value parameter.
 ref_id -- Sets the Reference ID, a free-text field that enables you to add a unique identifier to correlate an object in our service, such as a protected website, with an object on the customer side.

"""

import os
import requests
from .com_error import errorProcess

api_endpoint = 'https://my.incapsula.com/api/'


def modSiteConfiguration(site_id, param, value, api_id=os.environ.get('API_ID'), api_key=os.environ.get('API_KEY')):

    url = api_endpoint+'prov/v1/sites/configure'
    try:  # Setup the payload
        assert site_id is not None
        payload = {
            'api_id': api_id,
            'api_key': api_key,
            'site_id': site_id,
            'param': param,
            'value': value
        }

    except AssertionError as error:
        return errorProcess(error, site_id)
    except Exception as error:
        return errorProcess(error)
    try:  # Deliver the payload
        r = requests.post(url, data=payload)
        print("Request URL:\n{}".format(url))
        print("Request payload:\n{}".format(payload))
        r.raise_for_status()
        return r.text
    except NameError as error:
        return errorProcess(error, 'Rule ID')
    except Exception as error:
        return errorProcess(error)
