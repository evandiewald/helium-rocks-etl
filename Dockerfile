FROM python:3.10-slim-buster

COPY . .

RUN apt-get update
RUN apt-get -y install gcc libpq-dev python3-dev

RUN pip install --no-cache-dir -r requirements.txt


