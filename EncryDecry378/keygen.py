from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import Constants as const

privateKey = rsa.generate_private_key(
    public_exponent=const.PUBLIC_EXPONENT,
    key_size= const.RSA_KSZ,
    backend=default_backend())

with open("aliKey.pem", "wb") as f:
    f.write(privateKey.private_bytes(
        encoding = serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(b"penguinflower"),
    ))
