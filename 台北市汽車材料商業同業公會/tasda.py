# -*- coding: utf-8 -*-
# 台北市汽車材料商業同業公會
from bs4 import BeautifulSoup
import requests
import csv
import time


data = []
data.append(["company", "tel"])




for page in range(27):
	url = "http://www.tasda.org.tw/DspDir/dsp_index.cfm"
	
	# page = 1
	payload = {
		"FuncNO":"25",
		"PAGEID":str(page+1)
	}
	
	
	res = requests.post(url, data = payload)
	# print res.text.encode("utf-8")
	soup = BeautifulSoup(res.text, "lxml")
	# print soup.select(".member")[0]
	for i in soup.select(".member")[0].select("table")[:-2]:
		comp = i.select("td")[0].text.encode("big5", "ignore")
		tel = i.select("font")[1].text.encode("big5", "ignore")
		print comp
		tel = tel[5:tel.find("/")].strip()
		print tel
	
		data.append([comp, tel])
	
	

with open("tasda.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

