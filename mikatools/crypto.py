import base64
import os
import codecs
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class CryptoReadStream():
    def __init__(self, file, password, salt=""):
        password = password.encode()
        kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt.encode(),
                iterations=100000,
                backend=default_backend()
            )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        self.f = Fernet(key)
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
            p = self.f.decrypt(part)
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
    def __init__(self, file, password, salt="", allow_overwrite=True, append=False):
        password = password.encode()
        kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt.encode(),
                iterations=100000,
                backend=default_backend()
            )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        self.f = Fernet(key)
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
            s = [self.f.encrypt(x.encode()) for x in text.split("\n")]
            crypt = "\n".join([base64.urlsafe_b64encode(x).decode("utf-8")  for x in s])
        else:
            crypt = base64.urlsafe_b64encode(self.f.encrypt(text.encode())).decode("utf-8") 
        return crypt + "!"
            
    def writelines(self, list, line_breaks=True):
        self.write("".join(list))

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, tb):
        self.close()