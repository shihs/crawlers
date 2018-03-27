# -*- coding: utf-8 -*-
# http://tzma.industry.org.tw 台灣拉鍊工業同業公會
from bs4 import BeautifulSoup
import requests
import csv






data = []
data.append(["company", "contact person", "tel"])

s = requests.Session()

url = "http://tzma.industry.org.tw/Memberbook/Memberbook.asp"
s.get(url)


for page in range(1, 4):
	print page

	url = "http://tzma.industry.org.tw/Memberbook/Member_Search.asp"
	
	payload = {
		"page_list":str(page),
		"page_count":"3",
		"now_page":str(page),
		"company_name":"",
		"product":"",
		"company_add":"",
		"search_method":""
	}
	
	
	
	res = s.post(url, data = payload)
	# print res.text.encode("utf-8")
	soup = BeautifulSoup(res.text, "lxml")
	
	for i in soup.select(".smooth9")[1].select("a"):
		comp_url = "http://tzma.industry.org.tw/Memberbook/Company_Data.asp?sid=" + str(i)[34:38]
		print comp_url
		comp_res = requests.get(comp_url)
		comp_soup = BeautifulSoup(comp_res.text, "lxml")
		
		comp = comp_soup.select("tr")[5].select("td")[1].text.encode(comp_res.encoding, "ignore")
		contact_person = comp_soup.select("tr")[8].select("td")[1].text.encode(comp_res.encoding, "ignore")
		tel = comp_soup.select("tr")[11].select("td")[1].text.encode(comp_res.encoding, "ignore")
	
		data.append([comp, contact_person, tel])
	

with open("tzma.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)


