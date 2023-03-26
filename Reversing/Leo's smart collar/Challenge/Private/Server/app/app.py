from fastapi import FastAPI
import os
import pyotp


totp = pyotp.TOTP("TNVZCHWFIKYG553JHZQ5Y2ARPIWDV6NP")


flag = os.getenv("FLAG", "CSC{ISSUE WITH THE CHALLENGE CALL AN ADMIN!}")

app = FastAPI()


@app.get(
    "/",
)
async def home():
    return {"Greeting!": "This server is using FastAPI with OpenAPI enabled :)"}

@app.post(
    "/leo/smart/collar/verifier",
)
async def verify_otp(otp: int):
    if str(otp) == totp.now():
        return {"Flag": flag}
    else:
        return {"Error": "code isn't correct!"}
