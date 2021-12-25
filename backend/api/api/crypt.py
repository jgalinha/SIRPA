from sqlalchemy.sql.functions import current_user
from passlib.context import CryptContext
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization as crypt_serialization

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Crypt():
    def bcrypt(password: str):
        return pwd_ctx.hash(password)

    
    # https://www.programcreek.com/python/?CodeExample=generate+key+pair
    # https://dev.to/aaronktberry/generating-encrypted-key-pairs-in-python-69b
    def generate_key_pair(password):
        bytes_password = bytes(password, "utf-8")
        # generate RSA key pair
        key_pair = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        # generate encrypted private key
        private_key = key_pair.private_bytes(
            crypt_serialization.Encoding.PEM,
            crypt_serialization.PrivateFormat.PKCS8,
            encryption_algorithm=crypt_serialization.BestAvailableEncryption(bytes_password))
            # crypt_serialization.NoEncryption()).decode('utf-8')
        # generate public key
        public_key = key_pair.public_key().public_bytes(
            crypt_serialization.Encoding.OpenSSH,
            crypt_serialization.PublicFormat.OpenSSH).decode('utf-8')
        
        # return key pair tuple
        return public_key, private_key

