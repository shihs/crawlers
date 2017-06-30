# -*- coding: utf-8 -*-
#台灣科學園區科學工業同業公會 http://www.asip.org.tw/com_n.php
from bs4 import BeautifulSoup
import requests
import csv
import urllib



data = []
data.append(["GUI", "company", "company_en", "address", "tel", "industry"])
page = 0

while True:
	
	url = "http://www.asip.org.tw/com_n.php?pageNum_reComList=" + str(page)
	print url
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "lxml")

	if soup.select("#mcCenter_cont3")[0].select("table")[2].text.strip() == "":
		break
	
	for i in soup.select("#mcCenter_cont3")[0].select("table")[2].select("tr"):
		company = i.select("a")[0].text.encode("utf-8")
		company_en = i.select("div")[0].text.encode("utf-8")
		industry = i.select("td")[1].text.encode("utf-8")
		com_id = i.select("a")[0]["onclick"].replace("window.open('com/outinfo.php?id=", "").replace("','','width=600,height=680,scrollbars=yes,toolbar=no')", "")
		print company, company_en, industry, com_id
	
		company_url = "http://www.asip.org.tw/com/outinfo.php?id=" + com_id
		company_res = requests.get(company_url)
		company_soup = BeautifulSoup(company_res.text, "lxml")
	
		GUI = company_soup.select("tr")[3].select("td")[1].text.encode("utf-8")
		address = company_soup.select("tr")[4].select("td")[1].text.encode("utf-8").replace("郵遞區號：", "").replace("科學園區：", "").replace("地址(中)：", "").replace(" ", "").replace("\n", "")
		tel = company_soup.select("tr")[6].select("td")[1].text.encode("utf-8").replace("-", "")
		#print GUI, address, tel
	
		row = [GUI, company, company_en, address, tel, industry]
	
		for j in range(len(row)):
			row[j] = row[j].decode("utf-8").encode("big5", "ignore")
	
	
		data.append(row)
	# break
	page += 1


with open("asip.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

