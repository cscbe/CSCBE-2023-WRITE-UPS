#!/usr/bin/env python3

from Crypto.Cipher import AES
import os
import string

def verify(password, saved_password):
    if len(password) <= 7:
        return False
    for c in password:
        if c not in string.printable:
            return False

    return saved_password['hash'] == my_hash(password, saved_password['salt'])

def pad(inp):
    return inp.ljust(16, b'\00')

def my_hash(password, salt):
    password = password.encode()
    last_output = bytes(16)
    for i in range(0, len(password), 16):
        block = pad(password[i:i+16])
        key = bytes([block[i] ^ last_output[i] for i in range(16)])
        cipher = AES.new(key, AES.MODE_ECB)
        last_output = cipher.encrypt(salt)


    return last_output

SALT = pad(b'CSC!')

users = {
        'admin': {
            'salt': SALT,
            'hash': my_hash('admin', SALT)
            }
        }

print("Welcome to the CSCBE flag service.")
print("Please provide your credentials.")
username = input("What is your username?")
password = input("What is your password?")

if username not in users:
    print("Username not found.")
    exit()

credentials = users[username]

if verify(password, users[username]):
    print('Congratulations.')
    print(os.environ['FLAG'])
else:
    print('Invalid login.')
