# [Grandpa Huberts third vault]

## Category
[Crypto]

## Estimated difficulty
[Medium/Hard]

## Description
[In this challenge, the challengers are given a ciphertext that was obtained by shifting each letter of a plaintext message by the numeric value of the previous one. 
Their task is to decrypt the message and find the original plaintext.
3 plaintext ciphertext pairs have been provided to give a hint]

## Scenario
[When Hubert was young, he and his friends used to create all kinds of crazy ciphers.
This cipher however was his favorite one since it was both easy and complex at the same time.
When I was looking trough his viewfinder, I even discoverd some pictures of his notes when he was exercising on the cipher by encrypting parts of his favorite songs.
One encrypted sentence however was missing the encrypted plaintext besides it.
Might this code contain the location of the rumored  third vault of Hubert ?
I quickly noted them down in the hopes of cracking his code later on.]

## Write-up
[Initialize a variable shift to 0.
For each letter in the ciphertext, convert it back to its corresponding plaintext letter by subtracting the current shift value (initially 0).
Update the shift value to be the numeric value of the current plaintext letter.
Repeat steps 2-3 for each subsequent letter until the end of the ciphertext is reached.

Using this algorithm, the plaintext "CSCBRA" would be encrypted as follows:

"C" is the first letter, so it stays the same: "C"
"S" is shifted by the numeric value of "C", which is 3. So, "S" becomes "V" (since "S" is the 19th letter of the alphabet, and 19 + 3 = 22, which is the letter "V"): "CV"
"C" is shifted by the numeric value of "S", which is 19. So, "C" becomes "V" (since "C" is the 3rd letter of the alphabet, and 3 + 19 = 22, which is the letter "V"): "CVV"
"B" is shifted by the numeric value of "C", which is 3. So, "B" becomes "E" (since "B" is the 2nd letter of the alphabet, and 2 + 3 = 5, which is the letter "E"): "CVVE"
"R" is shifted by the numeric value of "B", which is 2. So, "R" becomes "T" (since "R" is the 18th letter of the alphabet, and 18 + 2 = 20, which is the letter "T"): "CVVET"
"A" is shifted by the numeric value of "R", which is 18. So, "A" becomes "S" (since "A" is the 1st letter of the alphabet, and 1 + 18 = 19, which is the letter "S"): "CVVETS"]

## PoC script
[Both encryption and decryption poc script are included]

## Flag
[CSC{MAYBETHEREATREASUREWASTHEFRIENDSWEMADEALONGTHEWAY}]

## Creator
[Sander Van Dessel]

## Creator bio
[Hi, I am Sander Van Dessel and I am a security consultant at NVISO. I love to do CTFS and play D&D (No I don't dress up as a dwarf and throw bean bags at people while shouting fireball).
I also seem to have discoverd a passion for Hubert challenges.]

[- https://www.linkedin.com/in/sander-van-dessel-622aba144/]

