# -*- coding: utf-8 -*-
# 爬取 台灣區絲織工業同業公會 http://www.filaweaving.org.tw/
from bs4 import BeautifulSoup
import requests
import csv




data = []
data.append(["company", "tel", "contact person"])


s = requests.Session()

url = "http://www.filaweaving.org.tw/members.aspx"
res = s.get(url)
# res = requests.get(url)
soup = BeautifulSoup(res.text, "lxml")

for i in soup.select("#gv_member")[0].select(".text_s1"):
	comp = i.select("a")[0].text.encode("big5", "ignore")
	tel = i.select("td")[1].text.encode("big5", "ignore")
	# print comp, tel
	comp_url = "http://www.filaweaving.org.tw/" + i.select("a")[0]["href"]
	# print comp_url

	comp_res = requests.get(comp_url)
	comp_soup = BeautifulSoup(comp_res.text, "lxml")
	contact_person = comp_soup.select(".for_td")[5].text.encode("big5", "ignore")
	# print contact_person

	data.append([comp, tel, contact_person])





for page in range(2, 15):
	print page

	VIEWSTATE = soup.select("#__VIEWSTATE")[0]["value"]
	EVENTVALIDATION = soup.select("#__EVENTVALIDATION")[0]["value"]

	payload = {
		"__EVENTTARGET":"gv_member",
		"__EVENTARGUMENT":"Page$" + str(page),
		"__VIEWSTATE":VIEWSTATE,
		"__EVENTVALIDATION":EVENTVALIDATION,
		"ddlist1":"請選擇"
	}
	
	
	res = s.post(url, data = payload)
	soup = BeautifulSoup(res.text, "lxml")
	
	for i in soup.select("#gv_member")[0].select(".text_s1"):
		print i.select("a")[0].text.encode("utf-8", "ignore")
		comp = i.select("a")[0].text.encode("big5", "ignore")
		tel = i.select("td")[1].text.encode("big5", "ignore")
		comp_url = "http://www.filaweaving.org.tw/" + i.select("a")[0]["href"]
	
		comp_res = requests.get(comp_url)
		comp_soup = BeautifulSoup(comp_res.text, "lxml")
		contact_person = comp_soup.select(".for_td")[5].text.encode("big5", "ignore")
	
		data.append([comp, tel, contact_person])


with open("filaweaving.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

print "DONE!"	


