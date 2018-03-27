# -*- coding: utf-8 -*-
# http://www.taiwantea.org.tw/ 台灣區製茶工業同業公會
from bs4 import BeautifulSoup
import requests
import csv



data = []
data.append(["company"])

first = ""

for review in ["today", "reply"]:
	page = 1
	while True:
		url = "http://www.taiwantea.org.tw/Member.asp?page=" + str(page) + "&Review=" + review
		print url
		res = requests.get(url)
		soup = BeautifulSoup(res.text, "lxml")
		
		for i in range(12):
			try:
				comp = soup.select("table")[-(i+3)].select("font")[0]			
			except:
				print "here"
				break
			
			try:
				comp = comp.select("a")[0].text.encode(res.encoding, "ignore")		
			except:
				comp = comp.text.encode(res.encoding, "ignore")[18:].strip()		
			finally:
				if comp == first:
					break
				if i == 0:
					first = comp
	
				data.append([comp])
				
				# comps.add(comp)
		
		if comp == first:
			break
		page += 1




with open("taiwantea.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)


