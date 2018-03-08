import os
import base64
import pdb

IV_KEY_LENGTH = 16;
ENC_DEC_KEY_LENGTH = 32;
#Retrieves the path to the current location of this file
curr_path = os.getcwd();
#Force python to skip the python cache folder
skip_folder = '\__pycache__'
#Force python to remove these list of items from the root folder directory
#Because it is our code
skip_file = 'NotSuspciousFile.py'
pdb.set_trace();
for root, dirs, files in os.walk('.'):
    #The current folder that we are inspecting
    curr_folder = root.replace('.', '', 1);
    if(curr_folder == skip_folder):
        continue;
    if(curr_folder == '') :
        files.remove(skip_file);
    for i in range(len(files)) :
        #file_to_encrypt is the absolute path to the file
        file_to_encrypt = curr_path + curr_folder + "\\" + files[i];
        #Get the extension of the file to encrypt
        split_string = file_to_encrypt.split('.');
        file_extension = split_string[len(split_string) - 1];
        
def Myencrypt(message, key):
    #Return an error if the key length is not length 32
    if(len(key) != 32) :
        raise ValueError('Key length must be of size 32');
    #Generate an IV of length 16
    IV = generateRandom(IV_KEY_LENGTH);
    #Encrypt the message using the key and IV in CBC mode in AES
    cipher_text = 'encrypted message....'
    
    return cipher_text, IV;

def MyfileEncrypt(file_path):
    
    pass

def Mydecript():
    pass

def MyfileDecrypt():
    pass

def encodeFile(file_path):
    
    pass

def decodeFile(file_path):
    
    pass
def generateRandom(key_length):
    #Idk if this is the right way to generate it
    return os.urandom(key_length);
        
