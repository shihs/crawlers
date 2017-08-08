# -*- coding: utf-8 -*-
#抓取2017台北紡織展廠商名單http://www.titas.tw/2017/cht/
from bs4 import BeautifulSoup
import requests
import csv


first = ""
page = 0



with open("taipei_textile.csv", "w") as f:
	f.write("company" + "\n")



while True:
	page = page + 1
	print page
	url = "http://www.titas.tw/2017/cht/visitor/exhibitorslist/?page=" + str(page) + "&ExYear=2016"
	res = requests.get(url)
	# print res.encoding
	soup = BeautifulSoup(res.text, "lxml")


	if soup.select(".table-fill")[0].select("tr")[1].select("td")[1].select("a")[0] == first:
		break
	else:
		first = soup.select(".table-fill")[0].select("tr")[1].select("td")[1].select("a")[0]

	for i in soup.select(".table-fill")[0].select("tr")[1:]:
		company = i.select("td")[1].select("a")[0].text.encode(res.encoding).decode("utf-8").encode("big5", "ignore")
		with open("taipei_textile.csv", "a") as f:
			f.write('"' + company + '"\n')

