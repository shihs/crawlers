# -*- coding: utf-8 -*-
# 台灣文創拓展網https://ccimarketing.org.tw
from bs4 import BeautifulSoup
import requests
import csv
import math
import time
import sys


# 公司頁面
url = "https://ccimarketing.org.tw/company"
res = requests.get(url)
soup = BeautifulSoup(res.text, "lxml")
companies = soup.select(".images_holder")


data = []
data.append(["company", "brand", "tel", "mail", "address"])

# 公司資訊頁面
for i in companies:
	brand = ""
	tel = ""
	mail = ""
	address = ""
	href = i.select("a")
	# 有公司資訊頁面
	if len(href) != 0:
		url = href[0]["href"]
		res = requests.get(url)
		soup = BeautifulSoup(res.text, "lxml")
		company = soup.select(".separator_content")[0].text.encode("big5", "ignore")
		print company.decode("big5", "ignore").encode("utf-8", "ignore")
		info = soup.select(".square_small")
		for j in info:
			if "+886" in str(j) or "品牌名稱" in str(j):
				info = j.select(".masonry_gallery_item_content")[0]
				break

		try:
			brand = info.select("h3")[0].text.encode("utf-8").replace("品牌名稱：", "").replace("品牌名稱 : ", "").strip().decode("utf-8").encode("big5", "ignore")

		except Exception as e:
			print e

		try:
			tel = info.select("div")[0].text.encode("big5", "ignore").strip()
			mail = info.select("div")[1].text.encode("big5", "ignore").strip()
			address = info.select("div")[2].text.encode("big5", "ignore").strip()
		except Exception as e:
			print e
		
		data.append([company, brand, tel, mail, address])	

with open("fresh_taiwan.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)


print "DONE!"


