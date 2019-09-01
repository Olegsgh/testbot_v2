# -*- coding: utf-8 -*-
# reqs:
#   pip install bs4
#   pip install requests
#   pip install lxml

from bs4 import BeautifulSoup
import requests
# import json

# ========
# url_ = "https://habr.com/ru/"
# session = requests.Session()
# r = session.get(url_, timeout=5)
# print(r.text)
#
# soup = BeautifulSoup(r.content, "lxml")
#
# url_title = soup.title.get_text()
# print(url_title)
#
# items_list = soup.find_all('article', {'class': True})
# for item in items_list:
#     # print(item.get_text())
#     item_title = item.find('h2').a.get_text()
#     item_link = item.find('h2').a['href'].strip()
#     print(item_title, item_link)

# ========
# url_ = "https://meduza.io/"
# url_ = 'https://meduza.io/api/w5/search?chrono=news&page=0&per_page=24&locale=ru'
# session = requests.Session()
# r = session.get(url_, timeout=5)
# # print(r.text)
#
# # soup = BeautifulSoup(r.content, "lxml")
# # url_title = soup.title.get_text()
# # print(url_title)
#
# json_content = json.loads(r.content)
# items_list = json_content["documents"]
# for item in items_list:
#     item_title = json_content["documents"][item]["title"]
#     item_link = json_content["documents"][item]["url"]
#     print(item_title,item_link)

