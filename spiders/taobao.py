from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import  WebDriverWait
from urllib.parse import quote
from  pyquery import  PyQuery as pq

browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)
keyword = 'iPad'

def index_page(page):
    print('正在爬取第',page,'页')
    try:
        url = 'https://s.taobao.com/search?q=' + quote(keyword)
        browser.get(url)
        if page>1:
            input = wait.until(  EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
            submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager li.item.active > span'),str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
        get_products()
    except TimeoutException:
        index_page(page)


def get_products():
    html = browser.page_source
    doc = pq(html)
    items =doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product ={
            'image':item.find('.pic .img').attr('data-src'),
            'price':item.find('.price').text().replace('\n',''),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text().replace('\n',''),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text()
        }
        print(product)
        save_mango(product)

import pymongo
MONGO_URL = 'localhost'
MONGO_DB='taobao'
MONGO_COLLECTION = 'products'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
def save_mango(product):
    try:
        if db[MONGO_COLLECTION].insert(product):
            print('存储mongo成功')
    except Exception:
        print('存储mongo失败')


MAX_PAGE = 10
def main():
    for i in range(1,MAX_PAGE+1):
        index_page(i)



if __name__=='__main__':
    main()
