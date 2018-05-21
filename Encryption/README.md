# Encryption / Decryption Programs 

## Table of Contents
1. [Requirements](#requirements)
2. [Libraries](#libraries)
3. [Encryption](#encryption)
4. [Decryption](#decryption)
<a name="requirements"></a>
## Requirements
[Live Node.js Server]
* A live Node.js server implementing a RESTful API must be configured to send Responses and receive Requests from the program <br>

[Mongo Database in your Server]
* A local Mongo Database must be configured in your Node.js server to store each private key as the program instance is run
<a name="libraries"></a>
## Libraries
1. [Python OS Library](https://docs.python.org/3/library/os.html)
2. [Python Cryptography Hazmat Library](https://cryptography.io/en/latest/)
<a name="encryption"></a>
## Encryption
* File Encryption Algorithm
    * A cryptographically strong Private and Public Key pair is generated using a 4096 Byte Key to be used with an RSA algorithm
    * The generated Private Key is then stored in a live Node.js server configured with A+ SSL inside of its local Mongo database
    * In the Node.js server, a unique application JSON Web Token and a unique cryptographically random password is generated to be associated with the received Private Key
    * The Node.js server then sends the JWT as a response and the program stores the received JWT in a .txt file inside the same folder as the program
    * A recursive Breadth First Search algorithm goes through a folder to find all of the files to encrypt
    * A file is then read in as a string and padded using PKCS7 to be used with AES-CBC in 128-bit blocks
    * A unique cryptographically strong 16 Byte IV and 32 Byte Key are both generated using the Python OS Library to be used to encrypt the file
    * The padded file is then encrypted using the previously generated IV and Key using AES in CBC mode
    * A tag for the encrypted file is then generated using HMAC with a cryptographically strong 32 Byte Key, SHA256 as the hashing algorithm, and the encrypted file
    * The encrypted file, encryption IV, and HMAC Tag are then all encoded using base 64
    * The encryption Key and the HMAC Key are then concatenated and incrypted using the previously generated RSA Public Key
    * The concatenated encrypted keys are then encoded to base 64
    * The encoded encrypted file, encoded IV, encoded concatenated keys, and the encoded tag are all stringified and placed in a JSON structure and written to a file with the exact same name but with the .nsf extension
    * The algorithm terminates once all files have been encrypted successfully
<a name="decryption"></a>
## Decryption
* File Decryption Algorithm
   * The program retrieves the generatred JWT from the previously generated appKey.txt file and asks the user for a password
   * The program then sends a GET request to the Node.js server with the JWT and password
   * The Node.js server then querries a Key object using the received JWT and compares the passwords
   * If the password is incorrect, the server sends a 404 response to terminate the program, otherwise, the server sends the Private Key object instead with a 200 response code
   * The program then uses the same Breadth First Search algorithm to find and locate all of the files
   * Each file is read in and the encrypted file, AES encryption IV, concatenated keys, a HMAC Tag are all decoded from base 64
   * The concatenated AES encryption Key and HMAC Key is then unencrypted using the received Private Key from the server
   * The decoded TAG is then compared to check for manipulations in the encrypted file
   * If the encrypted file has been tempered with, the program will terminate, otherwise, it will continue on the next step
   * The file is then unencrypted using the AES encryption key and IV, then unpadded
   * The file is then written back with its original file name and original extension
   * The algorithm terminates once all files have been decrypted successfully
