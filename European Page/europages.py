# -*- coding: utf-8 -*-
# B2B廠商找尋網站
#EUROPAGES http://www.europages.co.uk/business-directory-europe.html 台灣廠商名單
from bs4 import BeautifulSoup
import requests
import csv


url = "http://www.europages.co.uk/business-directory-europe.html"
res = requests.get(url)
soup = BeautifulSoup(res.text, "lxml")


data = []
data.append(["category", "company", "tel"])

duplicate = set()

for i in soup.select(".theme-title"):
	# 若該分類未抓取
	if i.text.encode("utf-8").strip() not in duplicate:
		duplicate.add(i.text.encode("utf-8").strip())

		category = i.text.encode("utf-8").strip()
		category_url = i.select("a")[0]["href"]
		print category
		print category_url

		category_res = requests.get(category_url)
		category_soup = BeautifulSoup(category_res.text, "lxml")

		check_code = ""
		# 抓取每個大分類中的小分類碼
		for check in category_soup.select(".check"):
			check_code =  check_code + check["value"] + ";"
		# print check_code


		page = 0
		# 
		while True:
			page += 1
			category_url_page = (category_url + "/companies/Taiwan%20R.O.C./pg-" + str(page) + "/results.html?ih=" + check_code )[:-1]
			
			category_res = requests.get(category_url_page)
			# 該頁不存在則跳出while
			if category_res.status_code == 410:
				break

			print category, page, category_url_page
			category_soup = BeautifulSoup(category_res.text, "lxml")

			# 該分類沒有台灣公司則跳出迴圈
			if len(category_soup.select(".main-title")) == 0:
				break
			
			# 抓取每間公司的資訊
			for j in category_soup.select(".main-title"):
				comp = j.text.encode("utf-8").strip()
				comp_url = j.select("a")[0]["href"]
				print comp_url
				comp_res = requests.get(comp_url)
				comp_soup = BeautifulSoup(comp_res.text, "lxml")
	
				# url = comp_soup.select(".compUrl")[0]
				if len(comp_soup.select(".info-tel-num")) != 0:
					tel = comp_soup.select(".info-tel-num")[0].text.encode("utf-8")
				else:
					tel = ""
				data.append([category, comp, tel])

			



# save file
with open("europages.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)




