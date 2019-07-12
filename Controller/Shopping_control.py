# -*- coding: utf-8 -*-
import re
import urllib.request

from bs4 import BeautifulSoup

from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
import Model.ShoppingMall_Model
import itertools

SLACK_TOKEN = "xoxb-677120743489-689663463669-QytfaFX5lMzWN4kFgOtUbtSM"
SLACK_SIGNING_SECRET = "7d602b14f8d01b7c840ea51426ecffc1"


app = Flask(__name__)
# /listening 으로 슬랙 이벤트를 받습니다.
slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)

@slack_events_adaptor.on("app_mention")
def ask_product(event_data):
    channel = event_data["event"]["channel"]
    print(event_data["event"])
    print(channel)
    text = event_data["event"]["text"]
    a= Model.ShoppingMall_Model.ShoppingMall()
    keywords = a.crawling("고구마")

    for keyword in keywords:
        for item in keyword:
            slack_web_client.chat_postMessage(
                channel=channel,
                text=item
            )

# def ask_price():
#     a = Model.ShoppingMall_Model.ShoppingMall()
#     keywords = a.crawling("고구마")
#     print(keywords)


# def display_available():
#
# def display_shopping_mall_list():
#


@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    # ask_price()
    app.run('0.0.0.0', port=5000)