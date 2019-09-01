import requests
import lxml

import bs4

url = "https://habr.com/ru"
session = requests.session()
r = session.get(url, timeout = 5)

soup = bs4.BeautifulSoup(r.content, "lxml")

title = soup.title.get_text()
print(title)

items_list = soup.find_all('article', {'class': True})
for item in items_list:
    item_title = item.find('h2').a.get_text()
    item_text = item.find('h2').a['href'].strip()
    print(item_title)