import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
class Ingridient:
    def __init__(self, name, link):
        self.name = name
        self.link = link



#     def crawling(self):
#         url = "https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=7%EC%9B%94+%EC%9D%8C%EC%8B%9D"
#         # source_code = urllib.request.urlopen(url).read()
#         chrome_options = Options()
#         chrome_options.add_argument('--headless')
#         chrome_driver_path = '../chromedriver.exe'
#         driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver_path)
#         driver.get(url)
#         # print(soup.find("ul", class_="_sfood-rolling-list"))
#         # print(soup.find("ul", class_="_sfood-rolling-list").find_all("li", class_="_sfood-rolling-item"))
#         # print(soup.find("span", class_="_sfood-pagination-info"))
#         soup = BeautifulSoup(driver.page_source, "html.parser")
#         for ingridient in soup.find("div", class_="_sfood-foodlist").find_all("li"):
#             # if ingridient.get_text() != "전체":
#             #     self.ingridient_list.append(ingridient.get_text())
#             self.ingridient_dict[ingridient['data-value']] = ingridient.find("img")['src']
#             # print(ingridient['data-value'])
#             # print(ingridient.find("img")['src'])
#
# #
# # a = Ingridient()
# # a.crawling()
# # print(a.ingridient_list)