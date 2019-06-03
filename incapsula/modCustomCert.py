#!/usr/bin/env python3

"""Uploads a custom certificate for a site

Requires the Site_ID, location of the certificate file, location of the 
Private Key file, and the passphrase if required

 site_id -- numerical site id to retrive
 certificate -- file location of the certificate to upload
 private_key -- file location of the private key for the certificate
 passphrase -- passphrase for the private key (Default: None)
 api_id -- API ID to use (Default: enviroment variable)
 api_key -- API KEY to use (Default: enviroment variable)

"""

import os
import requests
import base64
import sys
from OpenSSL import crypto
from .com_error import errorProcess
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

api_endpoint = 'https://my.incapsula.com/api/'

# Requires the Site_ID, location of the certificate file, location of
# the Private Key file, and the passphrase if required
def modCustomCert(
        site_id, certificate, private_key, passphrase=None,
        api_id=os.environ.get('API_ID'), api_key=os.environ.get('API_KEY')):
    try:
        with open(certificate,'rb') as certFile:
            read = certFile.read()
            cert = base64.b64encode(read)
    except EnvironmentError as error:
        return errorProcess(error,str(certificate)+'Certificate could not be read')
    except Exception as error:
        return errorProcess(error)
    try:
        with open(private_key,'rb') as privFile:
            read = privFile.read()
            privKey = base64.b64encode(privFile)
    except EnvironmentError as error:
        return errorProcess(error,str(private_key)+'Private Key could not be read')
    except Exception as error:
        return errorProcess(error)
    url = api_endpoint + 'prov/v1/customCertificate/upload'
    try:
        if(passphrase is not None):
            payload = {
                'api_id':api_id,
                'api_key':api_key,
                'site_id':site_id,
                'certificate':cert,
                'private_key':privKey,
                'passphrase':passphrase
            }
        else:
            payload = {
                'api_id':api_id,
                'api_key':api_key,
                'site_id':site_id,
                'certificate':cert,
                'private_key':privKey
            }
        r = requests.post(url, data=payload)
        return r.text
    except Exception as error:
        return errorProcess(error)

def incapsula_upload_certificate(SITE_ID, API_ID, API_KEY, TLSCert, TLSPriv, TLSPass):
    """
    Uploads a custom certificate and private key to Incapsula
    :param SiteName: Site DNS entry
    :param TLSCert: Path to TLS Certificate
    :param TLSPriv: Path to TLS Certificate private key
    :return: Status message of request
    """
    logger.info('Uploading TLS certificate')
    # Get password from command line input
    # Encode password in UTF8
    TLSPass_Bytes = TLSPass.encode("utf-8")

    # Base64 encode the Certificate
    with open(TLSCert, 'rb') as f:
        TLSCert64 = base64.b64encode(f.read())

    # Base64 encode the decrypted Private Key
    with open(TLSPriv, 'rb') as f:
        TLSPriv64 = base64.b64encode(
            crypto.dump_privatekey(
                crypto.FILETYPE_PEM,
                crypto.load_privatekey(
                    crypto.FILETYPE_PEM,
                    f.read(),
                    TLSPass_Bytes
                )
            )
        )

    try:
        response = requests.post(
            api_endpoint + 'prov/v1/sites/customCertificate/upload',
            data={
                'api_id': API_ID,
                'api_key': API_KEY,
                'site_id': SITE_ID,
                'certificate': TLSCert64,
                'private_key': TLSPriv64,
            }
        )

        # Consider any status other than 2xx an error
        if not response.status_code // 100 == 2:
            return "error: unexpected response {}".format(response)

        site_data = response.json()

        # Look for a 'res' code that's not 0 from the Incapsula API; something went wrong
        if int(site_data['res']) != 0:
            logger.error("Error uploading cert: {} - {}".format(site_data['res_message'],site_data['debug_info']))
            return
        else:
            logger.info('Certificate uploaded successfully')
            return

    except requests.exceptions.RequestException as e:
        # A serious problem happened, like an SSLError or InvalidURL
        return "error: {}".format(e)