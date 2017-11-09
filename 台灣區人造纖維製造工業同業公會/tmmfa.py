# -*- coding: utf-8 -*-
# 爬取 台灣區人造纖維製造工業同業公會http://www.tmmfa.org.tw/
from bs4 import BeautifulSoup
import requests
import csv



data = []
data.append(["company", "tel", "contact person"])

for comp_id in range(1, 50):
	print comp_id
	url = "http://www.tmmfa.org.tw/compdetail.aspx?sno=" + str(comp_id)
	
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "lxml")
	
	comp = soup.select("#lab_compname")[0].text.encode("big5")
	# print comp
	contact_person = soup.select("#lab_sale")[0].text.encode("big5")
	tel = soup.select("#lab_tel")[0].text.encode("big5")

	data.append([comp, tel, contact_person])

with open("tmmfa.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

print "DONE!"
