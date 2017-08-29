# -*- coding: utf-8 -*-
#the big5 Dubai https://www.thebig5.ae/
from bs4 import BeautifulSoup
import requests
import csv



data = []
data.append(["company", "Stand Number", "Country", "Tel", "Mail", "Web"])


url = "https://exhibitors.thebig5.ae/"
res = requests.get(url)

soup = BeautifulSoup(res.text, "lxml")

for i in soup.select("#results")[0].select("tr")[1:]:
	comp_info = i.select("td")
	comp = comp_info[0].text.encode(res.encoding, "ignore").strip()
	stand_number = comp_info[1].text.encode(res.encoding, "ignore").strip()
	country = comp_info[2].text.encode(res.encoding, "ignore").strip()

	comp_url = "https://exhibitors.thebig5.ae/" + comp_info[0].select("a")[0]["href"]
	comp_res = requests.get(comp_url)
	comp_soup = BeautifulSoup(comp_res.text, "lxml")

	tel = comp_soup.select("#MainPage_lblTelephone")[0].text.encode(res.encoding, "ignore").strip()
	mail = comp_soup.select("#MainPage_lblEmail")[0].text.encode(res.encoding, "ignore").strip()
	web = comp_soup.select("#MainPage_divweb")[0].text.encode(res.encoding, "ignore").strip()

	data.append([comp, stand_number, country, tel, mail, web])
	print comp


with open("thebig5.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)