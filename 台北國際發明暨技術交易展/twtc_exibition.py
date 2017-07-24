# -*- coding: utf-8 -*-
#2017台北國際發明暨技術交易展
from bs4 import BeautifulSoup
import requests
import math
import csv
import glob


data = []
data.append(["company", "company_en", "brand", "products", "position"])
exhibition = "taipeiampa"

url = "https://www.inventaipei.com.tw/zh_TW/exh/search.html?mainCategory=&subCategory=&condition=&sortBy=&currentPage=1&pageSize=100&currentShowYear=2017&country=&subject=&exhBrandName=&exhMainProduct=&searchMode=NORMAL&type=exhibitor"

res = requests.get(url)
# print res.text.encode("utf-8")

soup = BeautifulSoup(res.text, "html.parser")

pages = int(math.ceil(int(soup.select(".Total")[0].select("em")[0].text)/100.0))


for page in range(pages):
	url = "https://www.inventaipei.com.tw/zh_TW/exh/search.html?mainCategory=&subCategory=&condition=&sortBy=&currentPage=" + str(page+1) + "&pageSize=100&currentShowYear=2017&country=&subject=&exhBrandName=&exhMainProduct=&searchMode=NORMAL&type=exhibitor"
	res = requests.get(url)
	print res

	soup = BeautifulSoup(res.text, "html.parser")
	for i in soup.select(".checkbox"):
		row = []
		company = i.select("h3")[0].text.encode(res.encoding)
		company_en = i.select(".ENname")[0].text.encode(res.encoding)
		company = company.replace(company_en, "")
		if company == "":
			company = company_en
		brand = i.select("p")[0].text.encode(res.encoding).replace("品牌名稱：", "")
		items = i.select("p")[1].text.encode(res.encoding).replace("主要產品：", "")
		position = i.select("p")[2].text.encode(res.encoding).replace("攤位號碼:", "")
		
		d = [company, company_en, brand, items, position]
		for r in d:
			#print r
			row.append(r.decode("utf-8", "ignore").encode("big5", "ignore"))
		data.append(row)
	
with open("invention.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)



print exhibition + " is done!"


