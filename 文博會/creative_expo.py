# -*- coding: utf-8 -*-
# 2017文博會參展廠商
# https://creativexpo.tw/
from bs4 import BeautifulSoup
import requests
import csv

data = []
data.append(["place", "company", "email", "tel"])

for i in range(3):
	url = "https://creativexpo.tw/exhibitor-list-"+ str(i+1) + "/"
	
	res = requests.get(url)
	# print res.text.encode("utf-8")
	soup = BeautifulSoup(res.text, "html.parser")
	
	place = soup.select(".edgtf-title-subtitle-holder-inner")[0].select("span")[0].text.encode("utf-8").replace("參展商名錄 —", "")
	place = place.decode("utf-8").encode("big5")
	
	for i in soup.select(".edgtf-item-text-holder"):
		# print i.text.encode("utf-8")
		company = i.select(".edgtf-item-title")[0].text.encode("big5", "ignore").strip()
		print company
	
		email = i.select("div")[0].text.encode("big5", "ignore").replace("Email：".decode("utf-8").encode("big5"), "")
		tel = i.select("div")[1].text.encode("big5", "ignore").replace("TEL：".decode("utf-8").encode("big5"), "")
		print email
		print tel

		data.append([place, company, email, tel])


with open("creative_expo.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

	