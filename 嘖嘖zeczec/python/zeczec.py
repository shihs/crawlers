# -*- coding: utf-8 -*-
# 嘖嘖募資平台
from bs4 import BeautifulSoup
import requests
import csv




data = []
data.append(["Brand", "Statsu", "Money", "URL", "Source"])

page = 1
# brands = set()


while True:

	url = "https://www.zeczec.com/categories?page=" + str(page)
	print url
	
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "lxml")
	
	if len(soup.select(".a-project")) == 0:
		break
	
	for i in soup.select(".a-project"):
		brand_url = "https://www.zeczec.com" + i["href"]

		print i.select(".nowrap")[0].text.encode("utf-8", "ignore").replace("By ", "").strip()

		if len(i.select(".meta")[0].select(".nowrap")) != 0:
			meat = meta = i.select(".meta")[0].select(".nowrap")[0].text.encode("big5", "ignore").replace("By ", "").strip()
		else:
			try:
				meta = i.select(".meta")[0].select("span")[2].text.encode("big5", "ignore").replace("By ", "").strip()
			except:
				meta = i.select(".meta")[0].select("span")[0].text.encode("big5", "ignore").replace("By ", "").strip()

		status = i.select(".stand-label")[0].text.encode("big5", "ignore").replace("By ", "").strip()
		brand = i.select(".nowrap")[0].text.encode("big5", "ignore").replace("By ", "").strip()
		# brands.add(brand)
		

		data.append([brand, status, meta, brand_url, "zeczec"])

	page = page + 1





with open("zeczec.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)







