# -*- coding:utf-8 -*-
# 爬取 台灣自行車導覽(TBS)名單http://www.wheelgiant.com.tw/publication/tbs/qry_name.asp
import requests
from bs4 import BeautifulSoup
import csv
import string




data = []
data.append(["company", "company_en", "boss", "contact person", "exhibition date", "employees", "tel", "fax", "address", "web", "email", "sub"])


for alpha in string.ascii_uppercase:
	
	url = "http://www.wheelgiant.com.tw/publication/tbs/sup_list.asp?type=name&para1=" + alpha
	
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "lxml")
	
	for i in soup.select(".style39"):
		
		sup = i.select("a")[0]["href"][17:23]
	
		comp_url = "http://www.wheelgiant.com.tw/publication/tbs/sup_data.asp?type=name&para1=" + alpha + "&sup=" + sup
		print comp_url
	
		comp_res = requests.get(comp_url)
		comp_soup = BeautifulSoup(comp_res.text, "lxml")
		
		row = []

		info = comp_soup.select("#Layer2")[0]	
	
		company = info.select(".style37")[0].text.encode(comp_res.encoding, "ignore").decode("utf-8", "ignore").encode("big5", "ignore")
		row.append(company)
	
		company_en = info.select("tr")[3].text.encode(comp_res.encoding, "ignore").decode("utf-8", "ignore").encode("big5", "ignore")
		
		row.append(company_en)
		
		for i in info.select("tr")[4:14]:
			row.append('"' + i.select("td")[1].text.encode(comp_res.encoding, "ignore").decode("utf-8", "ignore").encode("big5", "ignore").strip() + '"')
	
		
		data.append(row)
		# break


	
with open("tbs.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)


