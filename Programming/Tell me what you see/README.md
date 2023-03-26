# Just Follow The Instructions

## Category
Programming

## Estimated difficulty
Easy

## Description
This challenge is a basic programming challenge related to the [look and say sequence](https://en.wikipedia.org/wiki/Look-and-say_sequence). The challenge server is a TCP socket server and will ask connected clients their favourite number and then return in words how the number would be read. This will serve as a hint of what is expected when the challenge server asks the client what they see when a specific number is shown. 
When they reply correctly to 21 questions under the time limit, the flag is returned. The answers to the 21 questions are the 21 first numbers of the look and say sequence in written language. For example: 1) 1 => one one 2) 11 => two one, 3) 21 => one two one one

Potential hints to give: 
1) Just follow the instructions
2) Just look and say

## Scenario
Really, just follow the instructions...

## Write-up
The only real info we have is that we have to follow the instructions, so let's just do that right?

When we connect to the challenge server we see that it asks for our favourite number, which is of course 42. The server says it is one four one two. It then continues by asking us to tell it what we see.

```shell
$ nc 127.0.0.1 5000
Follow the instructions and you shall receive what you came for.

Enter your favourite number: 42
Excellent choice, I say your number is one four one two.

Now look and tell me what you see here: 1

You cannot follow the instructions. You are not ready.
```

We see one "1" so given how the server replied earlier, let's reply with "one one". That brings us to another question where it asks the same for the number 11. If the specific sequence of numbers or the hints in the text were ringing a bell already, you are right: https://en.wikipedia.org/wiki/Look-and-say_sequence

```shell
$ nc 127.0.0.1 5000
Follow the instructions and you shall receive what you came for.

Enter your favourite number: 42
Excellent choice, I say your number is one four one two.

Now look and tell me what you see here: 1
one one
Tell me what you see again: 11
two one
Tell me what you see again: 21
one two one one
Tell me what you see again: 1211

You cannot follow the instructions. You are not ready.
```

Ok, so we can already imagine where this is going and we are definitely not going to be able to do this manually, so time to script this. It's a programming challenge after all right.

We first need to write a simple function that can translate a given number to how it would be read out loud.

```python
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

```

Now that we have the ability to answer the questions, we just need to send the right answers to the questions at the correct moment. We can use pwntools to connect with the challenge server and this results in the following script.

```python
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

```

When we run this, we get the following output:

```shell
$ python3 solve.py 
[+] Opening connection to 127.0.0.1 on port 5000: Done
Tell me what you see again: 11
two one
Tell me what you see again: 21
one two one one
Tell me what you see again: 1211
one one one two two one
Tell me what you see again: 111221
three one two two one one
<SNIPPED>
Tell me what you see again: 311311222113111231133211121312211231131112311211133112111312211213211312111322211231131122211311122122111312211213211312111322211213211321322113311213212322211231131122211311123113223112111311222112132113311213211221121332211211131221131211132221232112111312111213111213211231132132211211131221232112111312211213111213122112132113213221123113112221131112311311121321122112132231121113122113322113111221131221
one three two one one three two one three two two one one three three one one two one three two one two three one two three one one two one one one three one one two two two one one two one three two one one three three one one two one three two one one two three one two three two one one two three one one three one one two two two one one two one one one three one two two one one three one one one two three one one three three two two one one two one three two one one three two one three two two one one three three one two two one one two two three one one three one one two two two one one two one one one three one two two one one three one one one two three one one three three two two one one two one one one three one two two one one three one two one one one three two two two one two three two one one two one one one three one two one one one two one three three two two one one two one three two one one three two one three two two one one three three one one two one three two one one three two two one three two one one two three one one three two one three two two one one two one one one three one two two one two three two one one two one one one three one two two one two two two one one two one one two three two two two one one two three one one three one one two two two one one three one one one two three one one three three two one one one two one three one two two one one two three one one three one one one two three one one two one one one three three one one two one one one three one two two one one two one three two one one three one two one one one three two two two one one two three one one three one one two two one one one two one three one two two one one two three one one three one one two two two one one two one one one three three one one two one one one three one one two two two one one two one one one three one two two one one three one two one one one three two two two one one two one three two one one three two one three two two one one three three one one two one three two one one three three one one two one one one three one two two one two two two one one two one one one three two two one three two one one two three one one three one one two two two one two three two two two one one three three one two two two one one three one one two two one one

Good job, sometimes just following the instructions is all it takes: CSC{look_and_say_but_just_a_bit_faster_right}
[*] Closed connection to 127.0.0.1 port 5000
```

The flag is CSC{look_and_say_but_just_a_bit_faster_right}.

Sometimes following the instructions is indeed just all it takes.

## PoC script
The script that solves the challenge is located under Resources/solve.py.

## Flag
CSC{look_and_say_but_just_a_bit_faster_right}

## Creator
Jonas Van Wilder

## Creator bio
Jonas is a senior cyber security consultant & software engineer at NVISO, where he is a member of the R&D / Innovation team also known as NVISO Labs. His main focus is on managing and executing a number of key innovation projects related to services offered at NVISO. The little time left he still spends performing security assessments of mainly web applications, APIs and thick clients. Five years ago he also participated in the Cyber Security Challenge and he has been a contributor ever since.
