from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
#from cryptography.hazmat.primitives import serialization

class Encrypt:
    def __init__(self, key=None):
        # optional argument of key allows the user to load pre-existent keys
        self.privateKey = self.getNewKey() if key==None else key

    def getNewKey(self):
        return rsa.generate_private_key(public_exponent=65537,
        key_size=4096,
        backend=default_backend())

    def getPublicKey(self):
        return self.privateKey.public_key()

    def encrypt_string(self, string):
        string = bytes(string, encoding='utf-8')
        return self.getPublicKey().encrypt(string,
        padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
        ))

    def decrypt_string(self, string):
        msg = self.privateKey.decrypt(string,
        padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
        ))
        return msg.decode('utf-8')

    #def run(self, filepath, organisation, password):
