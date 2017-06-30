# -*- coding: utf-8 -*-
#爬取2017生技月廠商名單https://www.biotaiwanexhibition.com/visitorExhibitor.asp
from bs4 import BeautifulSoup
import requests
import csv


data = []
data.append(["company", "area"])

page = 0
last_comany = ""

while True:
	page += 1

	url = "https://www.biotaiwanexhibition.com/visitorExhibitor.asp?page=" + str(page) + "&Area="
	
	res = requests.get(url, timeout = 30)
	soup = BeautifulSoup(res.text, "lxml")
	
	product = soup.select("#product")[0]


	if product.select("li")[-1] == last_comany:
		break

	for i in product.select("li"):
		try:
			right = i.select(".right")[0]
			company = right.select("a")[0].text.encode(res.encoding).decode("utf-8", "ignore").encode("big5", "ignore")
			area = right.select("p")[1].select("a")[0].text.encode(res.encoding).decode("utf-8", "ignore").encode("big5", "ignore")
		
		except:
			continue

		data.append([company, area])

	last_comany = product.select("li")[-1]



	print str(page) + " is done!"

with open("biotaiwanexhibition.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)


print "finished!"