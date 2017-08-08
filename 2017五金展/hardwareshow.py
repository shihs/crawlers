# -*- coding: utf-8 -*-
#2017台灣五金展
from bs4 import BeautifulSoup
import requests
import csv



page = 0

first = ""
data = []

with open("hardwareshow.csv", "w") as f:
	f.write("company" + "\n")


while True:
	page = page + 1
	print page

	url = "http://www.hardwareshow.com.tw/visitors/ExhibitList_cht.asp?page=" + str(page) + "&ShowYears=2017"

	res = requests.get(url)
	print res.encoding
	soup = BeautifulSoup(res.text, "lxml")

	if first == soup.select(".ExSearchResult")[0].select("li"):
		break
	else:
		first = soup.select(".ExSearchResult")[0].select("li")

	for i in soup.select(".ExSearchResult")[0].select("li"):
		# data.append(i.text)
		company = i.text.encode("iso-8859-1").decode("utf-8", "ignore").encode("big5", "ignore")
		with open("hardwareshow.csv", "a") as f:
			f.write('"' + company + '"\n')




# for i in range(len(data)):
# 	data[i] = data[i].encode("iso-8859-1").decode("utf-8", "ignore").encode("big5", "ignore")




# with open("hardwareshow.csv", "wb") as f:
# 	w = csv.writer(f)
# 	w.writerows(data)