import pandas as pd
from datetime import datetime
import requests
import time 
from requests_html import HTMLSession
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
from PIL import Image
from io import StringIO, BytesIO

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from IPython.display import display, clear_output


session = HTMLSession()

# s = Service('chromedriver')
# driver = webdriver.Chrome(service=s)
# pages = 1
# for p in range(1, pages+1):
#     bikroy_url = 'https://bikroy.com/bn/ads/bangladesh/mobiles?sort=date&order=desc&buy_now=0&urgent=0&page=1'
#     driver.get(bikroy_url)
# # driver.maximize_window()

# single_page_urls = []
# for i in range (1, 28):
#     try:
#         single_url = driver.find_element(by=By.XPATH, value=f'//*[@id="app-wrapper"]/div[1]/div[3]/div/div[2]/div[4]/div[2]/div/div[1]/div[1]/ul/li[{i}]/a').get_attribute('href')
#         single_page_urls.append(single_url)
#     except:
#         pass
# single_page_urls

# s = Service('chromedriver')

# s_driver = webdriver.Chrome(service=s)
# for s_u in single_page_urls:
#     s_driver.get(single_page_urls[2])
#     s_u = 'https://bikroy.com/bn/ad/samsung-galaxy-j2-used-for-sale-dhaka-division-3169'
#     s_driver.get(s_u)

single_page_urls = ['https://bikroy.com/bn/ad/xiaomi-redmi-note-9-pro-6-64-used-for-sale-khulna-7']
cnt = 1
for s_u in single_page_urls:
    print("Count: ", cnt)
    s_driver = session.get(s_u)
    time.sleep(5)

    s_driver.html.render()
    # s_driver.get(s_u)
    time.sleep(5)
    
    # single page data scrapping
    s_title = s_driver.html.find('h1').text
    # s_title = r.html.find('h1').text

#     //*[@id="app-wrapper"]/div[1]/div[2]/div[2]/div[1]/div[1]/div/div[1]/div/div[1]/div[2]/div/div/h1
    #     //*[@id="app-wrapper"]/div[1]/div[2]/div[2]/div[1]/div[1]/div/div[1]/div/div[1]/div[2]/div/div/h1
    print("Title: ", s_title)

    # scrapping all images
    try:
        images = s_driver.html.xpath('//*[@id="app-wrapper"]/div[1]/div[2]/div[2]/div[3]/div[2]/div/div[1]/div/div[1]/div/div/ul')
        for img in images.html.find('img'):
            img_urls = img.get_attribute('src')

            img_urls_firstname = '/'.join(img_urls.split('/')[:-3])
            img_urls_rename = img_urls_firstname + '/620/466/fitted.jpg'
    #         print(img_urls_rename)
            img_name = '@'.join(img_urls_firstname.split('/')[-2:])

            r = requests.get(img_urls_rename)
            i = Image.open(BytesIO(r.content))
            i.save(f"img/mobile/{img_name}.jpg")
    except:
        print('No images')

    # extractig meta data
    meta_data = s_driver.html.xpath('//*[@id="app-wrapper"]/div[1]/div[2]/div[2]/div[3]/div[2]/div/div[1]/div/div[2]/div[2]')
    
    md = meta_data.html.find('div')
    meta_dic = {}
    for m in md:
        m = m.text
        if '\n' in m:
            key, val = m.split('\n')[0].replace(':', ''), m.split('\n')[1]
            meta_dic[key] = val
    print("Meta Data: ", meta_dic)

    # extracting description
    # click on show_more button
    try:
        s_driver.html.xpath('//*[@id="app-wrapper"]/div[1]/div[2]/div[2]/div[3]/div[2]/div/div[1]/div/div[2]/div[3]/div/div[2]/div/div[2]/button').click()
        time.sleep(3)
    except:
        print("No show more button")
    # desc = s_driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/div[2]/div[3]/div[2]/div/div[1]/div/div[2]/div[3]/div/div[2]/div/div[1]/div/ul/div')
    # description[0].text
    # description = [d.text.replace("'\uf076", "").replace("''\uf0d8", "") for d in desc.find_elements_by_tag_name('p')]
    # print(description)

    try:
        feature = s_driver.html.xpath('//*[@id="app-wrapper"]/div[1]/div[2]/div[2]/div[1]/div[1]/div/div[1]/div/div[2]/div[4]').text
        print(feature)
        # feature_lst.append(feature)
    except:
        print("No feature")

    desc = s_driver.html.xpath('//*[@id="collapsible-content-0"]/ul/div')
    print("Description: ", desc.text)
    print("=============================================")
    cnt += 1
