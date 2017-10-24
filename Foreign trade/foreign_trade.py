# -*- coding: utf-8 -*-
# 爬取B2B FOREIGN TRADE廠商 https://www.foreign-trade.com/search.htm
from bs4 import BeautifulSoup
import requests
import csv
import time
import string



comps = set()

data = []
data.append(["company", "tel", "contact person"])

for alpha in list(string.ascii_lowercase):
	# print alpha
	page = 0
	first_comp = ""
	while True:
		page += 1
		url = "https://www.foreign-trade.com/search.htm?string=" + alpha + "&pstype=m&cnty=TW&page=" + str(page)
		

		try:
			res = requests.get(url, timeout=30)
			soup = BeautifulSoup(res.text, "lxml")
		except requests.ConnectionError:
			time.sleep(30)
			with open("foreign_trade.csv", "ab") as f:
				w = csv.writer(f)
				w.writerows(data)
				data = []

		
		# 若公司已爬取過表示已爬取完該字母關鍵字
		if first_comp == soup.select(".boldtext")[0].text.encode("utf-8", "ignore"):
			break
		print url
		first_comp = soup.select(".boldtext")[0].text.encode("utf-8", "ignore")

		# 公司
		for i in soup.select(".boldtext"):
			comp = i.text.encode("utf-8")

			# 若該公司已爬取過
			if comp in comps:
				continue
			comps.add(comp)

			tel = ""
			contact_person = ""

			try:
				if str(i).find("href") != -1:
					print comp
					comp_url = "https://www.foreign-trade.com" + i["href"]
					print comp_url
					comp_res = requests.get(comp_url)
					comp_soup = BeautifulSoup(comp_res.text, "lxml")
	
					if len(comp_soup.select(".table2")) != 0:
						tel = comp_soup.select(".table2")[0].select("tr")[2].select(".value2")[1].text.encode("utf-8", "ignore").strip()
						contact_person = comp_soup.select(".table2")[0].select("tr")[5].select(".value2")[0].text.encode("utf-8", "ignore").strip()
			except:
				with open("foreign_trade.csv", "ab") as f:
					w = csv.writer(f)
					w.writerows(data)
					data = []


	
			data.append([comp, tel, contact_person])
			time.sleep(1)
		#break


with open("foreign_trade.csv", "ab") as f:
	w = csv.writer(f)
	w.writerows(data)


print "DONE!"


