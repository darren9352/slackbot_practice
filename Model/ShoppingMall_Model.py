import urllib.request
from bs4 import BeautifulSoup
from urllib import parse
from operator import itemgetter
import json

class ShoppingMall:

    def sorting_data(self,list_data):
        return sorted(list_data, key=itemgetter(5))

    def crawling(self,input_text):

        shopping_mall_data = []
        url = "https://search.shopping.naver.com/search/all.nhn?query="+parse.quote(input_text)+"&frm=NVSCPRO"

        source_code = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(source_code, "html.parser")
        item_img_list = []
        item_mall_list = []
        item_price_list = []
        for item in soup.find("ul", class_="goods_list").find_all("li",class_="_itemSection"):
            item_img_list.append(item.find("div", class_="img_area").find("a", class_="img").find("img", class_="_productLazyImg")['data-original'])

        for item in soup.find_all("div",class_="info_mall"):
            cur = item.find("p",class_="mall_txt").find("a")
            if cur.get_text(strip=True)=="":
                cur= item.find("img")['alt']
            else :
                cur=cur.get_text(strip=True)
            item_mall_list.append(cur)

        for item in soup.find_all("span",class_="price"):
            item_price_list.append(item.find("em").get_text(strip=True))
        cnt = 0
        for item in soup.find_all("div",class_="info"):
            shopping_mall_name = item.find("a",class_="tit").get_text(strip=True)
            shopping_mall_name = shopping_mall_name.replace(' ', '')
            item_link = item.find("a").get("href")
            item_price_data = item_price_list[cnt].replace(',', '').replace('원','')
            item_price_data = int(item_price_data)
            shopping_mall_data.append([item_mall_list[cnt], item_price_list[cnt], item_link, shopping_mall_name, item_img_list[cnt],item_price_data])

            cnt += 1

        sorted_data_list = self.sorting_data(shopping_mall_data)
        return sorted_data_list

if __name__ == "__main__":
    tmp = ShoppingMall()
    tmp.crawling(" 고구마")

