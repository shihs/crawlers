# -*- coding: utf-8 -*-
# 爬取 台灣區毛紡織工業同業公會 www.wool.org.tw
from bs4 import BeautifulSoup
import requests
import csv



data = []
data.append(["company", "tel"])


s = requests.Session()

url = "http://www.wool.org.tw/member.aspx"
res = s.get(url)
res = requests.get(url)
soup = BeautifulSoup(res.text, "lxml")

for i in soup.select("#gv_list")[0].select("tr")[3:]:
	comp = i.select("td")[0].text.encode("big5", "ignore")
	tel = i.select("td")[2].text.encode("big5", "ignore")
	# print comp, tel
	data.append([comp, tel])





for page in range(2, 7):
	print page

	VIEWSTATE = soup.select("#__VIEWSTATE")[0]["value"]
	EVENTVALIDATION = soup.select("#__EVENTVALIDATION")[0]["value"]

	payload = {
		"__EVENTTARGET":"gv_list",
		"__EVENTARGUMENT":"Page$" + str(page),
		"__VIEWSTATE":VIEWSTATE,
		"__EVENTVALIDATION":EVENTVALIDATION
	}
	
	
	res = s.post(url, data = payload)
	soup = BeautifulSoup(res.text, "lxml")
	
	for i in soup.select("#gv_list")[0].select("tr")[3:]:
		comp = i.select("td")[0].text.encode("big5", "ignore")
		tel = i.select("td")[2].text.encode("big5", "ignore")
		# print comp, tel
		data.append([comp, tel])


with open("wool.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

print "DONE!"	

