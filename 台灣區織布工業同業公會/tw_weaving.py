# -*- coding: utf-8 -*-
# 爬取 台灣區織布工業同業公會 廠商名單 http://www.weaving.org.tw
from bs4 import BeautifulSoup
import requests
import csv
import time


data = []
data.append(["company", "tel"])

for page in range(8):
	url = "http://www.weaving.org.tw/member.php?page=" + str(page+1)
	print url
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "lxml")
	
	for i in soup.select(".search_table")[0].select("tr")[2:]:
		comp = i.select("td")[1].text.encode("big5", "ignore")
		tel = i.select("td")[2].text.encode("big5", "ignore")
		print comp
		data.append([comp, tel])

	time.sleep(3)

with open("weaving.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

print "DONE!"