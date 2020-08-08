import base64
import os
import codecs
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import padding

def generate_keys():
    private_key = rsa.generate_private_key(
         public_exponent=65537,
         key_size=2048,
         backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def symmetric_crypto(password, salt):
    password = password.encode()
    kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt.encode(),
            iterations=100000,
            backend=default_backend()
        )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return Fernet(key)

def load_key(key, key_password):
    if isinstance(key, str) and key.startswith("-----BEGIN"):
        pass
    elif isinstance(key, str) or isinstance(key, Path):
        f = open(key, "rb")
        key = f.read()
        f.close()
    else:
        return key
    if "PRIVATE" in key:
        p_key = serialization.load_pem_private_key(
                key.encode(),
                password=None,
                backend=default_backend()
            )
    elif "PUBLIC" in key:
        p_key = serialization.load_pem_public_key(key.encode(), backend=default_backend())
    else:
        raise Exception("Could not determine the key type (private/public)")
    return p_key

def save_key(key, path, key_password=None):
    try:
        if password:
            enc = serialization.BestAvailableEncryption(password.encode())
        else:
            enc = serialization.NoEncryption()
        private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8,encryption_algorithm=enc)
    except:
        pem = key.public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)
    with open(path, "rb") as writer:
        for l in pem.splitlines():
            writer.write(l)
            writer.write(b"\n")

class CryptoReadStream():
    def __init__(self, file, password=None, salt="", key=None, key_password=None):
        if password and key:
            raise Exception("Specify password for symmetric encryption or key of asymmetric encryption. Not both!")
        if password:
            self.f = symmetric_crypto(password, salt)
            self.crpyto_args = []
        elif key:
            self.f = load_key(key, key_password)
            self.crpyto_args = [padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None)]
        else:
            raise Exception("Specify either a password (symmetric) or a key (asymmetric) ")
        self.file_handle = codecs.open(file, "r", encoding="utf-8")

    def read(self):
        return "\n".join(self.readlines())

    def readlines(self):
        return [self._decrypt(x) for x in self.file_handle.readlines()]

    def readline(self):
        return self._decrypt(self.file_handle.readline())

    def _decrypt(self,text):
        decrypted_texts = []
        for part in text.split("!"):
            if len(part) == 0:
                continue
            part = base64.urlsafe_b64decode(part)
            p = self.f.decrypt(part, *self.crpyto_args)
            decrypted_texts.append(p)
        return "".join([x.decode("utf-8") for x in decrypted_texts])

    def close(self):
        self.file_handle.close()
        
    def __next__(self):

        """ Return the next decoded line from the input stream."""
        line = self.readline()
        if line:
            return line
        raise StopIteration

    def __iter__(self):
        return self

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()

class CryptoWriteStream():
    def __init__(self, file, password=None, salt="", key=None, key_password=None, allow_overwrite=True, append=False):
        if password and key:
            raise Exception("Specify password for symmetric encryption or key of asymmetric encryption. Not both!")
        if password:
            self.f = symmetric_crypto(password, salt)
            self.crpyto_args = []
        elif key:
            self.f = load_key(key, key_password)
            self.crpyto_args = [padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None)]
        else:
            raise Exception("Specify either a password (symmetric) or a key (asymmetric) ")
        mode = "w"
        if append:
            mode = "a"
        elif not allow_overwrite:
            mode = "x"
        self.file_handle = codecs.open(file, mode,encoding="utf-8")

    def close(self):
        self.file_handle.close()

    def write(self, text, line_breaks=True):
        self.file_handle.write(self._encrypt(text, line_breaks=line_breaks))

    def _encrypt(self, text, line_breaks=True):
        if line_breaks:
            s = [self.f.encrypt(x.encode(), *self.crpyto_args) for x in text.split("\n")]
            crypt = "\n".join([base64.urlsafe_b64encode(x).decode("utf-8")  for x in s])
        else:
            crypt = base64.urlsafe_b64encode(self.f.encrypt(text.encode(), *self.crpyto_args)).decode("utf-8") 
        return crypt + "!"
            
    def writelines(self, list, line_breaks=True):
        self.write("".join(list))

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, tb):
        self.close()