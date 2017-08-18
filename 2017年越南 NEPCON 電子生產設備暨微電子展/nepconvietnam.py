# -*- coding: utf-8 -*-
# http://www.nepconvietnam.com/html/exhibitor_list.html#content  2017年越南 NEPCON 電子生產設備暨微電子展 NEPCON Vietnam 2017
from bs4 import BeautifulSoup
import requests
import csv


data = []
data.append(["company"])

url = "http://www.nepconvietnam.com/html/exhibitor_list.html#content"

res = requests.get(url)
soup = BeautifulSoup(res.text, "lxml")



for i in soup.select("#dataTables-example")[0].select("tr")[1:]:
	if i.select("td")[1].text == "TAIWAN":
		td = i.select("td")[0].encode(formatter="html").replace("&Acirc;&nbsp;", "")
		company = td[(td.find(">")+1):td.find("<", 2)].replace("    ", " ")
		data.append([company])


with open("nepconvietnam.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)


