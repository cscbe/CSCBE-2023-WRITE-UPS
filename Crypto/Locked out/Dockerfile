FROM python:3

EXPOSE 5555/tcp

WORKDIR /app


RUN apt update
RUN apt install socat -y

RUN pip3 install pycryptodome

COPY socat_server.sh .
COPY challenge.py .

ENV FLAG=CSC{Preimage_resistance_is_important}
ENTRYPOINT ./socat_server.sh
