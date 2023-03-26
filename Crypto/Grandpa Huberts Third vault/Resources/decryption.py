ciphertext = "CVVETSDNPYWKIDKISWFMEFBDIBJTSDNPY"
shift = 0
plaintext = ""
for c in ciphertext:
    p = chr((ord(c) - ord('A') - shift) % 26 + ord('A'))
    shift = ord(p) - ord('A') + 1
    plaintext += p
print(plaintext)