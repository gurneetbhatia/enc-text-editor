from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as a_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os
#from cryptography.hazmat.primitives import serialization
'''
text provided is encrypted with an AES key
the AES key is encrypted with RSA encryption
'''
class Encrypt:
    def __init__(self, keys=None):
        # keys[0] is the private key to encrypt/decrypt the aes key
        # keys[1] is the aes key to encrypt/decrypt the strings
        # aes key is provided in an encrypted format
        self.keys = self.get_new_keys() if keys == None else keys
        self.private_key = self.keys[0]
        self.aes_cipher = self.keys[1]
        self.block_size = 128
        # cipher.encryptor and cipher.decryptor

    def get_new_keys(self):
        private_key = rsa.generate_private_key(public_exponent=65537,
        key_size=4096,
        backend=default_backend())
        key = self.encrypt_with_rsa(os.urandom(32), private_key)
        iv = self.encrypt_with_rsa(os.urandom(16), private_key)
        # cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
        # backend=default_backend())
        # key and iv will be used to construct the cipher
        return [private_key, (key, iv)]

    def encrypt_with_cipher(self, input):
        key = self.decrypt_with_rsa(self.aes_cipher[0])
        iv = self.decrypt_with_rsa(self.aes_cipher[1])
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
        backend=default_backend())
        encryptor = cipher.encryptor()
        input = bytes(input, 'utf-8')
        padder = padding.PKCS7(self.block_size).padder()
        padder_data = padder.update(input) + padder.finalize()
        return encryptor.update(padder_data) + encryptor.finalize()

    def decrypt_with_cipher(self, input):
        key = self.decrypt_with_rsa(self.aes_cipher[0])
        iv = self.decrypt_with_rsa(self.aes_cipher[1])
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv),
        backend=default_backend())
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(self.block_size).unpadder()
        padded_data = decryptor.update(input) + decryptor.finalize()
        return (unpadder.update(padded_data) + unpadder.finalize()).decode('utf-8')


    def get_public_key(self):
        return self.private_key.public_key()

    def encrypt_with_rsa(self, input, key=None):
        private_key = self.private_key if key == None else key
        return private_key.public_key().encrypt(input,
        a_padding.OAEP(
        mgf=a_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
        ))

    def decrypt_with_rsa(self, input, key=None):
        private_key = self.private_key if key == None else key
        return private_key.decrypt(input,
        a_padding.OAEP(
        mgf=a_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
        ))



'''class Encrypt:
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
        return msg.decode('utf-8')'''

    #def run(self, filepath, organisation, password):
