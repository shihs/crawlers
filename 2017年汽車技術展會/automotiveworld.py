# -*- coding: utf-8 -*-
# http://www.automotiveworld.jp/en/To-Visit/Exhibitor/ 2017年汽車技術展會(AUTOMOTIVE WORLD)
from bs4 import BeautifulSoup
import requests
import csv
import urllib



data = []
data.append(["company", "country", "tel"])


url = "http://jan2017.tems-system.com/ExhiSearch/AUTO/eng/ExhiList"

res = requests.get(url)
soup = BeautifulSoup(res.text, "lxml")

# print res.text.encode("utf-8")

for i in soup.select("#01")[0].select("li"):
	company = i.text.encode("big5", "replace").strip()
	if (len(i.select("a")) != 0):
		comp_url = "http://jan2017.tems-system.com/exhiSearch/AUTO/eng/Details?id=" + urllib.quote(i.select("a")[0]["val-id"]) + "&type=2"
		print comp_url

		comp_res = requests.get(comp_url)
		comp_soup = BeautifulSoup(comp_res.text, "lxml")

		info = comp_soup.select(".search_detail_info")[0]
		country = info.select("tr")[0].select("td")[0].text.encode("big5", "replace").replace("Country：".decode("utf-8").encode("big5"), "")
		tel = '"' + info.select("tr")[1].select("td")[1].text.encode("big5", "replace").replace("TEL：".decode("utf-8").encode("big5"), "") + '"'

	else:
		country = ""
		tel = ""

	data.append([company, country, tel])


with open("automotiveworld.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)






