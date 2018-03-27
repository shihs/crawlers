# -*- coding: utf-8 -*-
# 天下雜誌2016 2000大企業名單http://issue.cw.com.tw/ipad/201605_2000/list.jsp
from bs4 import BeautifulSoup
import requests
import csv



industry_dic = {"A":"製造業", "B":"服務業", "C":"金融業"}

data = []
data.append(["industry1", "industry2", "company"])

for industry1 in ["A", "B", "C"]:
	url = "http://issue.cw.com.tw/ipad/201605_2000/list.jsp?orders=SER&sort=asc&inds=" + industry1 + "&start=0"
	res = requests.get(url)

	soup = BeautifulSoup(res.text, "lxml")
	
	page = soup.select("#pageMenu")[0].text.encode("utf-8").strip()
	begin = page.find("共".decode("utf-8").encode("utf-8"), 5)
	end = page.find(".", begin)
	
	pages = int(page[(begin+3):end])

	count = 0
	for page in range(pages):
		count = count + 1
		# if count == 2:
		# 	break
		url_page = url = "http://issue.cw.com.tw/ipad/201605_2000/list.jsp?orders=SER&sort=asc&inds=" + industry1 + "&start=" + str(page*10)
		res = requests.get(url_page)
		soup = BeautifulSoup(res.text, "lxml")
		table = soup.select(".datetable01")[0].select("tr")

		for tr in table[2:]:
			company = tr.select(".td_name")[0].text.encode("big5", "ignore")
			industry2 = tr.select(".td_l")[0].text.encode("big5", "ignore")
			# print company, industry
			data.append([industry_dic[industry1].decode("utf-8").encode("big5"), industry2, company])

		print "There are " + str(count) + " is done!"


with open("cw_magazine_2016.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

