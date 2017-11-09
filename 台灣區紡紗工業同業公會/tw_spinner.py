# -*- coding: utf-8 -*-
# 爬取 台灣區紡紗工業同業公會 http://www.tsa.org.tw/
from bs4 import BeautifulSoup
import requests
import csv





data = []
data.append(["company", "tel"])

for i in range(1, 100):
	print i
	url = "http://www.tsa.org.tw/memDP.aspx?sno=" + str(i)
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "lxml")
	
	comp = soup.select("#lab_namec")[0].text.encode("big5")
	tel = soup.select("#lab_tel")[0].text.encode("big5")

	data.append([comp, tel])


with open("tsa.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

print "DONE!"

