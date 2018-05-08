import Constants as const
from cryptography.hazmat.primitives import padding, serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKeyWithSerialization, RSAPrivateKeyWithSerialization

import json
import os
import requests

# TODO: FIX URL Constants

############################################################################
#   Posts public and private key to the server
#   @params: pubKey -> Public Key, privKey -> PrivateKey
#   @return: AppKey to be able to retrieve the private key from server. 
############################################################################
def post(pubKey, privKey):
    pubKey, privKey = getBytes(pubKey, privKey)
    appKey = authUser()
    while True:
        r = requests.post(const.POST, data={'key1':appKey, 'key2':pubKey, 'key3':privKey })
        if (r.status_code == 200):
            break
    return appKey

# TODO: Need to figure out how to serialize and deserialize crypto objects
def get(appKey, pubKey):
    while True:
        r = requests.get(const.GET, data={'key1':appKey, 'key2':pubKey})
        if(r.status_code == 200):
            break
    r.encoding
    privKey = r.text
    return privKey

def authUser():
    while True:
        r = requests.get(const.GET, auth=('hackerman', 'allthedataz')) #autheticate to server 
        if(r.status_code == 200):
            break
    r.encoding
    appKey = r.text
    return appKey

def getBytes(pubKey, privKey):
    privKey = privKey.private_bytes(
            encoding = serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(b"penguinflower"),
        )
    pubKey = pubKey.public_bytes(
        encoding = serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(b"penguinflower"),
    )
    return pubKey, privKey

