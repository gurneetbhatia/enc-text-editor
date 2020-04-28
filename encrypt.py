from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
#from cryptography.hazmat.primitives import serialization
'''
text provided is encrypted with an AES key
the AES key is encrypted with RSA encryption
'''
class Encrypt1:
    def __init__(self, keys=None):
        # keys[0] is the private key to encrypt/decrypt the aes key
        # keys[1] is the aes key to encrypt/decrypt the strings
        # aes key is provided in an encrypted format
        self.keys = self.get_new_keys() if keys == None else keys
        self.private_key = self.keys[0]
        self.aes_cipher = self.keys[1]
        # cipher.encryptor and cipher.decryptor

    def get_new_keys(self):
        private_key = rsa.generate_private_key(public_exponent=65537,
        key_size=4096,
        backend=default_backend())
        key = os.urandom(32)
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
        backend=default_backend())
        return [private_key, cipher]

    def get_public_key(self):
        return self.private_key.public_key()

    def encrypt_with_rsa(self, input):
        return private_key.public_key().encrypt(input,
        padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
        ))

    def decrypt_with_rsa(self, input):
        return self.private_key(input,
        padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
        ))



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
