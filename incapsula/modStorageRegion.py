#!/usr/bin/env python3

"""Use this operation to set-up advanced caching rules.

Valid options are listed at:
https://docs.imperva.com/bundle/cloud-application-security/page/api/sites-api.htm#Set3

Use this operation to set the site's data storage region.

 site_id -- numerical site id to retrive (Default: None)
 api_id -- API ID to use (Default: enviroment variable)
 api_key -- API KEY to use (Default: enviroment variable)
 data_storage_region -- APAC / EU / US
"""

import os
import requests
from .com_error import errorProcess

api_endpoint = 'https://my.incapsula.com/api/'


def modStorageRegion(
        site_id=None, api_id=os.environ.get('API_ID'), api_key=os.environ.get('API_KEY'), data_storage_region='US'):

    url = api_endpoint+'prov/v1/sites/data-privacy/region-change'
    try:  # Setup the payload
        assert site_id is not None
        payload = {
            'api_id': api_id,
            'api_key': api_key,
            'site_id': site_id,
            'data_storage_region': data_storage_region
        }


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
