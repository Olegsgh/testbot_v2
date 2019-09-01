import requests
import lxml
import json

import bs4

url = "https://meduza.io/api/w5/screens/news"
session = requests.session()
r = session.get(url, timeout = 5)

json_content = json.loads(r.content)

items_list = json_content["documents"]
for item in items_list:
    try:
        item_title = json_content["documents"][item]["title"]
        item_url = json_content["documents"][item]["url"]
        print(item_title,item_url)
    except:
        print("no data")