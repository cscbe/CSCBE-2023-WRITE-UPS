from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
import os
from dotenv import load_dotenv

app = FastAPI(openapi_url=None)
load_dotenv()
FLAG = os.getenv('FLAG', "CSC{ISSUE WITH THE CHALLENGE CALL AN ADMIN!}")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """ <!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>UNFILTERED REALITY</title>
	<style>
		html, body {
			margin: 0;
			padding: 0;
			height: 100%;
			background-color: #000;
			color: #fff;
			font-family: "Comic Sans MS", cursive, sans-serif;
			font-size: 16px;
			line-height: 1.4;
            display: flex;
			flex-direction: column;
			justify-content: center;
			align-items: center;
		}
        .footer {
        position: fixed;
        bottom: 0;
        right: 0;
        padding: 10px;
        background-color: #000;
      }
		h1, h2, h3, p, a {
			text-shadow: 1px 1px #ff00ff;
		}

		h1 {
			font-size: 48px;
			margin-top: 50px;
			text-align: center;
			animation: neon 1s ease-in-out infinite alternate;
		}

		h2 {
			font-size: 32px;
			margin-top: 50px;
			text-align: center;
			animation: shake 0.5s ease-in-out infinite;
		}

		p {
			margin-top: 20px;
			text-align: center;
			animation: rotate 2s linear infinite;
		}

		a {
			text-decoration: none;
			color: #ff00ff;
			border-bottom: 1px dotted #ff00ff;
			animation: blink 0.5s linear infinite;
		}

		@keyframes neon {
			from { text-shadow: 1px 1px #ff00ff; }
			to { text-shadow: 2px 2px #00ffff; }
		}

		@keyframes shake {
			from { transform: rotate(0deg); }
			to { transform: rotate(10deg); }
		}

		@keyframes rotate {
			from { transform: rotate(0deg); }
			to { transform: rotate(360deg); }
		}

		@keyframes blink {
			0% { opacity: 1; }
			50% { opacity: 0; }
			100% { opacity: 1; }
		}
	</style>
</head>
<body>
	<h1>Welcome to the REALITY BLOG</h1>
	<h2>Here is all my *controversial* thoughts</h2>
    <h3>I speak only REALITY and FACTS</h3>
	<p>Check out my AMAZING<a href=/blogposts>blog posts</a>!</p>
    <div class="footer">
      <p>Last updated: March 2 1997</p>
    </div>
</body>
</html>
"""

@app.get("/blogposts", response_class=HTMLResponse)
async def browser_check(request: Request):
    user_agent = request.headers.get("user-agent")
    if "Netscape" not in user_agent and "Mozilla/4." not in user_agent:
        return """
    <!DOCTYPE html>
<html>
<head>
	<title>Access Denied</title>
	<style>
		body {
			background-color: #ff0000;
			color: white;
			font-family: Impact, sans-serif;
			font-size: 2em;
			text-align: center;
			padding-top: 50px;
		}

		h1 {
			font-size: 4em;
			margin-bottom: 50px;
			animation: neon 2s infinite;
			text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #ff00de, 0 0 40px #ff00de, 0 0 70px #ff00de, 0 0 80px #ff00de, 0 0 100px #ff00de;
		}

		@keyframes neon {
			0% {
				color: white;
				text-shadow: none;
			}
			20% {
				color: #ff00de;
				text-shadow: none;
			}
			30% {
				color: #ff00de;
				text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #ff00de, 0 0 40px #ff00de, 0 0 70px #ff00de, 0 0 80px #ff00de, 0 0 100px #ff00de;
			}
			100% {
				color: white;
				text-shadow: none;
			}
		}

		img {
			width: 200px;
			height: 200px;
			margin-bottom: 50px;
			animation: rotate 3s linear infinite;
		}

		@keyframes rotate {
			from {
				transform: rotate(0deg);
			}
			to {
				transform: rotate(360deg);
			}
		}

		p {
			font-size: 1.5em;
			animation: shake 1s linear infinite;
		}

		@keyframes shake {
			0% {
				transform: translate(0, 0);
			}
			10% {
				transform: translate(-5px, 0);
			}
			20% {
				transform: translate(5px, 0);
			}
			30% {
				transform: translate(-5px, 0);
			}
			40% {
				transform: translate(5px, 0);
			}
			50% {
				transform: translate(-5px, 0);
			}
			60% {
				transform: translate(5px, 0);
			}
			70% {
				transform: translate(-5px, 0);
			}
			80% {
				transform: translate(5px, 0);
			}
			90% {
				transform: translate(-5px, 0);
			}
			100% {
				transform: translate(0, 0);
			}
		}
	</style>
</head>
<body>
	<h1>ACCESS DENIED</h1>
	<img src="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/851318cc-1465-4aa2-8af6-8a8008ba9c4f/d2b805k-32f7b5af-e170-401a-8b1d-b4c607123de4.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzg1MTMxOGNjLTE0NjUtNGFhMi04YWY2LThhODAwOGJhOWM0ZlwvZDJiODA1ay0zMmY3YjVhZi1lMTcwLTQwMWEtOGIxZC1iNGM2MDcxMjNkZTQuZ2lmIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.fiW9rzyb4yNK1vdCzx4T-QXsdFbhplWvfmE3n3sAKXg" alt="Access Denied">
    <p>ARE YOU FROM THE GOVERNMENT AND TRY TO SPY MY AMAZING AND FAMOUS CONTROVERSIAL POSTS ?</p>
    <p>OR MAYBE YOU COME FROM THE FUTURE... I DON'T TRUST NEW BROWSERS YOU KNOW...</p>
    </body>
 """
    else: 
        return """
    <!DOCTYPE html>
<html>
<head>
	<title>BLOGPOSTS</title>
</head>
<style>
body {
    background-color: black;
    color: lime;
    font-family: 'Comic Sans MS', sans-serif;
    font-size: 16px;
    margin: 0;
}

h1 {
    font-size: 36px;
    text-align: center;
    text-transform: uppercase;
    text-shadow: 0 0 10px white, 0 0 20px white, 0 0 30px magenta, 0 0 40px magenta, 0 0 70px magenta, 0 0 80px magenta, 0 0 100px magenta;
    margin: 30px 0;
    animation: neon 1.5s ease-in-out infinite alternate;
}

.post {
    border: 5px solid magenta;
    padding: 20px;
    margin-bottom: 50px;
    background-color: black;
    animation: glitch 1s infinite linear alternate-reverse;
}

.post h2 {
    font-size: 24px;
    margin-top: 0px;
    text-align: center;
    text-shadow: 0 0 5px magenta, 0 0 10px magenta, 0 0 15px magenta, 0 0 20px magenta, 0 0 25px magenta;
}

.post p {
    font-size: 20px;
    text-align: justify;
    text-shadow: 0 0 5px magenta, 0 0 10px magenta, 0 0 15px magenta, 0 0 20px magenta, 0 0 25px magenta;
}

.admin-button {
			position: absolute;
			top: 20px;
			right: 20px;
			padding: 10px;
			background-color: #ff00de;
			color: #000000;
			font-size: 18px;
			border: none;
			border-radius: 5px;
			cursor: pointer;
}

.admin-button:hover {
			background-color: #000000;
			color: #ff00de;
			transition: all 0.3s ease;
}

@keyframes neon {
    from {
        text-shadow: 0 0 10px white, 0 0 20px white, 0 0 30px magenta, 0 0 40px magenta, 0 0 70px magenta, 0 0 80px magenta, 0 0 100px magenta;
    }
    to {
        text-shadow: 0 0 15px white, 0 0 30px white, 0 0 45px magenta, 0 0 60px magenta, 0 0 105px magenta, 0 0 120px magenta, 0 0 150px magenta;
    }
}

@keyframes glitch {
    2%, 64% {
        transform: translate(2px, 0) skew(0deg);
    }
    4%, 60% {
        transform: translate(-2px, 0) skew(0deg);
    }
    62% {
        transform: translate(0, 0) skew(5deg);
    }
}
</style>
<body>
	<h1>MY BLOGPOSTS</h1>
	<a href="/blogposts/d223/admin" class="admin-button">Admin</a>
	<div class="post">
		<h2>Worrying about Y2K </h2>
		<p>I'm really worried about the Y2K bug. I've spent so much time building my famous blog, and now I fear that it might be lost forever. To be honest, I think that the government might be behind all of this. Why else would they let such a catastrophic bug exist? Is this their way of silencing the famous person I am ? </p>
        <p style="font-size: 14px;">Views: <span id="post1-views">3</span></p>
	</div>

	<div class="post">
		<h2>Why I'm not drinking still water</h2>
		<p>As the government provides us free, still water, it's natural to be skeptical about their intentions. </p>
        <p style="font-size: 14px;">Views: <span id="post1-views">1</span></p>
	</div>
</body>
</html>
    """

@app.get("/blogposts/d223/admin", response_class=HTMLResponse)
async def check_debug_cookie(request: Request):
    user_agent = request.headers.get("User-Agent")
    if "Netscape" not in user_agent and "Mozilla/4." not in user_agent:
        return """
    <!DOCTYPE html>
<html>
<head>
	<title>Access Denied</title>
	<style>
		body {
			background-color: #ff0000;
			color: white;
			font-family: Impact, sans-serif;
			font-size: 2em;
			text-align: center;
			padding-top: 50px;
		}

		h1 {
			font-size: 4em;
			margin-bottom: 50px;
			animation: neon 2s infinite;
			text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #ff00de, 0 0 40px #ff00de, 0 0 70px #ff00de, 0 0 80px #ff00de, 0 0 100px #ff00de;
		}

		@keyframes neon {
			0% {
				color: white;
				text-shadow: none;
			}
			20% {
				color: #ff00de;
				text-shadow: none;
			}
			30% {
				color: #ff00de;
				text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #ff00de, 0 0 40px #ff00de, 0 0 70px #ff00de, 0 0 80px #ff00de, 0 0 100px #ff00de;
			}
			100% {
				color: white;
				text-shadow: none;
			}
		}

		img {
			width: 200px;
			height: 200px;
			margin-bottom: 50px;
			animation: rotate 3s linear infinite;
		}

		@keyframes rotate {
			from {
				transform: rotate(0deg);
			}
			to {
				transform: rotate(360deg);
			}
		}

		p {
			font-size: 1.5em;
			animation: shake 1s linear infinite;
		}

		@keyframes shake {
			0% {
				transform: translate(0, 0);
			}
			10% {
				transform: translate(-5px, 0);
			}
			20% {
				transform: translate(5px, 0);
			}
			30% {
				transform: translate(-5px, 0);
			}
			40% {
				transform: translate(5px, 0);
			}
			50% {
				transform: translate(-5px, 0);
			}
			60% {
				transform: translate(5px, 0);
			}
			70% {
				transform: translate(-5px, 0);
			}
			80% {
				transform: translate(5px, 0);
			}
			90% {
				transform: translate(-5px, 0);
			}
			100% {
				transform: translate(0, 0);
			}
		}
	</style>
</head>
<body>
	<h1>ACCESS DENIED</h1>
	<img src="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/851318cc-1465-4aa2-8af6-8a8008ba9c4f/d2b805k-32f7b5af-e170-401a-8b1d-b4c607123de4.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzg1MTMxOGNjLTE0NjUtNGFhMi04YWY2LThhODAwOGJhOWM0ZlwvZDJiODA1ay0zMmY3YjVhZi1lMTcwLTQwMWEtOGIxZC1iNGM2MDcxMjNkZTQuZ2lmIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.fiW9rzyb4yNK1vdCzx4T-QXsdFbhplWvfmE3n3sAKXg" alt="Access Denied">
    <p>ARE YOU FROM THE GOVERNMENT AND TRY TO SPY MY AMAZING AND FAMOUS CONTROVERSIAL POSTS ?</p>
    <p>OR MAYBE YOU COME FROM THE FUTURE... I DON'T TRUST NEW BROWSERS YOU KNOW...</p>
    </body>
 """
    response = Response()
    if request.cookies.get("debug") == "1":
        return """
 <!DOCTYPE html>
<html>
  <head>
    <title>Matrix mode</title>
    <style>
      * {margin: 0; padding: 0}
      body {background: #000;}
      canvas {display: block;}
      h1 {
        font-size: 100px;
        margin-top: 200px;
        text-shadow: 2px 2px 4px #00ff00;
      }
      @keyframes blink {
        50% {
          color: #ff00ff;
        }
      }
      .flash {
        animation: blink 1s linear infinite;
      }
    </style>
  </head>
  <body>
    <canvas></canvas>
    <script>
      var canvas = document.querySelector('canvas'),
          ctx = canvas.getContext('2d');

      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;

      var letters = '""" + FLAG + """';
      letters = letters.split('');

      var fontSize = 10,
          columns = canvas.width / fontSize;

      var drops = [];
      for (var i = 0; i < columns; i++) {
        drops[i] = 1;
      }

      function draw() {
        ctx.fillStyle = 'rgba(0, 0, 0, .1)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        for (var i = 0; i < drops.length; i++) {
          var text = letters[Math.floor(Math.random() * letters.length)];
          ctx.fillStyle = '#0f0';
          ctx.fillText(text, i * fontSize, drops[i] * fontSize);
          drops[i]++;
          if (drops[i] * fontSize > canvas.height && Math.random() > .95) {
            drops[i] = 0;
          }
        }
      }
      setInterval(draw, 33);
    </script>
  </body>
</html>
"""
    else:
        return """
    <html>
	<head>
		<title>ACCESS DENIED</title>
		<style>
			body {
				background-color: red;
				font-family: "Courier New", Courier, monospace;
			}
			h1 {
				color: green;
				font-size: 60px;
				text-align: center;
				margin-top: 100px;
			}
			p {
				color: green;
				font-size: 30px;
				text-align: center;
				margin-top: 50px;
			}
		</style>
	</head>
	<body>
		<h1>Are you trying TO SPY ME ???</h1>
		<p>Only debuggers users (my big bro) and the super famous admin of this blog (me) can view this page so DO NOT try again !!!</p>
	</body>
</html>
"""
