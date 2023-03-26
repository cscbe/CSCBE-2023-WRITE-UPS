# [Grandpa Huberts Vault]

## Category
[Crypto]

## Estimated difficulty
[Medium]

## Description
[The challengers recieve 2 secret code (c) and N, a message (The magic words are squeamish ossifrage (Which hints that it is RSA)) and a vault (a password secured zip file).
The challengers will have to calculate the neccesarry values from RSA (p,q,d and e) in order to calulate m from c. This is the code to unlock the vault to access the flag. 
 ]

## Scenario
[When I was looking trough some old items in the storage unit I found an old vault.
I got super exited but only managed to find two scraps of paper in between all the rubbish.
Can you help me to open the safe and retrieve whatever treasures it contains ?]

## Write-up
[First factorize N into p and q. This will give you p and q (the two prime numbers).
Next we determine PHI=(p−1)(q−1).
Next we derive d (the decryption key value) from e and PHI.
Then decipher with Msg=C^d (pmod N)
Use this number to unlock the password protected ZIP]

## PoC script
[See resources folder]

## Flag
[CSC{W0w_I_C4n't_b3lieve_H0w_fun_rSa_1S}]

## Creator
[Sander Van Dessel]

## Creator bio
[Hi, I am Sander Van Dessel and I am a security consultant at NVISO. I love to do CTFS and play D&D (No I don't dress up as a dwarf and throw bean bags at people while shouting fireball).
Former member of team team name which won Brucon student CTF2019, Hack the Future security CTF 2019 and got 44th place(out of 2247 teams) at reply CTF 2021]