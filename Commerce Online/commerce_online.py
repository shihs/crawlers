# -*- coding: utf-8 -*-
#抓取commerce online所有商家http://tw.commerce.com.tw/manufacturer/0/company.htm
from bs4 import BeautifulSoup
import requests
import csv
import time
import math
import os

data = []

target = "commerce_online.csv"

if not os.path.exists(target):
	print "here"
	data.append(["company", "country", "tel"])


#all category page
url = "http://tw.commerce.com.tw/manufacturer/0/company.htm"

res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")

#each category
for i in soup.select("table")[13].select("a")[1:]:
	# print i.text.encode(res.encoding)
	# print i
	href = i["href"]

	#find the url of each category
	if href.find("manufacturer") != -1:
		pos_number = href.find("/", 14)
		cg_number = href[14:pos_number]
		cg_name = href[pos_number:]
		
		#每個分類的網址
		url_category = "http://tw.commerce.com.tw/manufacturer/" + cg_number + cg_name
		print url_category

		res_category = requests.get(url_category)		
		soup_category = BeautifulSoup(res_category.text, "html.parser")

		#company amount
		amount = soup_category.select("table")[13].select("tr")[0].text
		amount = int(amount[amount.find("(")+1:amount.find(")")])
		page = int(math.ceil(amount/20.0))
		# print amount, page

		#each page
		for p in range(page):
			print (p + 1)
			#第二頁之後
			if p != 0:
				url_category = "http://tw.commerce.com.tw/manufacturer/" + cg_number + "p" + str(p+1) + cg_name
				print url_category
				res_category = requests.get(url_category)
				soup_category = BeautifulSoup(res_category.text, "html.parser")

			#each company
			for j in soup_category.select("table")[18:]:
				try:
					if len(j.select("table")) != 0:
						img = j.select("img")
						# print img
						continue
		
					#company tag
					a = j.select("a")
					if len(a) != 2:
						break
					
					#check if is TW company
					if a[0].select("b")[0].text.strip() not in ["", "TW"]:
						continue

					company = a[1]

					#company name
					name_company = company.text.encode(res.encoding, "ignore").decode("utf-8", "ignore").encode("big5", "ignore").strip()
					# print name_company
					
					#url of company
					url_company = "http://tw.commerce.com.tw" + company["href"]
					print url_company
			
					res_company = requests.get(url_company)
					soup_company = BeautifulSoup(res_company.text, "html.parser")
					
					#company info page tag
					try:
						#free member
						if len(img) == 0:
							tel = soup_company.select("table")[17].select("tr")[3].select("td")[1].text.encode(res_company.encoding).decode("utf-8", "ignore").encode("big5", "ignore")
							country = soup_company.select("table")[17].select("tr")[5].select("td")[1].text.encode(res_company.encoding).decode("utf-8", "ignore").encode("big5", "ignore")
			
						#platinum member
						elif img[0]["src"] == "/pic2002/b001.gif":
							info = soup_company.select(".info-list")[2].select(".info-list")
							#tel of company
							tel = info[5].text.encode(res.encoding).decode("utf-8", "ignore").encode("big5", "ignore").strip()
							#nation of company
							country = info[9].text.encode(res.encoding).decode("utf-8", "ignore").encode("big5", "ignore").strip()
			
						#gold/ silver member
						else:
							tel = soup_company.select("table")[16].select("tr")[3].select("td")[1].text.encode(res_company.encoding).decode("utf-8", "ignore").encode("big5", "ignore")
							country = soup_company.select("table")[16].select("tr")[5].select("td")[1].text.encode(res_company.encoding).decode("utf-8", "ignore").encode("big5", "ignore")			
			
					except:
						tel = ""
						country = ""
		
					# print name_company
					print tel, country
		
					data.append([name_company, country, tel])
	
				except Exception as e:
					print "something wrong"
					print e
					with open(target, "ab") as f:
						w = csv.writer(f)
						w.writerows(data)
		
					continue
	# 		break
	# break


with open(target, "ab") as f:
	w = csv.writer(f)
	w.writerows(data)

print "DONE!"
