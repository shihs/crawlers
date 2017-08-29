# -*- coding: utf-8 -*-
# 紅點設計名單
from bs4 import BeautifulSoup
import requests
import csv





data = []
data.append(["company", "url"])


count = 1
for year in ["2017", "2016", "2015", "2014", "2013", "2012", "2011"]:

	url = "http://red-dot.de/pd/online-exhibition/?lang=en&i=C&v=TW&y=" + year
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "lxml")
	
	for i in soup.select(".box"):
		#year = i.select(".work_container_search_year")[0].text.encode("utf-8")
		product_url = i.select(".work_container_img")[0].select("a")[0]["href"]
		#print i.text.encode("utf-8")
		product_res = requests.get(product_url)

		txt = product_res.text.encode("utf-8")
	
		product_soup = BeautifulSoup(product_res.text, "lxml")
	
		print count
		print product_url
	
		if len(product_soup.select(".role_content")[0].select("a")) == 0:
			continue
		comp = product_soup.select(".role_content")[0].select("a")[0].text.encode("utf-8")
	
		count = count + 1
	
		if len(product_soup.select(".onex_role_link")) != 0:
			comp_url = product_soup.select(".onex_role_link")[0].text.encode("utf-8")
		else:
			comp_url = ""
		
		#data.append([comp, comp_url, year, product_url])
		data.append([comp, comp_url])
		#break

	
with open("red_dot.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)
	
