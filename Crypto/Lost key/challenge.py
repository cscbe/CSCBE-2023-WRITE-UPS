from Crypto.Util.number import *
from Crypto.Cipher import AES
import string
import random
import os
import binascii

flag = b'Flag: CSC{' + binascii.hexlify(os.urandom(6)) + b'}'

plaintext = os.urandom(16)

ciphertext = plaintext
for i in range(0, len(flag), 16):
    key = flag[i:i+16]
    key = key.ljust(16, b' ')
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(ciphertext)

print(flag.decode())
print("Plaintext:", binascii.hexlify(plaintext).decode())
print("Ciphertext:", binascii.hexlify(ciphertext).decode())


