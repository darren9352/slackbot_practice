# -*- coding: utf-8 -*-
import re
import urllib.request

from bs4 import BeautifulSoup
import View.Ask_Method
import Model.Ingridient_Model
import Controller.Shopping_control
import re
import Model.ShoppingMall_market_price
import Model.ShoppingMall_Model
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

SLACK_TOKEN = "xoxb-677120743489-689663463669-QytfaFX5lMzWN4kFgOtUbtSM"
SLACK_SIGNING_SECRET = "7d602b14f8d01b7c840ea51426ecffc1"

app = Flask(__name__)
# /listening 으로 슬랙 이벤트를 받습니다.
slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)
ingridient_list = []
receipe_list = []
test_block = []
blocks = []
choice = None
client_msg_id = []
my_price = 0
market_price =0
my_product = None
resend_state = 0
attachments = None
user_state = 0 # 0: 시작 단계, 1: 재료 리스트 보여주기, 2: 레시피 보여주기, 3: 종료
@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    global user_state
    global choice
    global blocks
    global client_msg_id
    global test_block
    global my_price
    global market_price
    global attachments
    global my_product
    global resend_state
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]
    print(text)
    msg_id = event_data["event"]["client_msg_id"]
    print(msg_id)
    if msg_id in client_msg_id:
        print('중복이다')
        return
    else:
        client_msg_id.append(msg_id)

    keywords = None
    # print(user_state)
    #
    #
    # print(text.split()[1] in ingridient_list)
    # print(ingridient_list)

    ok = False
    if user_state == 0 and text.split()[1] is not None:
        keywords = View.Ask_Method.show_check_menu()
        user_state = 1
        blocks = []
        # break
    elif user_state == 1 and (("1" in text.split()[1]) or ("시세" in text.split()[1]) or ("알아보기" in text.split()[1])):
        keywords = '어떤 물품의 가격을 검색하시겠습니까?'
        user_state = 9
    elif user_state == 9 and text.split()[1] is not None:
        my_product = text.split()[1]
        keywords = '현재 보이는 가격은 얼마 입니까?'
        user_state = 8
    elif user_state == 8 and text.split()[1] is not None:
        str_price = text.split()[1]
        prices = re.findall("\d+", str_price)
        tmp_str_price = ''
        for price in prices:
            tmp_str_price = tmp_str_price + price
        print(tmp_str_price)
        my_price = int(tmp_str_price)
        market_price_class = Model.ShoppingMall_market_price.Market_Price()
        market_price = market_price_class.crawling(my_product)
        keywords = str(my_price) + '원이 맞습니까?\n1.Y\n2.N'
        user_state = 7
    elif user_state == 7 and (("Y" in text.split()[1]) or ("1" in text.split()[1])):
        if my_price > market_price:
            blocks.append(	{
		"type": "image",
		"title": {
			"type": "plain_text",
			"text": "호구",
			"emoji": True
		},
		"image_url": "https://i0.wp.com/zeitpost.co.kr/wp-content/uploads/2016/07/20160727%EB%82%B4%EA%B0%80%ED%98%B8%EA%B5%AC%EB%9D%BC%EB%8B%881.jpg?resize=800%2C600",
		"alt_text": "호구"
	        })
            resend_state = 5
            user_state = 5
        else:
            blocks.append({
                "type": "image",
                "title": {
                    "type": "plain_text",
                    "text": "혜자",
                    "emoji": True
                },
                "image_url": "https://img1.daumcdn.net/thumb/R720x0.q80/?scode=mtistory2&fname=http%3A%2F%2Fcfile8.uf.tistory.com%2Fimage%2F226D4F355190597F08FCDF",
                "alt_text": "혜자"
            })
            resend_state = 6
            user_state = 4
    elif user_state == 5 and (("Y" in text.split()[1]) or ("1" in text.split()[1])):
        shoppingmall_class = Model.ShoppingMall_Model.ShoppingMall()
        print('my_product', my_product)
        shoppingmall_list = shoppingmall_class.crawling(my_product)
        print(shoppingmall_list)
        attachments = None
        i = 0
        for shoppingmall in shoppingmall_list:
            block = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "<https://www.naver.com|네이버>"
                },
                "accessory": {
                    "type": "image",
                    "image_url": "https://phinf.pstatic.net/dbscthumb/2891_000_1/20140312113255532_1JFUHSUMU.jpg/food673.jpg?type=f132_87_fst",
                    "alt_text": "image"
                }
            }
            block['text']['text'] = "<" + shoppingmall[2] + "|" + shoppingmall[3] + ">\n가격: " + shoppingmall[1] + "\n판매처: " + shoppingmall[0]
            block['accessory']['image_url'] = shoppingmall[4]
            blocks.append(block)
            blocks.append({"type": "divider"})
            i = i + 1
            if i == 10:
                break
        print(blocks)
        test_block = blocks
        user_state = 4
        resend_state = 7
    elif user_state == 1 and (("2" in text.split()[1]) or ("계절" in text.split()[1]) or ("음식" in text.split()[1]) or ("레시피" in text.split()[1])):
        keywords_list = View.Ask_Method.display_ingridient()
        slack_web_client.chat_postMessage(
            channel=channel,
            text='레시피를 얻을 7월 제철 재료를 고르십시오',
        )
        for keyword in keywords_list:
            block = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "<https://www.naver.com|네이버>"
                },
                "accessory": {
                    "type": "image",
                    "image_url": "https://phinf.pstatic.net/dbscthumb/2891_000_1/20140312113255532_1JFUHSUMU.jpg/food673.jpg?type=f132_87_fst",
                    "alt_text": "image"
                }
            }
            block['text']['text'] = keyword.name
            block['accessory']['image_url'] = keyword.link
            blocks.append(block)
            blocks.append({"type": "divider"})
            ingridient_list.append(keyword.name)
        #keywords = '음식을 선택하세요\n'+'\n'.join(ingridient_list)
        keywords = '음식을 선택하세요\n'
        user_state= 10
        print(ingridient_list)
        # break
    elif user_state == 10 and text.split()[1] in ingridient_list:
        print('Mychoice')
        choice = text.split()[1]
        blocks=[]
        keywords = choice + '를 선택 하겠습니까?\n1.Y\n2.N'
        print(keywords)
        user_state = 3
    elif user_state == 10 and text.split()[1] not in ingridient_list:
        keywords = '위의 리스트에 있는 재료 중 선택하십시오.'
        blocks = []
        # break
    elif user_state == 3 and (("Y" in text.split()[1]) or ("1" in text.split()[1])):
        print("INSIDE", choice)
        receipes_list = View.Ask_Method.display_receipe(Model.Ingridient_Model.Ingridient(choice,'ㅇㅇㄹㅇㄹㅇ'))
        for receipe in receipes_list:
            #print(receipe)
            block = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "<https://www.naver.com|네이버>"
                },
                "accessory": {
                    "type": "image",
                    "image_url": "https://phinf.pstatic.net/dbscthumb/2891_000_1/20140312113255532_1JFUHSUMU.jpg/food673.jpg?type=f132_87_fst",
                    "alt_text": "image"
                }
            }
            block['text']['text'] = "<"+receipe['link']+"|"+receipe['food']+">"
            block['accessory']['image_url'] = receipe['img']
            print(block)
            blocks.append(block)
            blocks.append({"type": "divider"})
            #receipe_list.append("<"+receipe['link']+"|"+receipe['food']+">" + " " +receipe['img'])
        resend_state = 7
        user_state = 4
        # break
    elif user_state == 4 and (("Y" in text.split()[1]) or ("1" in text.split()[1])):
        keywords = View.Ask_Method.exit()
        blocks = []
        print(keywords)
        user_state = 0
        # break
    elif user_state == 7 and (("N" in text.split()[1]) or ("2" in text.split()[1])):
        keywords = '가격을 다시 입력하십시오'
        user_state = 8
        blocks = []

    # if keywords is not None:
    slack_web_client.chat_postMessage(
        channel=channel,
        text=keywords,
        blocks=blocks,
        attachments = attachments
    )
    if resend_state == 5:
        slack_web_client.chat_postMessage(
            channel=channel,
            text='당신은 호구입니다. 추천 쇼핑몰 리스트를 받으시겠습니까?\n1.Y\n2.N',
        )
        blocks = []
        resend_state = 0
    elif resend_state == 6:
        slack_web_client.chat_postMessage(
            channel=channel,
            text='눈앞의 물건을 사시면 됩니다',
        )
        slack_web_client.chat_postMessage(
            channel=channel,
            text='종료하시겠습니까?\n1.Y\n2.N',
        )
        blocks = []
        resend_state = 0
    elif resend_state == 7:
        slack_web_client.chat_postMessage(
            channel=channel,
            text='종료하시겠습니까?\n1.Y\n2.N',
        )
        blocks = []
        resend_state = 0




# / 로 접속하면 서버가 준비되었다고 알려줍니다.
@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
