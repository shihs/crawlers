# -*- coding: utf-8 -*-
# 爬取 GMDU.net 台灣廠商名單 https://www.gmdu.net/
from bs4 import BeautifulSoup
import requests
import csv
import time
import random


page = 0

data = []
data.append(["company", "tel"])

while True:
	page += 1
	url = "https://www.gmdu.net/loca-5-p" + str(page) + ".html"
	print url

	try:
		res = requests.get(url)	
		soup = BeautifulSoup(res.text, "lxml")
	except:
		with open("gmdu.csv", "ab") as f:
			w = csv.writer(f)
			w.writerows(data)
		data = []
		time.sleep(60)

	if len(soup.select(".user-left-title")) != 0:
		break
	
	for i in soup.select(".itemlist"):
		comp = i.select("a")[0].text.encode("utf-8", "igrnoe")
		tel = i.select(".telephone")[0].select(".value")[0].text.encode("utf-8", "igrnoe")
		print comp

	data.append([comp, tel])

	time.sleep(random.randint(8, 12))


with open("gmdu.csv", "ab") as f:
	w = csv.writer(f)
	w.writerows(data)


print "FINISHED!"
