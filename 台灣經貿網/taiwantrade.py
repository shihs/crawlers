# -*- coding: utf-8 -*-
# 爬取台灣經貿網所有商品的供應商名單https://tw.taiwantrade.com/
from bs4 import BeautifulSoup
import requests
import csv
import math
import time
import sys


# 所有商品分類
url = "https://tw.taiwantrade.com/categories-view/all-category.html"

res = requests.get(url)
soup = BeautifulSoup(res.text, "lxml")
category = soup.select(".grpTitle")

data_dic = {}

count = 0
cg_count = 1

print "There are " + str(len(category)) + " categories."


# 各商品類別分別爬取
for i in category:

	while True:
		try:
			# 類別名稱
			cg = i.text.encode("big5", "ignore")
			print cg		

			url = "https://tw.taiwantrade.com/" + i.select("a")[0]["href"]
			#url = url.replace("Gallery", "Supplier")
			res = requests.get(url)
			soup = BeautifulSoup(res.text, "lxml")

			# 該分類公司數
			try:
				link = str(soup.select(".link")[1])
			except:
				break
			start = link.find("(")
			number = link[start+1:link.find(")")]
			# 計算頁數
			page = int(math.ceil(int(number)/20.0))
		
			print "There are " + number + " companies."
			
			# 每頁20筆，依序爬取
			for p in range(page):
				url = "https://tw.taiwantrade.com/products/search?word=*&cate=" + i.select("a")[0]["href"][-22:-17] + "&type=product&mode=1&page=" + str(p+1) + "&style=supplier"
				print cg_count, cg, url
		
				while True:
					try:
						res = requests.get(url, timeout = 60)
					except Exception as e:
						print e
						time.sleep(15)
					break
		
				soup = BeautifulSoup(res.text, "lxml")
			
				companies = soup.select(".listTitle")
			
				# 公司基本資料頁面
				for j in companies:
		
					count += 1
		
					company = j.select("a")[0].text.encode("big5", "ignore")
					
					if company in data_dic.keys():
						continue
		
					data_dic[company] = {}
					data_dic[company]["category"] = cg
					company_url = j.select("a")[0]["href"]
					
					# 兩種不同的公司基本資料頁面形式
					if "taiwantrade" in company_url:
						company_url = company_url + "/about-us"
			
					else:
						company_url = "https://tw.taiwantrade.com" + company_url
			
					print cg_count, cg, count, company_url
		
					try:
						company_res = requests.get(company_url, timeout = 60)
					except Exception as e:
						print e
						time.sleep(10)
					
					try:
						company_soup = BeautifulSoup(company_res.text, "lxml")
						# info = company_soup.select("#basicInformation")[0].select(".specBrief")[0]
						info = company_soup.select(".specBrief")[0]
						
						# 公司基本資訊
						for k in info.select(".item"):
							data_dic[company][k.select("em")[0].text.encode("big5", "ignore").replace(":", "").strip()] = k.select("strong")[0].text.encode("big5", "ignore")
					except Exception as e:
						print e
						continue


			cg_count += 1

	
		except Exception as e:
			print e
			exc_type, exc_obj, exc_tb = sys.exc_info()
			print(exc_type, exc_tb.tb_lineno)
			time.sleep(10)
			
			continue
	
		print "there are " + str(count) + "companies"	
		break

	





#欄位名稱
#儲存欄位名稱
colname = set()
for i in data_dic.keys():  # 公司名稱
	for j in data_dic[i].keys():  # 每間公司的欄位
		colname.add(j)

# 補齊沒有的欄位
for i in data_dic.keys():  # 公司名稱
	for j in colname: 
		if j not in data_dic[i].keys():
			data_dic[i][j] = ""


print "Saving data......"

# 儲存資料
data = []
# 欄位名稱
colname = list(colname)
colname.sort()
data.append(colname)
# 填入資料
for i in data_dic.keys():
	row = []
	for j in colname:
		row.append(data_dic[i][j])
	data.append(row)


print "Saving file......"

with open("taiwantrade.csv", "ab") as f:
	w = csv.writer(f)
	w.writerows(data)


print "DONE!"