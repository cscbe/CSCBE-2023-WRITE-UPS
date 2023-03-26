# Beep Boop

## Category
Web

## Estimated difficulty
Easy

## Description
Robots.txt page with some endpoints. One of these is where the flag is. 

## Scenario
My friend recently released a new business app, but he's worried that Beep Boop might discover something he hid on his website. 
Can you use your skills to find and retrieve it?

## Build

docker build challenge/Private/ -t beepboop && docker run -d -p 80:80 beepboop

## Write-up
There is a text in the first page that hint you to see the supbage "robots.txt"
Then, you have three endpoints. In the last, you have to check the HTML sourcecode and you will find the flag.  

## PoC script
```
curl http://127.0.0.1:80/c2121/b221
```

## Flag
CSC{R0b0t_D3t3ct3d!}

## Creator
Yannis Kireche 

## Creator bio
Yannis Kireche is a cybersecurity enthusiast who is currently in his final year of a Bachelor's degree in cybersecurity. As an intern at Nviso, he is working on a firmware emulation project in the IoT team. 
(bio-picture in resource)