# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import time
import csv




brands = set()

data = []
data.append(["Shop name", "Shop url", "Sales", "Shop owner", "Owner url"])

try_time = 1

page = 104
while True:
	print page
	url = "https://www.etsy.com/uk/c?order=most_relevant&use_mmx=1&explicit=1&locationQuery=1668284&page=" + str(page)
	
	res = requests.get(url)
	# print res.text.encode("utf-8")
	soup = BeautifulSoup(res.text, "lxml")
	
	if len(soup.select(".listing-link"))  == 0:
		time.sleep(90)
		if try_time == 5:
			break
		try_time = try_time + 1
		continue

	for i in soup.select(".listing-link"):

		product_brand = i.select(".text-gray-lighter")[0].text.encode("utf-8").strip()
		
		if product_brand in brands:
			continue
		
		brands.add(product_brand)
		product_url = i["href"]
		print product_brand
		# print product_url
	
		product_res = requests.get(product_url)
		product_soup = BeautifulSoup(product_res.text, "lxml")
	
		shop_url = product_soup.select(".shop-name")[0].select("a")[0]["href"]
		print shop_url
	
		# time.sleep(1)
		shop_res = requests.get(shop_url)
		shop_soup = BeautifulSoup(shop_res.text, "lxml")
	
		sales = shop_soup.select(".mr-xs-2")[1].text.encode("utf-8").replace(" Sales", "")
		shop_owner = shop_soup.select(".shop-owner")[0]
		owner = shop_owner.select("p")[0].text.encode("utf-8")
		owner_url = "https://www.etsy.com" + shop_owner.select("a")[0]["href"]
		# print owner
		# print owner_url
		
	
		data.append([product_brand, shop_url, sales, owner, owner_url])
		time.sleep(1)
	
		# break
	# break

	page = page + 1

with open("esty_2.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

