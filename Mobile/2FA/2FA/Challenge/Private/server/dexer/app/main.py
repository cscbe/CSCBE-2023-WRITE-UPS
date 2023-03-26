import base64
import subprocess
import json
import time, os
import logging
import hashlib
import random
from fastapi import FastAPI, HTTPException, Body, Request
from cryptography.fernet import Fernet
import redis

app = FastAPI()
redis_pool = redis.ConnectionPool(host='redis', port=6379, db=0)


logger = logging.getLogger("gunicorn.error")
logger.setLevel(logging.DEBUG)
KEY = "x3UbhzTEKZHmtjSfgSsmymigjKKXwppkEWan9i2JG7M="
flag = "csc(The_2FA_codes_mason_what_do_they_mean)"

def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)

def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)

class_template = """

package be.dauntless.twofa;

import java.security.MessageDigest;

public class Vault{{

    // 243d16af5d636a9a5c2ce5c2c5531b8d7777779a9c965708ef7b4ca380c75a60c063a2de287e29a4a38788ba96136d6c2f21d0
    String a = "{}";
    String c = "{}";
    String b = "{}";

    public String d = "{}";

    public String dd(){{
        return this.d;
    }}
   
    public boolean a(String b, String c) throws Exception
    {{
        return this.a(a + b + this.c + c).equals(this.b);
    }}

    private String a(String b) throws Exception
    {{
        //Log.d("xxx" ,b);
        MessageDigest md = MessageDigest.getInstance("SHA-512");
        byte[] digest = md.digest(b.getBytes());
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < digest.length; i++) {{
            sb.append(Integer.toString((digest[i] & 0xff) + 0x100, 16).substring(1));
        }}
        //Log.d("xxx", sb.toString());
        return sb.toString();
    }}
}}

"""

def Sha512Hash(pwd):
    return  hashlib.sha512(pwd.encode('utf-8')).hexdigest()



@app.post('/submitkey')
async def submit_key(request : Request):
    r = redis.Redis(connection_pool=redis_pool)
    try:
        data = await request.json()

        logger.error("solution pin: " + data["pin"])

        vault = data["vault"]
        logger.error(vault)

        decryptedVault = decrypt(vault, KEY)
        logger.error(decryptedVault)

        vaultData = json.loads(decryptedVault)

        if r.get(vaultData["id"]):
            return {"response": encrypt_for_delivery("This vault was destroyed. Access is forever lost.")}

        if round(time.time()) - vaultData["time"] <= 30:
            if vaultData["pin"] == data["pin"]:
                r.set(vaultData["id"], 1)
                return  {"response": encrypt_for_delivery(flag)}
            else:
                r.set(vaultData["id"], 1)
                return  {"response": encrypt_for_delivery("Wrong PIN. Vault is destroyed.")}
        else:
            r.set(vaultData["id"], 1)
            return  {"response": encrypt_for_delivery("Expired vault. Vault is now destroyed.")}
    except:
        return  {"response": encrypt_for_delivery("Invalid vault")}

@app.get('/getvault')
async def get_vault():

    a = hashlib.md5(os.urandom(32)).hexdigest()
    c = hashlib.md5(os.urandom(32)).hexdigest()
    hardcoded = "de287e29a4a38788ba96136d6c2f21d0"
    
    pin = str(random.randint(100000, 999999))
    sol = Sha512Hash(a + pin + c + hardcoded)

    
    confirmation = {
        "time": round(time.time()),
        "pin": pin,
        "id": hashlib.md5(os.urandom(32)).hexdigest()
    }

    encryptedConfirmation = encrypt(json.dumps(confirmation).encode(), KEY)
    thecode = class_template.format(a, c, sol, encryptedConfirmation.decode("utf-8"))

    source_code_encoded = base64.b64encode(thecode.encode('utf-8')).decode('utf-8')

    # Compile Java source code to Android dex file
    result = subprocess.run(['/compile.sh', source_code_encoded], capture_output=True)
    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=result.stderr.decode('utf-8'))
    #logger.error(result.stdout)
    return {"vault": encrypt_for_delivery(result.stdout.decode('utf-8'))}

@app.get('/validate')
async def validate(code: str):

   
    return Sha512Hash("243d16af5d636a9a5c2ce5c2c5531b8d7777779a9c965708ef7b4ca380c75a60c063a2de287e29a4a38788ba96136d6c2f21d0")
    return decrypt(code.encode(), KEY)







from Crypto.Cipher import AES


# AES 'pad' byte array to multiple of BLOCK_SIZE bytes
def pad(byte_array):
    BLOCK_SIZE = 16
    pad_len = BLOCK_SIZE - len(byte_array) % BLOCK_SIZE
    return byte_array + (bytes([pad_len]) * pad_len)

# Remove padding at end of byte array
def unpad(byte_array):
    last_byte = byte_array[-1]
    return byte_array[0:-last_byte]

def encrypt_for_delivery(message):
    key = "ca1111c9f4a927971077eb12cf0a4fcb"[0:16]
    """
    Input String, return base64 encoded encrypted String
    """

    byte_array = message.encode("UTF-8")

    padded = pad(byte_array)

    # generate a random iv and prepend that to the encrypted result.
    # The recipient then needs to unpack the iv and use it.
    iv = os.urandom(AES.block_size)
    cipher = AES.new( key.encode("UTF-8"), AES.MODE_CBC, iv )
    encrypted = cipher.encrypt(padded)
    # Note we PREPEND the unencrypted iv to the encrypted message
    return base64.b64encode(iv+encrypted).decode("UTF-8")

def decrypt_for_delivery_not_used(message):
    key = "ca1111c9f4a927971077eb12cf0a4fcb"[0:16]
    """
    Input encrypted bytes, return decrypted bytes, using iv and key
    """

    byte_array = base64.b64decode(message)

    iv = byte_array[0:16] # extract the 16-byte initialization vector

    messagebytes = byte_array[16:] # encrypted message is the bit after the iv

    cipher = AES.new(key.encode("UTF-8"), AES.MODE_CBC, iv )

    decrypted_padded = cipher.decrypt(messagebytes)

    decrypted = unpad(decrypted_padded)

    return decrypted.decode("UTF-8");
