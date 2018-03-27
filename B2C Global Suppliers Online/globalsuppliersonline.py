# -*- coding: utf-8 -*-
# http://www.globalsuppliersonline.com/ B2B台 灣廠商
from bs4 import BeautifulSoup
import requests
import csv
import time
# import urllib





comps = set()

url = "http://www.globalsuppliersonline.com/Taiwan"
res = requests.get(url)
soup = BeautifulSoup(res.text, "lxml")




for i in soup.select(".smaller")[4:(4+26)]:
	# print i
	for j in i.select("a")[1:3]:
		page = 1
		while True:
			#category_url = url + "/" + j.text#.encode("utf-8")
			category_url = "http://www.globalsuppliersonline.com/search/results.asp?txtsrch=" + j.text + "&match=HJHGgfjHKJhjht&cntry=207&order=&pgno=" + str(page)
			print category_url
			category_res = requests.get(category_url)
			category_soup = BeautifulSoup(category_res.text, "lxml")
			
			
			if len(category_soup.select(".rowblue")) == 0:
				break 
			for k in category_soup.select(".tablblue")[1].select(".normal"):
				try:
					comp = k.select("b")[0].text.encode("utf-8")
					print comp
					comps.add(comp)
				except:
					continue


			if len(category_soup.select(".tablblue")[1].select(".smaller")[-2].select("strong")[2].select("a")) == 0:
				break

			page += 1


		time.sleep(2)

	time.sleep(3)		



	# 	break
	# break




data = []
data.append(["company"])

for i in comps:
	data.append([i])

with open("globalsuppliersonline.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)


