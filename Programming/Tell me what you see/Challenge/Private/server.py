import traceback
import time
import random
import os
import socketserver
import socket

from itertools import groupby, islice
from threading import Thread
from functools import lru_cache


if "FLAG" not in os.environ:
    raise ValueError("Please set the flag by using the environment variable FLAG")
    
flag = os.environ["FLAG"]

numbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

total_questions = 21

def get_look_and_say(number='1'):
	while True:
		yield number
		number = ''.join(str(len(list(g))) + k for k, g in groupby(number))

sequence = [_ for _ in islice(get_look_and_say(), total_questions)]

@lru_cache(maxsize = 10000)
def get_as_text(number_sequence):
    res = []
    n = len(number_sequence)
    prev_number = number_sequence[0] # 1
    i = 1
    j = 1
    while i < n:
        number = number_sequence[i]
        if number == prev_number:
            j += 1
        else:
            # append counter number
            res.append(numbers[j])
            # append value number
            res.append(numbers[int(prev_number)])
            j = 1
        i+=1
        prev_number = number     
    
    # append counter number
    res.append(numbers[j])
    # append value number
    res.append(numbers[int(prev_number)])
        
    res = ' '.join(res)
    
    return res
    

def test_get_as_text():
    assert get_as_text("0") == "one zero"
    assert get_as_text("1") == "one one"
    assert get_as_text("2") == "one two"
    assert get_as_text("9") == "one nine"
    assert get_as_text("10") == "one one one zero"
    assert get_as_text("12") == "one one one two"
    assert get_as_text("21") == "one two one one"
    assert get_as_text("22") == "two two"
    assert get_as_text("99") == "two nine"
    assert get_as_text("123") == "one one one two one three"
    assert get_as_text("121") == "one one one two one one"
    assert get_as_text("112") == "two one one two"
    assert get_as_text("140") == "one one one four one zero"
    assert get_as_text("211") == "one two two one"
    assert get_as_text("22221") == "four two one one"
    assert get_as_text("1100") == "two one two zero"
    assert get_as_text("93") == "one nine one three"
    assert get_as_text("11111111") == "eight one"
    assert get_as_text("1321132132211331121321231231121113112221121321132122311211131122211211131221131211132221121321132132212321121113121112133221123113112221131112311332111213122112311311123112111331121113122112132113213211121332212311322113212221") == "one one one three one two two one one three one two one one one three two two two one two three two one one two one one one three one two one one one two one three one one one two one three two one one two three one one three two one three two two one one two one one one three one two two one one three one two one one two two one three two one one two three one one three two one three two two one one two three one one three one one two two two one one three one one one two three one one three three two two one one two one one one three one two two one one three one two one one one three two two one one one two one three one two two one one two three one one three one one one two three one one two one one two three two two two one one two one three two one one three two one three two two one one three three one one two one three two one two three one two three one one two one one one three one one two two two one one two one three two one one three three one one two one three two one one two three one two three two one one two three one one three one one two two two one one two one one one three one two two one one three one two one one one three one two three one one two one one two three two two one one one two one three two one one three two two two one one three one two one one three two one one"


class ConnectionHandler(socketserver.StreamRequestHandler):

    def handle(self):
        print(f"Accepted connection from client {self.client_address[0]}:{self.client_address[1]}")

        client_socket = self.request
        try:
            client_socket.settimeout(3)
            self.wfile.write(b"Follow the instructions and you shall receive what you came for.\r\n\r\nEnter your favourite number: ")
            
            chosen_number = self.rfile.readline().decode().strip()
            
            try:
                if int(chosen_number) > 1_000_000:
                    raise ValueError
            except ValueError as e:
                self.wfile.write(f"That's a weird favourite number. I don't like where this is going.\r\n".encode())
                raise e
                
            security = random.randrange(1, 1000)
            if security == 42:
                self.wfile.write(b"\r\nOur security monitoring system has detected an anomaly. Connection will be terminated.")
                raise ValueError
             
            chosen_number_text = get_as_text(chosen_number)
            self.wfile.write(f"{'Excellent' if chosen_number == '42' else 'Good'} choice, I say your number is {chosen_number_text}.\r\n\r\nNow look and tell me what you see here: 1\r\n".encode())
            
            i = 1
            n = 1
            while i < total_questions:
                res = self.rfile.readline().decode().strip()
                
                if res != get_as_text(str(n)):
                    self.wfile.write(f"\r\nToo hard? Try again when you are ready.\r\n".encode())
                    break
                else:
                    i += 1
                    n = sequence[i-1]
                    self.wfile.write(f"Tell me what you see again: {n}\r\n".encode()) 
            
            if i == total_questions:
                self.wfile.write(f"\r\nGood job, sometimes just following the instructions is all it takes: {flag}\r\n".encode())
        
        except ValueError as e:
            pass
        except socket.timeout as e:
            self.wfile.write(f"\r\nYou cannot follow the instructions. You are not ready.\r\n".encode())
        except Exception as e:
            m = random.randrange(1, 10)
            raise e
            self.wfile.write(f"\r\nYou are not ready. Please come back in {m} minutes.\r\n".encode()) 


def main():
    # Uncomment to run tests
    # test_get_as_text()

    host = '0.0.0.0'
    port = 5000
    
    with socketserver.ThreadingTCPServer((host, port), ConnectionHandler) as server:
        print('Challenge server started!')
        print('Waiting for clients...')
        server.serve_forever()


if __name__ == '__main__':
    main()
