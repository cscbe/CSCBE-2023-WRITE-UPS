# SquareGuard Part: II

## Category
Reversing

## Estimated difficulty
Hard (or Easy?)

## Description
This is a follow-up on the Part I, except this one comes with 'obfuscation' (just kidding, its compiled with `-O3`. Some functions should be inlined and optimized making it a bit more obscure). 

## Scenario
Good job. Our customer was impressed with your findings and asked us to obfuscate the application. We think we fixed most of them. Please have another look at the application and pay close attention to the 'obfuscated' code to find what you are looking for.

## Write-up
(I expect Part I to be solved prior to Part II.)

A student should find out that the Part II is based on Part I, either by looking at the similarities in the app UI, `.so` or scenario.

With the prior knowledge of Part I, the student should look for the function containing all the main logic.

This time, the function is a bit bigger as things have been optimized and inlined.

Comparing the decompiled function with the Part I decompiled function will help the reversing and shows how the 'obfuscation' (compiler optimization) produced code that is different but semantically the same.

It shouldn't be much longer until one understands what is going on, locates the new encrypted string and finds out where it is checked.

Repeat the same attack to extract the XOR key and the encrypted key can be decrypted once again.

## PoC script
N/A

## Flag
`CSC{0BFU5CAT10N_I5_G00D}`

## Creator
Sander Smets

## Creator bio
Security Researcher @ GuardSquare