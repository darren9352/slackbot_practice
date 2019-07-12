import Model.Ingridient_Model
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



import Model.Ingridient_Model

class Receipe():
    def __init__(self, ingridient):
        self.ingridient = ingridient
        self.receipe_list = []

    def crawling(self):
        url = "https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=7%EC%9B%94+%EC%9D%8C%EC%8B%9D"
        # source_code = urllib.request.urlopen(url).read()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_driver_path = '../chromedriver.exe'
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver_path)
        driver.get(url)
        print(url)
        driver.find_element_by_class_name("_sfood-rolling-area").find_element_by_partial_link_text(self.ingridient.name).click()
        print(self.ingridient.name)
        css_selector = "#_seasonal_food > div.lst_other2._sfood-detailarea > div.other_cook._sfood-dishbox > ul > li:nth-child(1)"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        #print(soup.find("ul", class_="_sfood-dishlist"))
        for receipe in soup.find("ul", class_="_sfood-dishlist").find_all("li"):
            food = receipe.find("a", class_="flex_t").get_text()
            refer = receipe.find("span", class_="flex_s").get_text()
            link = receipe.find("a", class_="thumb")['href']
            img = receipe.find("img")['src']
            self.receipe_list.append({"food":food, "refer":refer, "link":link, "img":img})
