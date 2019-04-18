#!/usr/bin/env python3
"""Create a new site

Creates a new site in Incapsula under the specified account.
After running you will recive an email from Incapsula with further
instructions to finnish verifing and setting up the site.
 domain -- the domain name for the site
 account_id -- sub-account to associate the site with
 api_id -- API ID to use (Default: enviroment variable)
 api_key -- API KEY to use (Default: enviroment variable)
 ref_id -- Customer specific identifier for this operation.	
 site_ip -- Manually set the web server IP/CNAME.	
 force_ssl -- If this value is "true", manually set the site to support SSL. This option is only available for sites with manually configured IP/CNAME and for specific accounts.	
 naked_domain_san -- Use “true” to add the naked domain SAN to a www site’s SSL certificate. Default value: true	
 wildcard_san -- Use “true” to add the wildcard SAN or “false” to add the full domain SAN to the site’s SSL certificate. Default value: true	
 log_level -- Available only for Enterprise Plan customers that purchased the Logs Integration SKU. Sets the log reporting level for the site. Options are “full”, “security”, “none” and "default"	
 logs_account_id -- Available only for Enterprise Plan customers that purchased the Logs Integration SKU. Numeric identifier of the account that purchased the logs integration SKU and which collects the logs. If not specified, operation will be performed on the account identified by the authentication parameters	
"""

import os
import requests
from .com_error import errorProcess

api_endpoint = 'https://my.incapsula.com/api/'


def addSite(
        domain, account_id, api_id=os.environ.get('API_ID'),
        api_key=os.environ.get('API_KEY'), ref_id=None, site_ip=None, 
        force_ssl=None, naked_domain_san=None, wildcard_san=None, 
        log_level=None, logs_account_id=None):
    url= api_endpoint + 'prov/v1/sites/add'
    try:
        payload = {
            'api_id':api_id,
            'api_key':api_key,
            'domain':domain,
            'account_id':account_id,
            'send_site_setup_emails':'true'
        }

        if ref_id is not None:
            payload['ref_id'] = ref_id
        if site_ip is not None:
            payload['site_ip'] = site_ip
        if force_ssl is not None:
            payload['force_ssl'] = force_ssl
        if naked_domain_san is not None:
            payload['naked_domain_san'] = naked_domain_san
        if wildcard_san is not None:
            payload['wildcard_san'] = wildcard_san
        if log_level is not None:
            payload['log_level'] = log_level
        if logs_account_id is not None:
            payload['logs_account_id'] = logs_account_id

        r = requests.post(url, data=payload)
        return r.text
    except Exception as error:
        return errorProcess(error)
