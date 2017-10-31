# -*- coding: utf-8 -*-
# 爬取 ITAC中華民國國際貿易協會 http://www.trade-taiwan.org/index.asp
from bs4 import BeautifulSoup
import requests
import csv
import time
import random


data = []
data.append(["company id", "company", "tel"])

try_time = 0

for comp_id in range(1, 3000):
	url = "http://www.trade-taiwan.org/company_Contacts.asp?idno=" + str(comp_id)
	

	try:
		res = requests.get(url, timeout = 30)
	except:
		with open("ITAC.csv", "ab") as f:
			w = csv.writer(f)
			w.writerows(data)
		data = []
		
		if try_time == 10:
			break
		try_time += 1
		time.sleep(60)


	print res.status_code
	print url

	if res.status_code != 200:
		continue

	soup = BeautifulSoup(res.text, "lxml")

	try:
		comp = soup.select(".Item_title2")[0].text.encode(res.encoding, "ignore")

	
		for i in soup.select("table")[3].select("tr"):
			if i.select("td")[0].text == "Company Tel :":
				tel = i.select("td")[1].text.encode(res.encoding, "ignore")
	
		data.append([comp_id, comp, tel])
		time.sleep(1)

	except:
		continue

with open("ITAC.csv", "ab") as f:
	w = csv.writer(f)
	w.writerows(data)


print "Done!"

