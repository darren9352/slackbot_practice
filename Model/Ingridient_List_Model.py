import urllib.request
import Model.Ingridient_Model
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Ingridient_List:
    def __init__(self):
        self.ingridient_list = []

    def crawling(self):
        url = "https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=7%EC%9B%94+%EC%9D%8C%EC%8B%9D"
        # source_code = urllib.request.urlopen(url).read()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_driver_path = '../chromedriver.exe'
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver_path)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for ingridient in soup.find("div", class_="_sfood-foodlist").find_all("li"):
            self.ingridient_list.append(Model.Ingridient_Model.Ingridient(name=ingridient['data-value'], link=ingridient.find("img")['src']))

