FROM python:3.10-buster
ENV BOT_NAME=$BOT_NAME

WORKDIR /usr/src/app/bot

COPY requirements.txt /usr/src/app/bot
RUN pip install -r /usr/src/app/bot/requirements.txt
COPY . /usr/src/app/bot
