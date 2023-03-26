import sys
from fastapi import FastAPI, Header, HTTPException
from os import getcwd
from fastapi.responses import FileResponse


app = FastAPI()


@app.get("/mips/c2c")
def download_c2c():
    return FileResponse(
        path=getcwd() + "/files/c2c",
        media_type="application/octet-stream",
        filename="c2c",
    )


@app.get("/mips/aHV0Y2h5.conf")
def download_c2c(x_c2c: str | None = Header(default=None)):
    if x_c2c == r"CSC{N0t_th3_fl4g}":
        return FileResponse(
            path=getcwd() + "/files/aHV0Y2h5.conf",
            media_type="application/octet-stream",
            filename="aHV0Y2h5.conf",
        )
    raise HTTPException(status_code=403, detail="Only c2c clients can do that!")
