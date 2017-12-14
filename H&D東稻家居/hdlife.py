# -*- coding: utf-8 -*-
# 東稻家居
import requests
from bs4 import BeautifulSoup
import csv




data = []
data.append(["Brand"])


url = "http://www.hdlife.com.tw/"

res = requests.get(url)
soup = BeautifulSoup(res.text, "lxml")

brands = set()

for i in soup.select(".brandLogoWrap")[0].select(".brandLogoBox"):
	# brand_url = i["href"].encode("utf-8")
	# print i["href"].replace("http://www.hdlife.com.tw/Browsing/Brands/", "").encode("utf-8")
	brand = i["title"].encode("big5", "ignore")
	print brand
	brands.add(brand)

for i in soup.select(".brandSPmenu"):
	brand = i.text.encode("big5", "ignore").strip()
	print brand
	brands.add(brand)


for i in brands:
	data.append([i])


with open("hdlife.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)


