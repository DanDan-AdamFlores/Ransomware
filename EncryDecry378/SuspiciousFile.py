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
    #Unstrigify the item
    print(file_path)
    json_data = json.load(open(file_path))
    file_extension = json_data[const.EXT]
    file_cipher = json_data[const.CIPHER]
    IV = json_data[const.IV]
    key = json_data[const.KEY]
    
    #Byte-ify the following
    file_cipher = to_bytes(file_cipher)
    IV = to_bytes(IV)
    key = to_bytes(key)
    
    #Decode the bytes
    file_cipher = base64.b64decode(file_cipher)
    IV = base64.b64decode(IV)
    key = base64.b64decode(key)
    
    #Run my decrypt to decrypt the file and return the decrypted file
    contents = MyDecrypt(file_cipher, key, IV)
    
    split_string = file_path.split('.')
    file_name = split_string[0]
    
    f = open(file_name + file_extension, "wb+")
    f.write(contents)
    
    return 
    

##########################################################
# Given an AES-256 Cipher Text,key, and iv; a cipher text 
# is decrypted.
##########################################################
def MyDecrypt(cipher_text, key, iv):
    if(len(key) != const.ENC_DEC_KEY_LENGTH and len(iv) != const.IV_KEY_LENGTH) :
        raise ValueError('Key/IV length is mismatched.')
    cipher = createCipher(iv, key)
    decryptor = cipher.decryptor()
    file = decryptor.update(cipher_text) + decryptor.finalize() 
    file = unpadFile(file)
    
    return file

##########################################################
#   Generates magic box to encrypt and decrypt files
##########################################################
def createCipher(iv, key):
    if(len(key) != 32) :
        raise ValueError('Key length must be of size 32')
    #Encrypt the message using the key and IV in CBC mode in AES
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    return cipher

def unpadFile(file):
     unpadder = padding.PKCS7(128).unpadder()
     data = unpadder.update(file)
     data + unpadder.finalize()
     return data
 
def to_bytes(string):
    byte_string = string[2 : len(string) - 1]
    return bytes(byte_string, 'utf-8')

if __name__ == '__main__':
    #Retrieves the path to the current location of this file
    curr_path = os.getcwd()
    #Force python to skip the python cache folder
    skip_folder = '\__pycache__'
    #Force python to remove these list of items from the root folder directory
    #Because it is our code
    skip_file_list = list(['NotSuspciousFile.py', 'SuspiciousFile.py', 'Constants.py', 'Constants.pyc'])
    for root, dirs, files in os.walk('.'):
        #The current folder that we are inspecting
        curr_folder = root.replace('.', '', 1)
        if(curr_folder == skip_folder):
            continue
        if(curr_folder == '') :
            for i in skip_file_list:
                files.remove(i)
        for i in range(len(files)) :
            #file_to_encrypt is the absolute path to the file
            file_path = curr_path + curr_folder + "/" + files[i]
            MyfileDecrypt(file_path)