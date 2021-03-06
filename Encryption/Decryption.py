import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, serialization, hashes, hmac
from cryptography.hazmat.primitives.asymmetric import rsa, padding as opad
import base64
import Constants as const
import json
import sys
import keys

#########################################################################
# Takes an encrypted file and decrypts it
#########################################################################
def MyfileDecrypt(file_path):
    json_data = json.load(open(file_path))
    file_extension = json_data[const.EXT]
    file_cipher = json_data[const.CIPHER]
    IV = json_data[const.IV]
    keys = json_data[const.KEY]
    tag = json_data[const.TAG]
    #Byte-ify the following
    file_cipher = to_bytes(file_cipher)
    IV = to_bytes(IV)
    keys = to_bytes(keys)
    tag = to_bytes(tag)
    #Decode the bytes
    file_cipher = base64.b64decode(file_cipher)
    IV = base64.b64decode(IV)
    keys = base64.b64decode(keys)
    tag = base64.b64decode(tag)

    return file_cipher, IV, keys, file_extension, tag


############################################################################
# Given an AES-256 Cipher Text,key, and iv; a cipher text
# is decrypted.
############################################################################
def MyDecrypt(cipher_text, key, iv):
    if(len(key) != const.ENC_DEC_KEY_LENGTH and len(iv) != const.IV_KEY_LENGTH) :
        raise ValueError('Key/IV length is mismatched.')
    cipher = createCipher(iv, key)
    decryptor = cipher.decryptor()
    file = decryptor.update(cipher_text) + decryptor.finalize()
    file = unpadFile(file)

    return file

#############################################################################
#   Generates magic box to encrypt and decrypt files
#############################################################################
def MyRSADecrypt(file_path, crypto):
    #Retrieve items from the file path specified
    file_cipher, IV, key, file_extension, tag = MyfileDecrypt(file_path)

    key = crypto.decrypt(
            key,
            opad.OAEP(
                    mgf=opad.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None))
    HMAC, key = getHMAC(key)

    #Run my decrypt to decrypt the file and return the decrypted file
    if(isValidFile(file_cipher, HMAC, tag)):
        contents = MyDecrypt(file_cipher, key, IV)
    else:
        raise ValueError('Tag or File is not intact. Dumping Package.')
    split_string = file_path.split('.')
    file_name = split_string[0]

    f = open(file_name + file_extension, "wb+")
    f.write(contents)

    return

def verify_decryption_password(appKey, password) :
    crypto = None
    prk_bytes = keys.get(appKey, password)
    prk_bytes = base64.b64decode(to_bytes(prk_bytes))
    crypto = serialization.load_pem_private_key(
        prk_bytes,
        password=None,
        backend=default_backend()
    )
    if(crypto != None) :
        return crypto
    else:
        sys.exit()

#############################################################################
#   Generates magic box to encrypt and decrypt files
#############################################################################
def createCipher(iv, key):
    if(len(key) != 32) :
        raise ValueError('Key length must be of size 32')
    #Decrypt the message using the key and IV in CBC mode in AES
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)

    return cipher

#############################################################################
#   Unpads the given file
#############################################################################
def unpadFile(file):
     unpadder = padding.PKCS7(128).unpadder()
     data = unpadder.update(file)
     data += unpadder.finalize()
     return data

#############################################################################
# Turns string files into bytes
#############################################################################
def to_bytes(string):
    byte_string = string[2 : len(string) - 1]
    return bytes(byte_string, 'utf-8')

#############################################################################
# Parse HMAC key from stored key
#############################################################################
def getHMAC(key):
    hmac = key[32:64]
    key = key[:32]
    return hmac, key

def isValidFile(cipher_text, HMACKey, tag):
    h = hmac.HMAC(HMACKey, algorithm=hashes.SHA256(), backend=default_backend())
    h.update(cipher_text)
    hTag = h.finalize()

    if(hTag==tag):
        return True
    return False
