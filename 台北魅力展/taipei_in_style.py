# -*- coding: utf-8 -*-
# 爬取 Taipei in Style 2016, 2015 參展廠商
# http://www.taipeiinstyle.com/new/brands/Brands_cht.asp
from bs4 import BeautifulSoup
import requests
import csv





s = requests.Session()



for year in ["2016", "2015"]:
	page = 0
	data = []

	while True:

		page = page + 1
		print page
		url = "http://www.taipeiinstyle.com/new/brands/Brands_cht.asp?page=" + str(page) + "&ProductsAreaMainNo=0&Sort=ChineseCompany,ASC&ViewType=first&ProductsAreaSubNo=&SubPageName=Brands&DataYear=" + year
		headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"}
		res = s.get(url, headers = headers)
		# print res
		soup = BeautifulSoup(res.text, "html.parser")
	
	
		if str(page) != soup.select(".PapeNow")[0].select("div")[0].text:
			print page
			break
	
		for i in soup.select(".galleryInfo"):
			data.append([i.text.encode(res.encoding).decode("utf-8").encode("big5", "ignore")])
	
	
	with open("taipeiinstyle_"+ year +".csv", "ab") as f:
		w = csv.writer(f)
		w.writerows(data)
