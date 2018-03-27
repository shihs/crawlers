# -*- coding: utf-8 -*-
# 爬取 2017德國漢諾威工具機展 http://www.emo-hannover.de/home
from bs4 import BeautifulSoup
import requests
import csv


data = []
data.append(["company", "tel"])


url = "http://www.emo-hannover.de/en/exhibition/exhibitors-products/exhibitor-index/exhibitor-lists.xhtml?n=RC"
res = requests.get(url)
soup = BeautifulSoup(res.text, "lxml")

for i in soup.select(".exhibitor-name"):

	comp_url = "http://www.emo-hannover.de" + i.select("a")[0]["href"]
	print comp_url.strip()
	comp_res = requests.get(comp_url)
	comp_soup = BeautifulSoup(comp_res.text, "lxml")

	comp_info = comp_soup.select(".col-inner")[0]

	comp = comp_info.select(".f-paragraph")[0].text.encode("utf-8").strip()

	if "Phone" in comp_info.select(".f-paragraph")[2].text.encode("utf-8"):
		tel = comp_info.select(".f-paragraph")[2].select("div")[0].text.encode("utf-8").replace("Phone: ", "").replace("+", "").strip()
	else:
		tel = ""

	data.append([comp, tel])
	print comp, tel
	print 


with open("emo_hannover.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)