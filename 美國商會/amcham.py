# -*- coding: utf-8 -*-
# 美國商會
from bs4 import BeautifulSoup
import requests
import csv
import time



data = []
data.append(["company", "tel"])



url = "https://amcham.com.tw/directory/"
res = requests.get(url)
soup = BeautifulSoup(res.text, "lxml")

for i in soup.select(".archive-company-list"):
	for j in i.select(".archive-company-list-item"):
		print j.text.encode("utf-8")
		comp_url = j.select("a")[0]["href"]
		comp_res = requests.get(comp_url)
		comp_soup = BeautifulSoup(comp_res.text, "lxml")
		
		info = comp_soup.select(".directory-listing-container")[0]
		comp = str(info)
		pos = comp.find("<br/>")
		comp = comp[(pos+5):comp.find("<br/>", pos+1)].strip().decode("utf-8", "ignore").encode("big5", "ignore")
		tel = info.select(".directory-listing-data")[1].text.encode("big5", "ignore")

		data.append([comp, tel])
		time.sleep(0.5)

	# 	break
	# break




with open("amcham.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)


