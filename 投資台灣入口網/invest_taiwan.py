# -*- coding: utf-8 -*-
# 爬取投資台灣入口網 http://investtaiwan.nat.gov.tw/showSuccessList?lang=cht
from bs4 import BeautifulSoup
import requests
import csv




data = []
data.append(["company"])

for i in range(1, 7):
	# print i

	payload = {
		"page":i,
		"lang":"cht"
	}
		
	url = "http://investtaiwan.nat.gov.tw/showSuccessList"
	res = requests.post(url, data = payload)
	soup = BeautifulSoup(res.text, "lxml")	
	
	for i in soup.select(".companyName"):
		data.append([i.text.encode("big5", "ignore")])




with open("invest_taiwan.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)


