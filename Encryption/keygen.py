from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
# from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKeyWithSerialization, RSAPublicKeyWithSerialization
import Constants as const
import keys

def generate_PEM() :
    privateKey = rsa.generate_private_key(
        public_exponent=const.PUBLIC_EXPONENT,
        key_size= const.RSA_KSZ,
        backend=default_backend())
    
    # Post keys to server
    appKey = keys.post(privateKey)

    # Save public key to local machine
    with open("aliKey.pem", "wb") as f:
        f.write(privateKey.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo))

    return appKey