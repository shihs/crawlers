# -*- coding: utf-8 -*-
# 鞋類暨運動休閒科技研發中心供應商
from bs4 import BeautifulSoup
import requests
import csv
import time



data = []
data.append(["company"])

comps = set()



for page in range(288):

	url = "http://www.bestmotion.com/book/Resaultp_eng.asp?MyQuery2=%20&MyQuery3=Taiwan&page=" + str(page+1)
	print url
	try:
		time.sleep(1)
		res = requests.get(url)	
		soup = BeautifulSoup(res.text, "lxml")

		for i in soup.select("center")[2].select("table")[1:-2]:
			if len(i.select("td")[0].select("font")) == 2:
				comp = i.select("font")[1].text.encode(res.encoding, "ignore").strip()
				if comp in comps:
					continue
		
				comps.add(comp)
				data.append([comp])
	except:
		print "oops!"
		continue
	
	


with open("bestmotion.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)
