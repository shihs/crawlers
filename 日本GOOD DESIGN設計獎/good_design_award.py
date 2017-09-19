# -*- coding: utf-8 -*-
# 日本GOOD DESIGN AWARD台灣得獎名單
from bs4 import BeautifulSoup
import requests
import csv



s = requests.Session()

url = "http://www.g-mark.org/award/search?keyword=&from=&to=&prizeCode=&country=Taiwan&locale=zh_TW"
res = s.get(url)
soup = BeautifulSoup(res.text, "lxml")

data = []
data.append(["company", "product url", "category", "web"])

comp_set = set()
page = 0


token = soup.select("#more")[0].select("a")[0]["href"]
token = token[token.find("?token"):]

while True:
	page += 1
	# if page == 2:
	# 	break
	url = "http://www.g-mark.org/award/search/page/" + str(page) + token
	print url

	res = s.get(url)

	if res.status_code == 500:
		break
	soup = BeautifulSoup(res.text, "lxml")
	
	
	for i in soup.select(".yearArea"):
		print i["id"]
		print 
		for j in i.select("li"):
			product_url = "http://www.g-mark.org" + j.select("a")[0]["href"] + "&locale=zh_TW"
			print product_url
			product_res = requests.get(product_url)
			product_soup = BeautifulSoup(product_res.text, "lxml")
			

			company_info = product_soup.select(".basicinfo")[0]
			if "Company" in company_info.select("dt")[2].text.encode("utf-8"):
				company_info = company_info.select("dd")[2]
				comp = company_info.text.encode("utf-8").replace(" (Taiwan)", "").strip()
			else:
				company_info = company_info.select("dd")[3]
				comp = company_info.text.encode("utf-8").replace(" (Taiwan)", "").strip()

			
			if comp in comp_set:
				continue
	
			comp_set.add(comp)
	
			if len(company_info.select("a")) != 0:
				comp_url = company_info.select("a")[0]["href"]
			else:
				comp_url = ""	
	
			print comp
			category = product_soup.select(".basicinfo")[0].select(".type")[1].text.encode("utf-8").strip()
			
			data.append([comp, product_url, category, comp_url])
	




with open("good_design_award.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)


print "Finished"