# -*- coding: utf-8 -*-
#
from bs4 import BeautifulSoup
import requests
import csv
import math




last_comany = ""

address = []
with open("2.csv", "r") as f:
	
	reader = csv.reader(f, delimiter = ",")

	for i in reader:
		address.append(i[2]) 

print address



for add in address[1:]:
	data = []
	data.append(["company"])
	
	
	url = "https://" + add + "/zh_TW/exh/show/prefix/list.html?currentPage=1"
	print url
	
	res = requests.get(url)
	# print res.text.encode("utf-8")
	soup = BeautifulSoup(res.text, "html.parser")
	
	page = int(math.ceil(int(soup.select(".Total")[0].select("em")[0].text)/10.0))

	print page
	
	for i in range(page):
		print i+1
	
		url = "https://" + add + "/zh_TW/exh/show/prefix/list.html?currentPage=" + str(i+1)
		res = requests.get(url)
		soup = BeautifulSoup(res.text, "html.parser")
	
		for box in soup.select(".checkbox-info"):
			
			company_name = box.select(".ENname")[0].text.encode("big5", "ignore")
			company = box.select("a")[1].text.encode("big5", "ignore").replace(company_name, "")
			print company
	
	
			data.append([company])
	
	with open(add.split(".")[1] + ".csv", "wb") as f:
		w = csv.writer(f)
		w.writerows(data)
