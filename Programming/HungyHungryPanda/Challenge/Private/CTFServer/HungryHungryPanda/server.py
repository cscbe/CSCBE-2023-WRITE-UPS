#!/usr/bin/env python3
import argparse
import sys
import socket, time
from threading import Thread
from time import sleep
import netifaces as ni


from df_maze import Maze
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



def createGlobalMaze(subMazes):
    globalMaze = Maze(20, 20, 0, 0)
    for subMaze in subMazes:
        for x in range(0, 5):
            for y in range(0, 5):
                transporter = subMaze["maze"].maze_map[x][y].get_transporter()
                if transporter == "x":
                    transporter = " "
                targetCell = subMaze["maze"].maze_map[x][y]
                targetCell.set_transporter(transporter)
                globalMaze.maze_map[x + subMaze["x"]][subMaze["y"]+ y] = targetCell
    return globalMaze

def getMaze():
    subMazes = []
    for i in range(0,4):
        for j in range(0, 4):
            maze = Maze(5, 5, floor(random.random() * 5), floor(random.random() * 5))
            maze.make_maze()
            subMazes.append({   "x": i * 5,
                                "y": j * 5,
                                "maze": maze
                            })
    for letter in string.ascii_lowercase:

        fromMaze = subMazes[floor(random.random() * len(subMazes))]
        while not fromMaze["maze"].has_open_transporters():
            fromMaze = subMazes[floor(random.random() * len(subMazes))]

        toMaze = subMazes[floor(random.random() * len(subMazes))]
        while toMaze == fromMaze or not toMaze["maze"].has_open_transporters():

            toMaze = subMazes[floor(random.random() * len(subMazes))]
        fromMaze["maze"].configureTransporter(letter)
        toMaze["maze"].configureTransporter(letter)

    startMaze = subMazes[floor(random.random() * len(subMazes))]
    while not startMaze["maze"].has_active_transporters():
        startMaze = subMazes[floor(random.random() * len(subMazes))]


    last_transport = "S" 
    path = last_transport
    currentSubMaze = startMaze["maze"]
    for i in range(0, 6):
        try:
            next_transport = currentSubMaze.get_next_transport(last_transport, path).get_transporter()
            for m in subMazes:
                if m["maze"].has_transporter(next_transport) and m["maze"] != currentSubMaze:
                    nextSubMaze = m
                    break

            path += next_transport
            last_transport = next_transport
            currentSubMaze = nextSubMaze["maze"]
        except:
            break
    
    while True:
        x = floor(random.random()* 5)
        y = floor(random.random()*5)
        if currentSubMaze.maze_map[x][y].get_transporter() == "":
            currentSubMaze.maze_map[x][y].set_transporter("F")
            break

    while True:
        startX = floor(random.random() * 5)
        startY = floor(random.random() * 5)
        if startMaze["maze"].maze_map[startX][startY].get_transporter() == "":
            startMaze["maze"].maze_map[startX][startY].set_transporter("S")
            break

    return createGlobalMaze(subMazes), path, [startMaze["x"] + startX, startMaze["y"] + startY]

def buildPath(globalMaze, startPos, steps):
    curX = startPos[0]
    curY = startPos[1]
    for step in steps:
        if step == "U":
            if curY == 0 or globalMaze.maze_map[curX][curY].haswall("N"):
                return False, True
            curY -= 1
        elif step == "D":
            if curY == 19 or globalMaze.maze_map[curX][curY].haswall("S"):
                return False, True
            curY += 1
        elif step == "L":
            if curX == 0 or globalMaze.maze_map[curX][curY].haswall("W"):
                return False, True
            curX -= 1
        elif step == "R":
            if curX == 19 or globalMaze.maze_map[curX][curY].haswall("E"):
                return False, True
            curX += 1

        currentTransporter = globalMaze.maze_map[curX][curY].get_transporter()
        if currentTransporter == "F":
            return True, False
        if currentTransporter in string.ascii_lowercase and not currentTransporter == "":
            (curX, curY) = globalMaze.get_transport_target(curX, curY)

        else:
            if currentTransporter != "S":
                globalMaze.maze_map[curX][curY].set_transporter(".")

    return False, False
prolog = """
 ___________  _______  ___       _______  ___      ___       __     ________    _______  
("     _   ")/"     "||"  |     /"     "||"  \    /"  |     /""\   ("      "\  /"     "| 
 )__/  \\__/(: ______)||  |    (: ______) \   \  //   |    /    \   \___/   :)(: ______) 
    \\_ /    \/    |  |:  |     \/    |   /\\  \/.    |   /' /\  \    /  ___/  \/    |   
    |.  |    // ___)_  \  |___  // ___)_ |: \.        |  //  __'  \  //  \__   // ___)_  
    \:  |   (:      "|( \_|:  \(:      "||.  \    /:  | /   /  \\  \(:   / "\ (:      "| 
     \__|    \_______) \_______)\_______)|___|\__/|___|(___/    \___)\_______) \_______) 
                                                                                         

Welcome to Telemaze! You have 5 seconds to escape.
S - START
F - FINISH
a-z - transporters

Movement options: D(own) / U(p) / L(eft) / R(ight)
Example solution: DULRRUULDDRUDLRU

Please escape from:

"""
flag = "You got out in time! CSC{Next_Time_I_Eat_My_Way_Out}"

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

        globalMaze, path, startPos = getMaze() 
       
        while len(path) < 5:
            globalMaze, path, startPos = getMaze() 
        self.client_socket.sendall(bytes(str(prolog), "utf-8"))
        self.client_socket.sendall(bytes(str(globalMaze), "utf-8"))
        while True:
            try:
                starttime = time.time()
                self.client_socket.sendall(bytes("\n> ", "utf-8"))
                steps = self.client_socket.recv(1024).decode().strip()
                endtime = time.time()
                totaltime = floor((endtime - starttime) * 100)/100
                gotflag, hitwall = buildPath(globalMaze,startPos, steps)
                self.client_socket.sendall(bytes("You took {}s\n".format(totaltime), "utf-8"))
                if gotflag:
                    self.client_socket.sendall(bytes(flag, "utf-8"))
                else:
                    if hitwall:
                        self.client_socket.sendall(bytes("Looks like you hit a wall:\n", "utf-8"))
                    else:
                        self.client_socket.sendall(bytes("That's not correct... Your path can be found below:\n", "utf-8"))
                    self.client_socket.sendall(bytes(str(globalMaze), "utf-8"))

                self.closeConn()
                return

                if answer == str(CTFDict.SOLUTION_1):
                    self.client_socket.sendall(CTFDict.WON.encode())
                    self.closeConn()
                    return
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
