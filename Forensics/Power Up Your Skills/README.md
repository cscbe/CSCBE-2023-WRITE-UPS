# Power up your skills 

## Category
Forensic

## Estimated difficulty
Medium 

## Description
This challenge requires a Forensic/CTF mindset and a basic understanding of Powershell. 
To succeed this challenge, you have to search for potential powershell logs (command history). 
Then, try to decode and understand what is happening on the computer. 

## Scenario
Your colleague Sandrine from the Accounting Department needs your help.

She reports that her computer has become extremely slow after downloading a "magic PC booster". She provides you a backup of her hard drive.

As a forensic investigator, can you use your skills to analyze her computer and identify the issue ?

## Write up

At the beginning, you receive an archive with a hard disk image. 

You need to analyze this image with the Autopsy software. (you have to mount it manually on your computer and use autopsy to scan your "physical drives")

Then, a hint in the title guide you to check the powershell command history. (Otherwise, it's always a good forensic mindset to check directly logs/command history).

You see that a script has been downloaded from a strange ftp server. It has been deobfuscate with a custom script before execution. Then, he has been obfuscate once again by an another custom script. 

Furthermore, you find some base64 encoded command. When you decode it (using cyberchef by example), you are in front of some powershell commands. You understand that the obfuscator has been totally removed but the deobfuscator has just been moved and renamed with an other extension to be hide but not totally removed. 
Also, you find the location of the ""malicious script"" and the location of the deobfuscator in the filesystem.

To complete the task, you need to obtain both the script and the deobfuscator. Once you have them, you must deobfuscate the script and then read it's content. Then, you discover the location of the flag.

To avoid the possibility to find the flag randomly, the flag is encoded with the obfuscator script as well. 

### Location 

Powershell history --> C:\Users\sandrinecompta\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt
script.ps1 --> C:\Windows\Tasks\scripts
Deobfuscator --> C:\Windows\Help\common_windows_file
Flag --> C:\Program Files (x86)\Internet Explorer\IEcrashlogs.txt

## Flag 
CSC{PS1s3asy2learn!}

## Creator
Yannis Kireche 

## Creator bio
Yannis Kireche is a cybersecurity enthusiast who is currently in his final year of a Bachelor's degree in cybersecurity. As an intern at Nviso, he is working on a firmware emulation project in the IoT team. 
(bio-picture in resource)