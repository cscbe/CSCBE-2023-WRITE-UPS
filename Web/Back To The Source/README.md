# Source maps

## Category
Web

## Estimated difficulty
Easy

## Description
Find out hidden functionality within the JavaScript source maps.
For debugging reasons, frameworks like React generate source maps.
Even if the JavaScript is obfuscated, there will be .map files which shows the original source code.

https://developer.chrome.com/blog/sourcemaps/

## Scenario

## Write-up
The flag is in 3 parts.

1st part: In the normal source code of index.html

2nd part: /manifest.json

3th part: Chrome Dev Tools -> Sources -> <website url>/static/js/pages/login/index.js (you can't view this by manually going to that URL, this is because Chrome Dev Tools takes the source .map)

## PoC script
N/A

## Flag
CSC{D0n7_93n3ra73_50Urc3_MaP2}

## Creator
Lesley De Keyser

## Creator bio
Lesley is currently a CSIRT & SOC Engineer at NVISO. He is an active CTF player, winning CSCBE in 2020, representing Belgium in ESCS Prague 2021 and winning Remote Cyber Battle of Nordic-Baltics in 2022.

You can find more about Lesley on [https://lesley.co](https://lesley.co) or [LinkedIn](https://linkedin.com/in/lesleydk/)