FROM python:3.9.18-slim

WORKDIR /recently-played

RUN apt-get update -y && apt-get install cron -y

COPY ./crontab-schedule /var/spool/cron/crontabs/root

COPY ./src/requirements.txt .

RUN pip3 install -r requirements.txt

COPY ./src/ .