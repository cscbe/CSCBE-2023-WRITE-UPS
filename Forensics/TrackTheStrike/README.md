# TrackTheStrike

## Category
Forensic

## Estimated difficulty
Easy

## Description
You'll have to quickly pass the pcapng into tshark -T Fields -e usb.capdata and pipes with grep & stdout to a file. 
After that a simple python script will decrypt the data. 
Careful that I type in Azerty keyboard and most of the keycode scripts maps qwerty.

## Scenario
We just find this sniffing communication file from a investigation. Could you extract the secret inside ?

## Write-up
https://gist.githubusercontent.com/inesmartins/662442da446c3f79e19bca9bd82ea7d1/raw/cd7c2ae10a362d39759862dc42ee0e77af740d7c/usb-keyboard-pcap-parser.py

## PoC script
No need here.

## Flag
CSC{K3yB04rdFl4gW4sH3r3}

## Creator
Vincent Castanié

## Creator bio
Student in Bachelor@EPFC I making my final internship at NVISO / IoT section on a USB MiTM subject.