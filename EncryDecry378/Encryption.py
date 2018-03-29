from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa as rsa, padding as opad
from cryptography.hazmat.primitives import hmac
import base64
import pdb
import Constants as const
import os

##########################################################
# Using a generated IV and predetermined key, a file is 
# encrypted using AES-256 CBC
#
# Then using a MAC function, a tag is generated
##########################################################
def MyEncryptMAC(file, key, HMACKey):
    #Return an error if the key length is not length 32
    if(len(key) != const.ENC_DEC_KEY_LENGTH) :
        raise ValueError('Key length must be of size 32')
    
    #Generate an IV of length 16
    IV = generateRandom(const.IV_KEY_LENGTH)
    
    #Generate cipher text
    cipher = createCipher(IV, key)
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(file) + encryptor.finalize()

    #The file has been encrypted, go ahead and output a tag for the 
    #encrypted file using the HMACKey
    h = hmac.HMAC(HMACKey, algorithm=hashes.SHA256(), backend=default_backend())
    h.update(cipher_text)
    tag = h.finalize()

    #Return the encrypted message, the IV, and the HMAC tag
    return cipher_text, IV, tag

##########################################################
# Using a 32-bit generated key, a file will be read into 
# Myencrypt to be encrypted, then stored into a JSON file.
##########################################################
def MyfileEncryptMAC(file_path):
    #Generates 32-bit key for file encryption
    encKey = generateRandom(const.ENC_DEC_KEY_LENGTH)
    #Retrieve a padded file from the specified file_path variable
    file = get_padded_file(file_path)
    #Now generate an HMAC Key for a tag
    HMACKey = generateRandom(const.HASH_KEY_LENGTH)
    
    #Encrypt the above file with the generated encryption key and HMACKey
    cipher_text, IV, tag = MyEncryptMAC(file, encKey, HMACKey)
    
    #Encode the cipher text
    encoded_cipher_text = encode_text(cipher_text)
    encoded_IV = encode_text(IV)
    encoded_tag = encode_text(tag)

    #Extract the file enxtension from the file path
    split_string = file_path.split('.')
    file_name = split_string[0]
    file_extension = '.' + split_string[len(split_string) - 1]

    #Return the generated cipher text, 16-bit IV, 32-bit Key, and the
    #File extension
    return encoded_cipher_text, encoded_IV, encKey, file_extension, file_name, HMACKey, encoded_tag

############################################################################
#   Encrypts the Key and HMACKey using RSA
############################################################################
def MyRSAEncrypt(file_path):
    encoded_cipher_text, encoded_IV, encKey, file_extension, file_name, HMACKey, encoded_tag = MyfileEncryptMAC(file_path)
    # Load RSA public key
    public_key = getPK()
    
    keys = encKey + HMACKey
    
    ciphered_key = public_key.encrypt(
        keys,
        opad.OAEP(
            mgf=opad.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None))

    #Encode the ciphered key
    encoded_cipher_key = encode_text(ciphered_key)

    return encoded_cipher_text, encoded_IV, encoded_cipher_key, file_extension, file_name, encoded_tag

############################################################################
#   Generates magic box to encrypt and decrypt files
############################################################################
def createCipher(iv, key):
    if(len(key) != 32) :
        raise ValueError('Key length must be of size 32')
    #Encrypt the message using the key and IV in CBC mode in AES
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    return cipher

#############################################################################
#Retrieves the private key from a PEM file
#############################################################################
def getPK():
    private_key = None

    while True:
        password = input("Password Required: ")
        password = bytes(password, "utf-8")
        # Retrieves Crypto-Key Object from PEM file
        try:
            with open("aliKey.pem", "rb") as key_file:
                    private_key = serialization.load_pem_private_key(
                        key_file.read(),
                        password=password,
                        backend=default_backend())
        except:
            print("Bad password. Try again.")
        # Retrieve public key from Crypto-Key Object
        if private_key != None:
            pk = private_key.public_key()
            return pk

#############################################################################
#Given a file path, pads the file
#############################################################################
def get_padded_file(file_path): 
    read_file = None
    
    #Read the file from the file path
    with open(file_path, mode='rb') as file:
        read_file = file.read()
        
    #Pad the file
    padded_file = padFile(read_file)
    
    #Return the padded version of the file
    return padded_file

#############################################################################
# A given file is padded into 128-bit blocks so that it 
# be ecrypted.
#############################################################################
def padFile(file):
    padder = padding.PKCS7(128).padder()
    pddFile = padder.update(file)
    pddFile += padder.finalize()
    return pddFile

##############################################################################
#Generates a key given the length of the key to generate
##############################################################################
def generateRandom(key_length):
    return os.urandom(key_length)

##############################################################################
#Encodes the string in base64
##############################################################################
def encode_text(string):
    return base64.b64encode(string)

##############################################################################
#Stringifies all of the items in the list
##############################################################################
def stringify(item_list):
    #Holds all of the decoded items
    stringified_items = list()
     
    #Turns each of the items in the list into a string
    for i in range(len(item_list)):
        stringified_items.append(str(item_list[i]))
    
    #Returns the stringified items 
    return stringified_items[0], stringified_items[1], stringified_items[2], stringified_items[3]

##############################################################################
#Divides the file_path into the file name and the extension associated with
#the file path
##############################################################################
def extractFileExtension(file_path) :
    #Split the string
    split_string = file_path.split('.')
    #Extract the the file name from the file path
    file_name = split_string[0]
    #Extract the extension from the file path
    file_extension = '.' + split_string[len(split_string) - 1]
    
    #Return the extracted file name and file extension
    return file_name, file_extension