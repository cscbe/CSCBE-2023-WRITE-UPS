from pwn import *
import sys
from ast import literal_eval
import random, time
io = remote(sys.argv[1], int(sys.argv[2]))
intro = io.recvuntil("Choose where to throw your bamboo:")
print((intro.decode('UTF-8')))

map = []
for i in range(0, 10):
    map.append(["🟦"] * 10)

def goLeft(x, y):
    result = tryPanda(x-1, y)
    if b"Awesome" in result:
        goLeft(x-1, y)
    return b"Awesome" in result

def goRight(x, y):
    result = tryPanda(x+1, y)
    if b"Awesome" in result:
        goRight(x+1, y)
    return b"Awesome" in result

def goUp(x, y):
    result = tryPanda(x, y-1)
    if b"Awesome" in result:
        goUp(x, y-1)
    return b"Awesome" in result

def goDown(x, y):
    result = tryPanda(x, y+1)
    if b"Awesome" in result:
        goDown(x, y+1)
    return b"Awesome" in result

def cleanMap():
    global map
    for x in range(0, 10):
        for y in range(0, 10):
            char = map[x][y]
            if char == "🐼":
                putPanda(x-1, y-1, "🟥")
                putPanda(x+1, y-1, "🟥")
                putPanda(x-1, y, "🟥")
                putPanda(x+1, y, "🟥")
                putPanda(x-1, y+1, "🟥")
                putPanda(x+1, y+1, "🟥")

                putPanda(x+1, y, "🟥")
                putPanda(x-1, y, "🟥")
                putPanda(x, y+1, "🟥")
                putPanda(x, y-1, "🟥")

    for x in range(0, 10):
        line = ""
        for y in range(0, 10):
            line +=map[y][x]
        print(line)
    # for line in map:
    #     print(" ".join([str(k) for k in line]))
    
    print("")
                

def putPanda(x, y, c):
    global map
    if x < 0 or x > 9 or y < 0 or y > 9:
        return False
    if map[x][y] == "🐼":
        return False
    map[x][y] = c

def tryPanda(x, y):

    if x < 0 or x > 9 or y < 0 or y > 9:
        return b""
    if map[x][y] != "🟦":
        return b""
    print("Trying, ", x, y)
    io.send("{}{}\n".format(letters[x], y))
    intro = ""
    try:
        intro = io.recvuntil("Choose where to throw your bamboo:")
        # print(intro)
        if b"Awesome" in intro:
            putPanda(x, y, "🐼")
        elif b"flag" in intro:
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            print(intro)
        else:
            putPanda(x, y, "🟥")
        return intro
    except EOFError:
        intro = io.recvall()
        print(intro.decode("UTF-8"))
        raise SystemExit

y = "0123456789"
letters = "ABCDEFGHIJ"
while True:
    xx = random.randint(0, 9)
    yy =  random.randint(0, 9)
    while map[xx][yy] != "🟦":
        xx = random.randint(0, 9)
        yy =  random.randint(0, 9)
    result = tryPanda(xx, yy)
    # print((result.decode('UTF-8')))
    if b"Awesome" in result:
        
        # print((result.decode('UTF-8')))
    
        left = goLeft(xx, yy)
        right = goRight(xx, yy)

        if not left and not right:
            goUp(xx, yy)
            goDown(xx, yy)
        cleanMap()
    elif b"flag" in result:
        print((result.decode('UTF-8')))
        print("DONE")
        break
    cleanMap()
    time.sleep(0.1)


