import base64, os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


SALT_BYTES = 16

class Encrypter:
    def __init__(self, n=2**18, r=8, p=1):
        self.n = n
        self.r = r
        self.p = p

    def generate_key(self, password, salt):
        kdf = Scrypt(salt=salt, length=32, n=self.n, r=self.r, p=self.p)
        return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))

    def encrypt_token(self, key, token):
        salt = os.urandom(SALT_BYTES)
        key = self.generate_key(key, salt)
        ciphertext = Fernet(key).encrypt(token.encode("utf-8"))
        return base64.urlsafe_b64encode(salt + ciphertext)

    def decrypt_token(self, key, encrypted_token):
        raw = base64.urlsafe_b64decode(encrypted_token)
        salt, ciphertext = raw[:SALT_BYTES], raw[SALT_BYTES:]
        key = self.generate_key(key, salt)
        return Fernet(key).decrypt(ciphertext).decode("utf-8")

