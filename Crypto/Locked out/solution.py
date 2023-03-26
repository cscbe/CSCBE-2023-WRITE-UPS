from pwn import *
import random
from Crypto.Cipher import AES

HOST = 'localhost'
PORT = 49156
FILENAME = "./challenge.py"
LOCAL=False

context.log_level = 'debug'

def pad(inp):
    return inp.ljust(16, b'\00')

target = pad(b'admin')
salt = pad(b'CSC!')
alphabet = set(string.printable)
alphabet.remove('\n')

def attempt():
    global target, salt
    guess = ''.join(random.choices(string.ascii_letters + string.digits, k=16)).encode()
    cipher = AES.new(guess, AES.MODE_ECB)
    encrypted = cipher.encrypt(salt)

    answer = ''.join([chr(encrypted[i] ^ target[i]) for i in range(16)])
    for c in answer:
        if c not in alphabet:
            return None

    return guess+ answer.encode()

answer = None
i = 0
while answer is None:
    i += 1
    if i % 100000 == 0:
        print(i)
    answer = attempt()

print(answer)


if LOCAL:
    r = process(FILENAME)
else:
    r = remote(HOST,PORT)



r.recvuntil('username?')
r.sendline('admin')
r.recvuntil('password?')
r.sendline(answer)
print(r.recvall())
