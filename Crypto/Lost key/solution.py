from Crypto.Util.number import *
from Crypto.Cipher import AES
from progressbar import progressbar

pt = long_to_bytes(0xe70a9e673548ddd7869ffc29130525ad)
ct = long_to_bytes(0xb5db6e220c99af65eec03c3cb4e2cc4e)


middles = {}

alphabet = '0123456789abcdef'

for c1 in progressbar(alphabet):
    for c2 in alphabet:
        for c3 in alphabet:
            for c4 in alphabet:
                for c5 in alphabet:
                    for c6 in alphabet:

                        key1 = (c1 + c2 + c3 + c4 + c5 + c6).encode()
                        cipher = AES.new(b'Flag: CSC{' + key1, AES.MODE_ECB)
                        middle = cipher.encrypt(pt)
                        middles[middle] = key1

print("Middles generated")


for c1 in progressbar(alphabet):
    for c2 in alphabet:
        for c3 in alphabet:
            for c4 in alphabet:
                for c5 in alphabet:
                    for c6 in alphabet:
                        key2 = c1 + c2 + c3 + c4 + c5 + c6 + '}'
                        key2 = key2.ljust(16, ' ').encode()

                        cipher = AES.new(key2, AES.MODE_ECB)
                        middle = cipher.decrypt(ct)
                        if middle in middles:
                            print(b'CSC{' + middles[middle]+key2)

