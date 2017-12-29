# -*- coding: utf-8 -*-
# 爬取 https://www.popupasia.com/?page_id=11&lang=zh 亞洲手創展品牌
from bs4 import BeautifulSoup
import requests
import csv




data = []
data.append(["brand"])


url = "https://www.popupasia.com/?page_id=193&lang=zh"
res = requests.get(url)
print res.encoding

soup = BeautifulSoup(res.text, "lxml")

for i in soup.select(".lshowcase-description"):
	print i
	data.append([i.text.encode("big5", "ignore")])



with open("popupasia.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)



