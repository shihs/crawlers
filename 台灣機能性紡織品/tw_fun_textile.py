# -*- coding: utf-8 -*-
# 爬取 台灣機能性紡織品 廠商名單 http://tft.ttfapproved.org.tw/en/index.asp
from bs4 import BeautifulSoup
import requests
import csv
import time


comps = set()

data = []
data.append(["company", "tel"])

for page in range(21):
	url = "http://tft.ttfapproved.org.tw/en/product_search_c/search-list.asp?func=query&page=" + str(page+1)
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "lxml")
	
	n = (len(soup.select(".style21"))/3)
	print n
	
	count = 1
	for i in range(n):
		comp = soup.select(".style21")[i*3].text.encode("utf-8").strip()
		if comp in comps or comp == "N/A":
			continue
	
		comps.add(comp)
		# code = soup.select(".style21")[i*3+1].text.encode("utf-8").strip()
		# print comp, code
	
		url = "http://tft.ttfapproved.org.tw/en/product_search_c/show_detail.asp?approved_ok_no=" + soup.select(".style21")[i*3+1].text.encode("utf-8").strip()
	
		comp_res = requests.get(url)
		comp_soup = BeautifulSoup(comp_res.text, "lxml")
	
		tel = comp_soup.select(".a12pt")[2].select("td")[3].text.encode("utf-8")
	
		data.append([comp, tel])

	time.sleep(3)



with open("tw_fun_textile.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

print "DONE!"


