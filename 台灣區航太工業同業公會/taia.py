# -*- coding: utf-8 -*-
# 爬取 台灣區航太工業同業公會 http://www.taia.org.tw/index.asp
from bs4 import BeautifulSoup
import requests
import csv
import time
import random


data = []
data.append(["company", "tel"])



for comp_id in range(1, 105):
	print comp_id
	url = "http://www.taia.org.tw/member_d.asp?mitem=" + str(comp_id) + "&navno=4&secno=400"

	res = requests.get(url)
	soup = BeautifulSoup(res.text, "lxml")

	comp = soup.select("caption")[0].text.encode("big5", "ignore")
	for i in soup.select(".content")[0].select("tr"):
		if i.select("th")[0].text.encode("utf-8") == "電話：":
			tel = i.select("td")[0].text.encode("big5").strip()
			break

	data.append([comp, tel])


with open("taia.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

print "DONE!"
