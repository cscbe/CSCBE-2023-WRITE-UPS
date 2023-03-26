# SquareGuard Part: I

## Category
Reversing

## Estimated difficulty
Medium

## Description
The idea is to have a mobile application with a basic key generator. Passing in the correct key will return the expected flag _(using basic 4-byte XOR)_. The application is 'vulnerable' in that it checks the first 4 bytes of the decrypted flag against `CSC{` to validate if the input was correct. Students should be able to reverse-engineer the checking logic to calculate the XOR key.

The XOR Key has generated off a string. The student either reverse engineers how the string is generated to use the app to obtain the flag. Or one might locate the encrypted byte array and XOR against it using CyberChef or anything else.

## Scenario
We have an urgent request from a customer to pentest their unprotected application, but our pentest-team is on vacation. Can you have a look and give us what we need?

## Write-up
Unpack the APK using `apktool` and take out the `.so` libraries.

Throw the library into IDA (or a similar tool like Ghidra) and have a look at function names. The binary is pretty small, so functions named `extractKey`, `getEncryptedKey`, `Java_com_example_squareguard_MainActivity_authenticateKey` should grab the attention.

Looking around to see how they are used, it becomes clear that everything happens in `Java_com_example_squareguard_MainActivity_authenticateKey`. The function contains a nice loop where the encrypted flag is decrypted, followed by a nice big if statement that checks for the `CSC{`

```c
if(v11[0] == 0x43 && v11[1] == 83 && v11[2] == 67 && v11[3] == 66)
```

Now locate the array of bytes used in the loop and use CyberChef to XOR the first 4 bytes of the array against the 4 bytes found in the if statement. This will give the 4-byte key, which we then use to XOR against the byte array.

## PoC script
N/A

## Flag
`CSC{OBFUSCATION_NOT_FOUND}`

## Creator
Sander Smets

## Creator bio
Security Researcher @ GuardSquare