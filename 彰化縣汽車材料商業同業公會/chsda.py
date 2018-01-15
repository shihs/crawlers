# -*- coding: utf-8 -*-
# 彰化縣汽車材料商業同業公會
from bs4 import BeautifulSoup
import requests
import csv
import time



data = []
data.append(["company"])


url = "http://www.chsda.org.tw/main.php?fid=04"

for page in range(12):
	payload = {
		"org_id":"1",
		"pageNo":str(page+1)
	}
	
	
	res = requests.post(url, data = payload)
	soup = BeautifulSoup(res.text, "lxml")
	
	for table in range(10):
		try:
			comp_info = str(soup.select("#form1")[0].select(".text9pt")[8+table*3])
		except:
			break
		start = comp_info.find("公司名稱:")+len("公司名稱:")
		
		comp = comp_info[start:comp_info.find("<br/>", start)]
		print comp
		
		data.append([comp.decode("utf-8", "ignore").encode("big5", "ignore")])

with open("chsda.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)
