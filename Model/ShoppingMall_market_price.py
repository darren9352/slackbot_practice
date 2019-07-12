import urllib.request
from bs4 import BeautifulSoup
from urllib import parse
from operator import itemgetter
import json

class Market_Price:
    def crawling(self,input_text):
        url ="https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query="+parse.quote("서울")+parse.quote(input_text)+parse.quote("소매가")
        source_code = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(source_code, "html.parser")
        print('input text',input_text)

        price = soup.find("div", class_="tab_info").find("div",class_="present").find("strong", class_="down")
        if price == None:
            price = soup.find("div", class_="tab_info").find("div",class_="present").find("strong", class_="stand")
        price = price.get_text(strip=True).replace(',','').replace('원','')

        return int(price)

if __name__ == "__main__":
    tmp = Market_Price()
    print(tmp.crawling("돼지고기"))
