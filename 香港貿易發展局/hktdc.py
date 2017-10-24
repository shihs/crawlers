# -*- coding: utf-8 -*-
# 爬取 HKTDC貿發網 http://www.hktdc.com/asian-suppliers-listing/
from bs4 import BeautifulSoup
import requests
import csv
import time




data = []
data.append(["company"])

url = "http://www.hktdc.com/asian-suppliers-listing/"

res = requests.get(url)
soup = BeautifulSoup(res.text, "lxml")

company = set()

for i in soup.select(".link_black_middle"):
	if "Taiwan" in i.text.encode("utf-8"):
		category_url = i["href"].replace("/1/", "")
		print category_url

		if "http" not in category_url:
			break

		page = 0
		while True:
			page += 1
			category_res = requests.get(category_url + "/" + str(page) + "/")
			category_soup = BeautifulSoup(category_res.text, "lxml")
			
			if len(category_soup.select(".content_black_large_bold")) != 0:
				break

			for i in category_soup.select(".padding_bottom_5px"):
				if len(i.select(".link_black_middle_bold")) != 0:
					comp = i.select(".link_black_middle_bold")[0].text.encode("utf-8").strip()
					print comp
					company.add(comp)

time.sleep(10)


page = 0
while True:
	page += 1
	url = "http://www.hktdc.com/products-suppliers/Taiwan-Suppliers/en/31/" + str(page) +"/"
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "lxml")

	if len(soup.select(".content_black_large_bold")) != 0:
		break
	 
	for i in soup.select(".word-wrap"):
		comp = i.select(".link_red_middle_bold")[0].text.encode("utf-8").strip()
		company.add(comp)



company = list(company)

for d in company:
	data.append([d])




with open("hktdc.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)


