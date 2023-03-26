# [Blink]

## Category
Misc 

## Estimated difficulty
Medium 

## Description
Understand AVR assembler source code for Arduino to interpret led signals sent from an Arduino.

## Scenario
We keep finding these strange devices lying around. We just captured a video of one of them blinking! 

We were also able to obtain the source code of an enigmatic "module.S", which we believe is somehow connected to the devices. Could it be the key to solving the mystery of the beacons?

## Write-up
The Arduino shown in the video ("device.m4v") is transmitting a secret message bit by bit, by making the onboard led blink. 

There are two kinds of blinks, one short (the led is on for 400ms) and one long (the led is on for 1s). The long blinks encode a "0" bit and the short blinks encode a "1" bit. This behaviour is fully controlled by the code in the module.S file, which contains AVR assembly code for an Arduino board. 

The module.S file provided to the participants has been stripped of all comments and some descriptive variable names. A fully commented version of the module.S file is provided in the Resources ("module.S_commented") :)

The Arduino sketch that calls the module.S code is also provided in the Resources for context ("blink.ino"), but is not required to solve the challenge (or to understand the solution).

The code in module.S performs two tasks: 

1) First, in the "preprocess" function, it XORs each byte of the secret message (flag) with a key. The XOR key ("theyAr3Am0ngUs!") is included in the module.S source code, but the secret message is not. 
2) Then, in the "beacon" function, it loops over the bytes of the XORed message, and for each byte it loops over its bits with the help of a bitmask (in "beaconByte"). When: 
- bit == 1, it turns on the onboard led for 400ms
- bit == 0, it turns on the onboard led for 1s

Given this knowledge, these are the steps required to solve the challenge: 

1) Watch the video and transcribe the blinks to a series of bits: 1 for the short blinks, 0 for the long ones. This gives the following sequence (separated in bytes for easier reading):

00110111 00111011 00100110 00000010 00100011 00011110 00010010 00101111 00000110 01110010 00100010 01010110 00111011 00011000 01011100

2) The bit sequence above needs to the XORed with the key included in the module.S source code, which is "theyAr3Am0ngUs!", or in binary: 

01110100 01101000 01100101 01111001 01000001 01110010 00110011 01000001 01101101 00110000 01101110 01100111 01010101 01110011 00100001

3) This gives the following result in binary: 

01000011 01010011 01000011 01111011 01100010 01101100 00100001 01101110 01101011 01000010 01001100 00110001 01101110 01101011 01111101 

which, converted to ASCII, gives the flag: "CSC{bl!nkBL1nk}" :) 

## PoC script
N/A 

## Flag
CSC{bl!nkBL1nk}

## Creator
Théo Rigas

## Creator bio
Hi there, I'm Théo Rigas and I work at NVISO as a cybersecurity expert. I'm currently focused on IoT and the S-SDLC, but I've dabbled in a little bit of everything, including web, mobile, and infrastructure pentesting. When I'm not busy trying to stop an army of killer fridges, I'm either nerding out over AI and programming or watching sports.

https://www.linkedin.com/in/theorigas/