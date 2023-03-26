from pwn import *

numbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

def say_what_you_see(number_sequence):
    res = []
    n = len(number_sequence)
    prev_number = number_sequence[0]
    i = 1
    j = 1
    while i < n:
        number = number_sequence[i]
        if number == prev_number:
            j += 1
        else:
            res.append(numbers[j])
            res.append(numbers[int(prev_number)])
            j = 1
        i += 1
        prev_number = number    

    res.append(numbers[j])
    res.append(numbers[int(prev_number)])
     
    return " ".join(res)

r = remote("127.0.0.1", 5000)
r.send(b"42\n") # obviously
r.recvline_contains(b"Now look and tell me")
r.send(b"one one\n")
while True:
    line = r.recvline().decode().strip()
    print(line)
    if not line:
        continue
    if not line.startswith("Tell me what you see"):
        break
    s = line.split(":")[1].strip()
    answer = say_what_you_see(s)
    print(answer)
    r.send(f"{answer}\n".encode())
