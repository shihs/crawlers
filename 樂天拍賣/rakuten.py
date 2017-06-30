# -*- coding: utf-8 -*-
#抓取所有樂天拍賣的商家http://www.rakuten.com.tw/info/shopdirectory/?m-id=RADTop-Footer-Navi
from bs4 import BeautifulSoup
import requests
import csv
import time

data = []
data.append(["category", "company", "GUI", "boss", "shop_name", "shop_admin", "address", "tel"])

#所有商家列表
url = "http://www.rakuten.com.tw/info/shopdirectory/?m-id=RADTop-Footer-Navi"

res = requests.get(url)

soup = BeautifulSoup(res.text, "html.parser")
count = 0
#每個類別的商家
for i in soup.select(".ui-shop-category"):
	
	category = i.select("h2")[0].select("a")[0].text.encode("big5", "ignore")
	print  i.select("h2")[0].select("a")[0]

	#獲取每個商家網址
	for j in i.select(".category-content")[0].select("li"):
		shop_url = "http://www.rakuten.com.tw"+ j.select("a")[0]["href"] + "info/?l-id=tw_contactshop_shopinfo#Shipping"
		print shop_url	
		res = requests.get(shop_url)
		# print res.encoding
		soup = BeautifulSoup(res.text, "html.parser")
		row = []
		row.append(category)
		#商家資訊
		if len(soup.select(".b-table")) == 0:
			continue
		for k in soup.select(".b-table")[0].select("td")[0:7]:
			row.append(k.text.encode("big5", "ignore"))
		# print row
		count = count + 1
		print str(count) + " is done!" 

		data.append(row)
	# 	break
	# break
	time.sleep(30)



with open("rakuten.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)


print "finished"