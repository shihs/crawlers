# -*- coding: utf-8 -*-
#
from bs4 import BeautifulSoup
import requests
import csv




last_comany = ""

address = []
with open("1.csv", "r") as f:
	 # address.append(f.readlines()[2])
	
	reader = csv.reader(f, delimiter = ",")

	for i in reader:
		address.append(i[2].split(":")[1]) 

print address


# for add in address:
for add in ['//www.autotaiwan.com.tw/']:
	print add
	data = []
	# data.append(["company", "area"])
	data.append(["company"])

	page = 0
	while True:
		page += 1
		print page
		url = "https:" + add + "visitorExhibitor.asp?page=" + str(page) + "&Area="
		print url

		headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"}

		res = requests.get(url, timeout = 30, headers = headers)
		soup = BeautifulSoup(res.text, "lxml")
		
		product = soup.select("#product")[0]
	
	
		if product.select("li")[-1] == last_comany:
			break
	
		for i in product.select("li"):
			try:
				right = i.select(".right")[0]
				company = right.select("a")[0].text.encode(res.encoding).decode("utf-8", "ignore").encode("big5", "ignore")
				#area = right.select("p")[1].select("a")[0].text.encode(res.encoding).decode("utf-8", "ignore").encode("big5", "ignore")
			
			except:
				continue
	
			# data.append([company, area])
			data.append([company])
	
		last_comany = product.select("li")[-1]
	


		print str(page) + " is done!"
		
	with open(add.split(".")[1] + ".csv", "wb") as f:
		w = csv.writer(f)
		w.writerows(data)




