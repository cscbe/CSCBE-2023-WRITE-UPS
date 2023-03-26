#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Script copied from https://medium.com/swlh/this-is-how-to-create-a-simple-minesweeper-game-in-python-af02077a8de
# And then butchered for the CTF
# Though for some reason this thing doesn't even have a flood fill, so adding it myself
# And I added the pandas too
from http import client
import random
from signal import signal, SIGINT
from sys import exit
import time

import argparse
import sys
import socket, time
from threading import Thread
from time import sleep
import netifaces as ni

from math import floor
import random
import string

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# --- Import needed data libraries ---
import csv, time
from random import randint, random

intro = """
 _    _                                _    _                                _____                _
| |  | |                              | |  | |                              |  __ \              | |
| |__| |_   _ _ __   __ _ _ __ _   _  | |__| |_   _ _ __   __ _ _ __ _   _  | |__) |_ _ _ __   __| | __ _
|  __  | | | | '_ \ / _` | '__| | | | |  __  | | | | '_ \ / _` | '__| | | | |  ___/ _` | '_ \ / _` |/ _` |
| |  | | |_| | | | | (_| | |  | |_| | | |  | | |_| | | | | (_| | |  | |_| | | |  | (_| | | | | (_| | (_| |
|_|  |_|\__,_|_| |_|\__, |_|   \__, | |_|  |_|\__,_|_| |_|\__, |_|   \__, | |_|   \__,_|_| |_|\__,_|\__,_|
                    __/ |      __/ |                      __/ |      __/ |
                    |___/      |___/                      |___/      |___/

Welcome to our habitat for Pandas! As the new caregiver, it is your job to feed all the pandas by throwing them some bamboo from our helicopter.

Our panda population exists of:
- The PandaLicious group: A group of {} pandas that enjoys a bit of butter on their bamboo
- The OppaPandaStyle group: These {} dancers are always shaking their paws. Woop Woop!
- The Black&White group: These {} pandas joined up when they all found out they are color blind.
- Bob: Bob normally hangs with the OppaPandaStyle group, but lost them a few weeks ago. Please feed Bob!

It's difficult to see the pandas from your helicopter, so you'll have to guess a bit. Luckily, pandas of the same group do tend to walk in straight lines, so as soon as you found one you're good to go!

Our helicopter can only stay in the air for {} seconds, and our helicopter can only carry {} bamboo shoots, so hurry up and aim well!

"""


# --- Function definition for generateStartMap ---
# Will take in the size of the map to be made and produce an empty starting map for the game.
def generateStartMap(size):
    startingMap = []
    for counter in range(size):
        currentLine = []
        for counter in range(size):
            currentLine.append("🌳")
        startingMap.append(currentLine)

    return startingMap

# --- Function definition for shotToNumbers ---
# Will take in a string of a letter and number and return a list of two numbers.
def shotToNumbers(coordinateString, headingsList):
    shotList = []
    shotList.append(int(coordinateString[1]))

    for column in headingsList:
        if coordinateString[0] == column:
            shotList.append(headingsList.index(column))

    return shotList

# --- Function definition for checkHit ---
# Will take in shotCoordinateList and shipMap and return whether the shot hit or missed.
def checkHit(shot, map):
    if map[shot[0]][shot[1]] == None:
        return ""
    else:
        return map[shot[0]][shot[1]]

def isFreeCell(map, x, y):
    # left and right
    if map[x][y] == None and map[max(x-1, x)][y] == None and map[min(x+1, 9)][y] == None:
        # up and down
        if map[x][max(y-1, 0)] == None and map[x][min(y+1, 9)] == None:
            # up left and up right
            if map[max(x-1, 0)][max(y-1, 0)] == None and map[min(x+1, 9)][max(y-1, 0)] == None:
                # down left and down right
                if map[max(x-1, 0)][min(y+1, 9)] == None and map[min(x+1, 9)][min(y+1, 9)] == None:
                    return True
    return False


def canPlace(map, x, y, groupSize, xx, yy):
    for i in range(0, groupSize):
        if not isFreeCell(map, x, y):
            return False
        x += xx
        y += yy
    return True

def placePanda(map, x, y, size, xx, yy, key, currentMap):
    for a in range(0, size):
        # currentMap[x][y] = "🐼"
        map[x][y] = key
        x += xx
        y += yy
def addPandas(map, shipSymbols, pandaNames, currentMap):
    for k in shipSymbols:
        groupSize = len(pandaNames[k])

        c = 0
        while True:
            c += 1
            if c > 10000:
                return False
            xx = randint(0, 1)
            yy = 1 - xx

            x = randint(0, 9 - xx * groupSize)
            y = randint(0, 9 - yy * groupSize)

            if canPlace(map, x, y, groupSize, xx, yy):
                placePanda(map, x, y, groupSize, xx, yy, k, currentMap)
                # printMap()
                break
    return True


# --- Function definition for updateMap ---
# Takes in the current map and the last shot results and returns an updated map.
def updateMap(lastShotCell, lastShotResult, map):
    map[lastShotCell[0]][lastShotCell[1]] = lastShotResult
    return map

# --- Function definition for checkShipStatus ---
# Will check the ship layout to check which ships have been sunk.
def checkShipStatus(shipList, shipMap):
    shipStatus = []
    for index in range(len(shipList)):
        shipStatus.append(False)
    for index in range(len(shipList)):
        for list in shipMap:
            if shipList[index] in list:
                shipStatus[index] = True
    return shipStatus
def printMap(client_socket, currentMap, gridSize, validColumns):
    output(client_socket,"\n")
    output(client_socket,"  " + "  ".join(validColumns) + "\n")
    for counter in range(gridSize):
        output(client_socket,str(counter) + " " + " ".join(currentMap[counter]) + "\n")

    output(client_socket,"\n")
# --- Game variables ---

flag = """

                               .                             :-====-:
                           -+*++++++:    :-=============-::+**+=--=++*+.
                         :#++*+=+***#*=+=:.             .#%##########*+*-
                         #+##*=-=*##*-.                 -%##*-...:+####+%
                        .%##*    =+.                    +##*       ####*%.
                         *###- .#-                      -%##.     :######
                          =#####.                        =%##+-::=######.
                            -*#.                          :*##########%.
                            .#+=-.              ....        .-++***+-.:*:
                            *#####+          -*######*-                 +=
                           *#######.        +###########:                +=
             -           -*##=-+##=         =####+---*###:                *:
            +*.        =#######*:             -*#+*#######                :*
        +=.=++: :-.  .#+######+   =---++=       +#########.                #.
        -+++=+*+++   == .-=+=-    -*##%#+.     :.=#######=                .*:
         =+=====*.   *:       :.    ::.       :%+..-===-.                 :#:
       .  :++++=.    +-       :#-.:=*+-.....:=#+=*=                       -%=
     :+++-. .*       -*         =+%%%%%#****#+=++=++.                    :*%*
     -+++====+        #-          *%###*====*=+*+===*                   :+%##
      .*+*+==*+=-:.   .#:.        .*##**+=*+===*-=++*:                 :*%###
     :#++*#****==+#*+=-*#-.         .-=+**-++==*:..:                 .-#####%:
     #*#######**+===++####+:.          :-:..-+**:                  .-*%#######.
    .%####****##**++*+**####=::.        ..   .::.              ..:=*###########.
     ######**=+*##****+==+*###+-:::...                    ..:-=+*###############.
     -%##*****######*:+*+=-=+*###*+-:::::::::::::::::::-==+**+++*##############%#.
      =%############.  .-+*+=++**#####*++==--:::-=++***++==+*##################%#*
       .*#########%+:::.. :=***+-=+*#######%%#*++====++*#######################%:==
         :+#######%::+*++++-.-+*+=--=+####*+=++**#############################%+ .#.
         ...:=*##%*-:-+*===+*--:-+*+=-+#**###################################%+:::=*
      -*#####*+: ****+++===*:     .-**%####################################%%##*-::#.
     ##+-::-+####%=::.=*++=.         #%################################%%########*=+=
    +#-      .+##%=::-*=:            +%########################%%#*++*#%###########*+
    #+         =#%+:::.               +%################%%#%%*-.       :*%##########*
   .%-          +##::::.               :+#%######%##*++=-:*#=            -#%########+
    %=          .#%=:::::.                 .::::.   .::::+%=              =#########+
    *#:.         *##-::::::.                      .::::::##.               #%######%-
    -%+:::...    *###=::::::::.                 .::::::::%#:.              #%#######
     +#+::::::::-####%+:::::::::::..       ...:::::::::::#%-:::..         .#%######.
      +%*-:::::-*#######+-:::::::::::::::::::::::::::::::-%*-:::::::::::::*%#####+
       :*##*++*############*+=-:::::::::::::::::::::::::::=%#=::::::::::-*%####*:
         .-+****************####***++++++++++++++++++++++++*%%#+-::::-=*%%###=:
                                                             .-+#######*+=:.

                    csc{1_l1k3_b1g_p4nd4s_4nd_1_c4nn0t_l13!}"""
# --- Welcome message and UX code ---


# ----------- Starting the Game. Code will need to loop until the user quits. -----------
def Game(client_socket):
    gridSize = 10
    validRows = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    validColumns = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    shipSymbols = ["P", "O", "W", "B"]
    shipNames = ["PandaLicious", "OppaPandaStyle", "Black&White", "Bob"]
    helicopterSeconds = 30
    startTime = time.time()
    playing = True
    currentMap = []
    pandasFed = 0
    bambooShoots = 50
    pandaNames = {
        "P": ["Bao Bao", "Bei Bei", "Da Mao", "Er Shun", "Gao Gao", "Lin Bing"],
        "O" : ["He Hua", "Lun Lun", "Mei Lan", "Rou Rou"],
        "W" : ["Po", "Yun Zi", "Zhen Zhen", "Yang Guang", "Yang Yang" ],
        "B" : ["Bob"]
    }
    output(client_socket, intro.format(len(pandaNames["P"]), len(pandaNames["O"]), len(pandaNames["W"]) , helicopterSeconds,bambooShoots))
    totalPandas = len(pandaNames["P"]) + len(pandaNames["O"]) + len(pandaNames["W"]) + len(pandaNames["B"])

    GameStatus = True
 

    shipMap = []
    # --- Variables to be set before each round ---
    currentMap = generateStartMap(gridSize)
    previousShots = []

    while True:
        shipMap = []
        for i in range(0, 10):
            shipMap.append([None] * 10)

        if addPandas(shipMap, shipSymbols, pandaNames, currentMap):
            break

    firstRun = True
    while GameStatus:
         
        while True:

            try:
                if not firstRun:
                    output(client_socket, "\033c")
                    firstRun = True
                printMap(client_socket, currentMap, gridSize, validColumns)

                output(client_socket, "---------------------------\n"
                    "BAMBOO REMAINING: {} \n".format(str(bambooShoots)))

                # --- Get location input from the user for their shot ---
                while True:
                    output(client_socket, "Choose where to throw your bamboo: ")
                    userShot = client_socket.recv(1024).decode().strip().upper()
                    if len(userShot) != 2:
                        output(client_socket,"Please enter a valid coordinate:")
                    elif userShot in previousShots:
                        output(client_socket,"That spot already has bamboo!\n")
                    elif userShot[0] not in validColumns or userShot[1] not in validRows:
                        output(client_socket,"That's a weird number\n")
                    else:
                        previousShots.append(userShot)
                        shotCoordinateList = shotToNumbers(userShot, validColumns)
                        break

                output(client_socket, "---------------------------\n")

            
                    

                # --- Check the shot vs. shipMap to verify a hit or miss ---
                shotResult = checkHit(shotCoordinateList, shipMap)
                # output(client_socket,shotResult)

                if shotResult:
                    pandasFed += 1
                    if shotResult == 'B':
                        output(client_socket,"Awesome! You fed Bob\n")
                    else:
                        pandaName = pandaNames[shotResult].pop()
                        output(client_socket,"Awesome! You fed {} from the {} crew\n".format(pandaName, shipNames[shipSymbols.index(shotResult)]))

                    # output(client_socket,pandasFed, totalPandas)
                    if pandasFed == totalPandas:
                        output(client_socket,"You found all of them!\n")
                        output(client_socket,"Here's the flag: {}\n".format(flag))
                        GameStatus = False
                        break
                else:
                    output(client_socket,"Why are you wasting bamboo? :(\n")

                if time.time() - startTime > helicopterSeconds:
                    output(client_socket,"Unfortunatelly, we ran out of fuel, so we'll have to head back. Better luck next time!\n")
                    GameStatus = False
                    break

                currentMap = updateMap(shotCoordinateList, "🐼" if shotResult else "🎍", currentMap)

                bambooShoots -= 1
                if bambooShoots == 0:
                    output(client_socket, "Oh no, we ran out of bamboo shoots and not all pandas are fed yet :(. Better luck next time!\n")
                    GameStatus = False
                    break

            except BrokenPipeError:
                client_socket.close()
                return
    client_socket.close()


def output(client_socket, s):
    client_socket
    client_socket.sendall(bytes(s, "utf-8"))

class ClientThread(Thread):
    def __init__(self, client_socket, ip, port):
        """[summary]

        Args:
            client_socket ([socket]): [holds the client socket]
        """
        Thread.__init__(self)
        self.client_socket = client_socket
        self.client_ip = ip
        self.client_port = port

    def run(self):
            try:
                Game(self.client_socket)
            except BrokenPipeError:
                self.closeConn()
                return

    def closeConn(self):
        self.client_socket.close()
        print(f"{Colors.FAIL}[-] Client {self.client_ip}:{self.client_port} disconnected {Colors.ENDC}")


class Server():
    def __init__(self, address, port):
        """[summary]

        Args:
            address ([str]): [server's ip]
            port ([int]): [server's port]
        """
        self.initConn(address, port)

    @classmethod
    def initConn(self, address, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_socket.bind((address, port))
            server_socket.listen(5)
        except Exception:
            print("Could not bind address to port, use a different port or try again later")
            sys.exit()
        if args.verbose:
            print(f"{Colors.BOLD}Listening on {address} {port} ...{Colors.ENDC}")
        while True:
            try:
                (client_socket, (ip, port)) = server_socket.accept()
                print(f"{Colors.OKGREEN}[+] Connection established from {ip} at port {port} {Colors.ENDC}")
                client_thread = ClientThread(client_socket, ip, port)
                client_thread.daemon = True
                client_thread.start()
            except KeyboardInterrupt:
                print(f"\n{Colors.WARNING}We are shutting down the server {Colors.ENDC}")
                sleep(1)
                break
            except Exception as e:
                print(f"{Colors.FAIL}Error occured {e} {Colors.ENDC}")
                break


def verifyInter(ip):
    interfaces = ni.interfaces()
    for i in interfaces:
        # Checking if there's an ip assigned to the interface
        if len(ni.ifaddresses(i)) > 1:
            if ip == ni.ifaddresses(i)[2][0]['addr']:
                return True
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Server settings args
    parser.add_argument('-p', '--port', metavar='', type=int, help='specify server\'s port', default=2802)
    parser.add_argument('-a', '--address', metavar='', type=str, help='specify server\'s address', default="0.0.0.0")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-q', '--quit', action='store_true', help='quiet mode - default')
    group.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
    args = parser.parse_args()
    AllowedAddre = ['localhost', '0.0.0.0']
    if(verifyInter(args.address) or (args.address in AllowedAddre)):
        try:
            server = Server(args.address, args.port)
            sys.exit()
        except KeyboardInterrupt:
            sys.exit()
    print(f"{Colors.FAIL}Error occured. Try using a valid address or check network interfaces. {Colors.ENDC}")
