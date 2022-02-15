from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization as crypt_serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from icecream import ic
from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def bcrypt(password: str):
    return pwd_ctx.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_ctx.verify(plain_password, hashed_password)


# https://www.programcreek.com/python/?CodeExample=generate+key+pair
# https://dev.to/aaronktberry/generating-encrypted-key-pairs-in-python-69b
def generate_key_pair(password):
    """generate pair of keys

    Args:
        password (str): password to encrypt private key

    Returns:
        tuple: public and private key
    """
    # generate RSA key pair
    try:
        key_pair = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        # generate encrypted private key
        private_key = key_pair.private_bytes(
            encoding=crypt_serialization.Encoding.PEM,
            format=crypt_serialization.PrivateFormat.PKCS8,
            encryption_algorithm=crypt_serialization.BestAvailableEncryption(
                is_bytes(password)
            ),
        ).decode("utf-8")
        # encryption_algorithm=crypt_serialization.NoEncryption()).decode(utf-8')
        # generate public key
        public_key = (
            key_pair.public_key()
            .public_bytes(
                crypt_serialization.Encoding.OpenSSH,
                crypt_serialization.PublicFormat.OpenSSH,
            )
            .decode("utf-8")
        )

        # return key pair tuple
        return public_key, private_key
    except Exception as e:
        return {"error": "error generating key pair", "msg": f"{e}"}


def load_pub_key(public_key):
    """load RSA Public Key

    Args:
        public_key (bytes): The OpenSSH encoded key data

    Returns:
        RSAPublicKey: the RSA public key
    """
    try:
        return crypt_serialization.load_ssh_public_key(is_bytes(public_key))
    except ValueError as e:
        return {
            "error": "The OpenSSH data could not be properly decoded or if the key is not in the proper format",
            "msg": f"{e}",
        }
    except UnsupportedAlgorithm as e:
        return {
            "error": "The serialized key is of a type that is not supported",
            "msg": f"{e}",
        }
    except Exception as e:
        return {"error": "error loading public key", "msg": f"{e}"}


def load_priv_key(private_key, password):
    """load the RSAPrivatekey

    Args:
        private_key (bytes): the PEM encoded data
        password (bytes): password

    Returns:
        RSAPrivateKey: the RSA private key
    """
    try:
        kr = crypt_serialization.load_pem_private_key(
            is_bytes(private_key), password=is_bytes(password)
        )
        return kr
    except ValueError as e:
        return {
            "error": "PEM data's structure could not be decoded successfully",
            "msg": f"{e}",
        }
    except UnsupportedAlgorithm as e:
        return {
            "error": "The serialized key type is not supported by the OpenSSL version cryptography is using",
            "msg": f"{e}",
        }
    except Exception as e:
        return {"error": "error loadind private key", "msg": f"{e}"}


def sign(kr, data):
    """sign a data that can be verify by others with public key

    Args:
        kr (RSAPrivateKey): private key
        data (bytes): data to sign

    Returns:
        bytes: signature
    """
    try:
        data = data if isinstance(data, bytes) else bytes(data)
        signature = kr.sign(
            is_bytes(data),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return signature
    except ValueError as e:
        return {"error": "The data could not be encrypted", "msg": "{}".format(e)}
    except Exception as e:
        return {"error": "error singing the data", "msg": "{}".format(e)}


def verify(ku, data, signature):
    """Verify a sign data

    Args:
        ku (str): public key
        data (bytes): data to verify
        signature (str): data signature

    Returns:
        if data is valid return a data, else raise an error
    """
    try:
        ku.verify(
            signature,
            is_bytes(data),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return {"data": "data validated"}
    except InvalidSignature as e:
        return {"error": "Invalid signature", "msg": "{}".format(e)}
    except Exception as e:
        return {"error": "error verifying the data", "msg": "{}".format(e)}


def encrypt(key, data):
    """encrypt a data

    Args:
        key (RSAPublicKey): key to encrypt with
        data (bytes): data to encrypt

    Returns:
        bytes: encrypted data
    """
    try:
        return key.encrypt(
            is_bytes(data),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
    except Exception as e:
        return {"error": "error encrypting the data", "msg": "{}".format(e)}


def decrypt(key, ciphertext):
    """Decrypt an cipher

    Args:
        key (RSAPrivateKey): key to decrypt with
        ciphertext (bytes): The cipher text to decrypt

    Returns:
        bytes: Decrypted data
    """
    try:
        return key.decrypt(
            is_bytes(ciphertext),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
    except Exception as e:
        return {"error": "error decrypting the data.", "msg": "{}".format(e)}


def is_bytes(data):
    """check if a data are in bytes format

    Args:
        data: data to check

    Returns:
        bytes: an bytes formated data
    """
    try:
        if isinstance(data, bytes):
            return data
        else:
            return bytes(data, "utf-8")
    except Exception as e:
        return {"error": "error converting data to bytes", "msg": "{}".format(e)}
