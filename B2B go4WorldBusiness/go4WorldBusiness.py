# -*- coding: utf-8 -*-
# 爬取 go4WorldBusiness台灣廠商名單 https://www.go4worldbusiness.com/ 
from bs4 import BeautifulSoup
import requests
import csv
import time
import random



data = []
data.append(["company", "tel"])

comps = set()
try_time = 0

url = "https://www.go4worldbusiness.com/browse/Taiwan/members.html"
res = requests.get(url, timeout = 30)
soup = BeautifulSoup(res.text, "lxml")

print "There are " + str(len(soup.select(".col-md-6")[1:])) + " categories need to crawl."

cag_num = 1
for i in soup.select(".col-md-6")[1:]:
	print cag_num
	cag_num += 1

	page = 0
	while True:
		cag = i.select("a")[0]["href"]
		# print cag
		cag_url = "https://www.go4worldbusiness.com/find?searchText=" + cag[(cag.find("Taiwan/")+7):cag.find(".html")] + "&countryFilter%5B0%5D=Taiwan&pg_buyers=1&pg_suppliers=" + str(page+1) + "&_format=html&BuyersOrSuppliers=suppliers"
		print cag_url
		page += 1

		try:	
			cag_res = requests.get(cag_url, timeout = 30)
			cag_soup = BeautifulSoup(cag_res.text, "lxml")
		except:
			with open("go4worldbusiness.csv", "ab") as f:
				w = csv.writer(f)
				w.writerows(data)
			data = []
			try_time += 1
			if try_time == 10:
				break
			timp.sleep(60)

		if len(cag_soup.select(".mar-top-30")) != 0:
			break
		
		for j in cag_soup.select(".underline-none"):
			comp_url = j["href"]
			if "member" not in comp_url:
				continue
	
			comp = j.text.encode("utf-8", "ignore").strip()
			if comp in comps:
				continue
	
			comps.add(comp)
	
			comp_url = "https://www.go4worldbusiness.com" + comp_url
			try:
				comp_res = requests.get(comp_url, timeout = 30)
				comp_soup = BeautifulSoup(comp_res.text, "lxml")
			except:
				with open("go4worldbusiness.csv", "ab") as f:
					w = csv.writer(f)
					w.writerows(data)
				data = []
				try_time += 1
				if try_time == 10:
					break
				timp.sleep(60)

			
			if len(comp_soup.select("address")) != 0:
				tel = comp_soup.select("address")[0].text.encode("utf-8", "ignore")
				if tel.find("Phone:") == -1:
					tel = ""
				elif tel.find("Fax:") == -1:
					tel = tel[tel.find("Phone:")+6:tel.find("Phone:")+6+14].strip()
				else:
					tel = tel[tel.find("Phone:")+6:tel.find("Fax:")].strip()
			else:
				tel = ""
			# print tel

			data.append([comp, tel])
			
		
			# break
		time.sleep(0.3)
		# break
	# break
	
	

with open("go4worldbusiness.csv", "ab") as f:
	w = csv.writer(f)
	w.writerows(data)

print "DONE!"

