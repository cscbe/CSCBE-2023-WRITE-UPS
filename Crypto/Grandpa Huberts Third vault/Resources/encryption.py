plaintext = "CSCBRACKETCHACHAREALSMOOTHBRACKET"
shift = 0
ciphertext = ""
for p in plaintext:
    c = chr((ord(p) - ord('A') + shift) % 26 + ord('A'))
    shift = ord(p) - ord('A') + 1
    ciphertext += c
print(ciphertext)