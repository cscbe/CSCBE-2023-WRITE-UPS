FROM python:3.11.1-bullseye
RUN apt update && apt install openssl
RUN mkdir /instl
WORKDIR /instl
COPY ./app/requirements.txt requirements.txt
RUN openssl req -newkey rsa:4098 -nodes -keyout server.key -x509 -days 365 -out server.crt -subj "/C=BE/ST=Bruxelles/L=Bruxelles/O=CSC/CN=c2c.weirddom1337l33t.com"
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /app