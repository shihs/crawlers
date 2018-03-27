# -*- coding: utf-8 -*-
# 台灣台灣精品得獎廠商
from bs4 import BeautifulSoup
import requests
import time
import csv
import random



company_set = set()

data = []
data.append(["company", "year", "tel1", "tel2"])



page = 1
while True:
	url = "https://www.taiwanexcellence.org/tw/award/product/result?page=" + str(page)
	print url
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "lxml")
	
	if len(soup.select(".item-list")[0].select("a")) == 0:
		break
	for i in soup.select(".item-list")[0].select("a"):
		row = []
		company = i.select(".company")[0].text.encode("big5", "ignore")
		if company in company_set:
			continue
	
		company_set.add(company)
		print company	
		product_url = i["href"]
		product_res = requests.get(product_url)
		product_soup = BeautifulSoup(product_res.text, "lxml")
		year = product_soup.select(".award")[0].select("img")[0]["src"][67:71]

		row.extend([company, year])

		for info in product_soup.select("#contact")[0].select("p"):
			if "公司電話：" in info.text.encode("utf-8"):
				# print info.select("a")[0].text.encode("utf-8")
				row.append(info.select("a")[0].text.encode("big5", "ignore"))
		data.append(row)
		# print 
		# print product_soup.select("#contact")[0].select("a")[0].text.encode("utf-8")
	
	page += 1



with open("taiwanexcellence.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

