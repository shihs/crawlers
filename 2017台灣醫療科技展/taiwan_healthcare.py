# -*- coding: utf-8 -*-
# 2017台灣醫療科技展
from bs4 import BeautifulSoup
import requests
import csv



data = []
data.append(["company"])


for page in range(3):

	url = "https://expo.taiwan-healthcare.org/visit/exhibitor-list.php?PageNO=" + str(page+1)
	res = requests.get(url)

	soup = BeautifulSoup(res.text, "lxml")

	for i in soup.select("#accordion")[0].select(".panel"):
		company = i.select(".col-sm-6")[0].text.encode("utf-8").strip()
		print company

		data.append([company])



with open("taiwan_healthcare.csv", "wb") as f:
		w = csv.writer(f)
		w.writerows(data)

