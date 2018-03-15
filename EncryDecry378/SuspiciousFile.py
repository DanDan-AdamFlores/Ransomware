import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
import pdb
import Constants as const
import json

##########################################################
# Takes an encrypted file and decrypts it
##########################################################
def MyfileDecrypt(file_path):
    #Generates 32-bit key
    key = generateRandom(const.ENC_DEC_KEY_LENGTH)
    #Retrieve a padded file from the specified file_path variable
    file = get_padded_file(file_path)
    #Encrypt the above file
    cipher_text, IV = MyEncrypt(file, key)
    #Encode the cipher textex
    encoded_cipher_text = encode_text(cipher_text)
    encoded_IV = encode_text(IV)
    encoded_key = encode_text(key)
    #Extract the file enxtension
    split_string = file_path.split('.')
    file_name = split_string[0]
    file_extension = '.' + split_string[len(split_string) - 1]

    #Return the generated cipher text, 16-bit IV, 32-bit Key, and the
    #File extension
    return encoded_cipher_text, encoded_IV, encoded_key, file_extension, file_name
    

##########################################################
# Given an AES-256 Cipher Text,key, and iv; a cipher text 
# is decrypted.
##########################################################
def MyDecrypt(cipher_text, key, iv):
    if(len(key) != const.ENC_DEC_KEY_LENGTH and len(iv) != const.IV_KEY_LENGTH) :
        raise ValueError('Key/IV length is mismatched.')
    cipher = createCipher(iv, key)
    decryptor = cipher.decryptor()
    decryptor.update(cipher_text) + decryptor.finalize() 
    return 