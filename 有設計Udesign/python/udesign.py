# -*- coding: utf-8 -*-
# uDesign https://udesign.udnfunlife.com/mall/Cc1a00.do
import requests
from bs4 import BeautifulSoup
import json
import csv



data = []
data.append(["Brand"])

# url = "http://udesign.udnfunlife.com/mall/cus/gbr/Cc1g02.do"
# res = requests.get(url)
# # print res.text.encode("utf-8")
# soup = BeautifulSoup(res.text, "lxml")

# 品牌一覽首頁
# for i in soup.select(".page--filterContent")[0].select(".brandBox"):
# 	# print i
# 	country = str(i.select(".location")[0])
# 	print country
# 	if "台灣" not in country:
# 		continue
# 	name = i.select(".name")[0].text.encode("utf-8")
# 	print name

page = 1
brands = set()
while True:	
	url = "http://udesign.udnfunlife.com/mall/cus/gbr/Cc1g02.do?dc_btn_0=Func_Brand_Search&dc_page_0=" + str(page)
	print url

	res = requests.get(url)
	js = json.loads(res.text)
	
	if js["HasNext"] != True:
		break
	
	for i in js["BrandDesignList"]:
		if "台灣" not in i["Ctry"].encode("utf-8"):
			continue

		brand = i["Chinm"].encode("big5", "ignore")
		if brand in brands:
			continue

		brands.add(brand)
		data.append([brand])
		print i["Chinm"].encode("utf-8", "ignore")

	page = page + 1


with open("udesign.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

print "DONE!"










