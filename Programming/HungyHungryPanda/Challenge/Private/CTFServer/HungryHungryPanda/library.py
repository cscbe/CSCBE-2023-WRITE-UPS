import time
import sys
import os
from pyfiglet import Figlet


AllowedAddre = ['localhost', '0.0.0.0']


def loadAnimation():
    # String to be displayed when the application is loading
    load_str = "starting your server..."
    ls_len = len(load_str)
    # String for creating the rotating line
    animation = "|/-\\"
    anicount = 0
    # used to keep the track of the duration of animation
    counttime = 0
    # pointer for travelling the loading string
    i = 0
    while (counttime != 70):
        # used to change the animation speed smaller the value, faster will be the animation
        time.sleep(0.075)
        # converting the string to list as string is immutable
        load_str_list = list(load_str)
        # x->obtaining the ASCII code
        x = ord(load_str_list[i])
        # y->for storing altered ASCII code
        y = 0
        # if the character is "." or " ", keep it unaltered switch uppercase to lowercase and vice-versa
        if x != 32 and x != 46:
            if x > 90:
                y = x-32
            else:
                y = x + 32
            load_str_list[i] = chr(y)
        # for storing the resultant string
        res = ''
        for j in range(ls_len):
            res = res + load_str_list[j]
        # displaying the resultant string
        sys.stdout.write("\r"+res + animation[anicount])
        sys.stdout.flush()
        # Assigning loading string  to the resultant string
        load_str = res
        anicount = (anicount + 1) % 4
        i = (i + 1) % ls_len
        counttime = counttime + 1
    os.system("/usr/bin/clear")


# Dict for all needed messages, challenges, flags etc..
class CTFDict:
    WELCOME = "Welcome to our server!"
    FLAG = "FLAG{YOU_WIN}"
    LOST = "LOST"
    WON = "Well I guess you win! " + FLAG + "\n"
    CHALLENGE_1 = "Solve it and secure the flag! YmFzZTY0Cg==\n"
    CHALLENGE_2 = "This is so BASic <GuGDBju-XFDY&f9k$\"qD,4V0@khI_D.-st7WEEdEc\#PdF>7Mu2)@QmCGf+63DhM0G&^/869/H\n"
    SOLUTION_1 = "base64"
    HELP = "Quit to leave"


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# ASCII ART
figlet = Figlet()
ASCII_ART = figlet.renderText("CTF Server")
