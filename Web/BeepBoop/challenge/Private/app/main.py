from fastapi import FastAPI, Response, Request
from fastapi.responses import HTMLResponse
import os
from dotenv import load_dotenv

app = FastAPI(openapi_url=None)
load_dotenv()
FLAG = os.getenv('FLAG', "CSC{ISSUE WITH THE CHALLENGE CALL AN ADMIN!}")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
        <html>
            <body>
                <h2>My first business app! I hope I will be rich with it</h1>
                <p><small>P.S: Don't try to search for potential other subpages, that's the only page browsable</small></p>
            </body>
        </html>
    """

@app.get('/robots.txt', response_class=HTMLResponse)
def robots():
    return """User-agent: Beep Boop<br>
Disallow: /c174/b4582<br>
Disallow: /b454/flag.txt<br>
Disallow: /c2121/b221<br>"""

@app.get('/c174/b4582', response_class=HTMLResponse)
def nothing():
   return """
    <html>
        <body>
            <img src="http://www.quickmeme.com/img/c8/c88bc3dc5be7c1fa50ff79af96fc2855953edf3883a759560dad88a5645ca724.jpg">
        </body>
    </html>
    """
   
@app.get('/c2121/b221', response_class=HTMLResponse)
def rickroll():
    return """
    <html>
        <head><!-- You didn't really think it would be that easy, did you? ;) """ + FLAG + """ --> </head>
        <body>
            <img src="https://media.tenor.com/HuyTG8nfZ90AAAAC/rick_astley_oh_reallyy.gif">
        </body>
    </html>
    """

@app.get('/b454/flag.txt', response_class=HTMLResponse)
def nothing2():
   return """
    <html>
        <body>
            <img src="https://media.tenor.com/rqJYP8tnzwEAAAAM/dicaprio-maybe.gif">
        </body>
    </html>
    """

   

   