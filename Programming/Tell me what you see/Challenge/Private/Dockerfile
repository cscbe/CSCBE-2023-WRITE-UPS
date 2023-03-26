FROM python:3.8.12-slim

RUN apt-get update

RUN adduser --disabled-password --gecos '' geoffrey

USER geoffrey

ENV PATH = "/home/geoffrey/.local/bin:${PATH}"

WORKDIR /app

COPY server.py /app/

ENTRYPOINT ["python3", "-u", "server.py"]
