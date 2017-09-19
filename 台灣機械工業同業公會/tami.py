# -*- coding:utf-8 -*-
# 爬取台灣機械工業同業公會廠商名單http://www.tami.org.tw/trade.php 
import requests
from bs4 import BeautifulSoup
import csv
import zipfile




data = []
data.append(["large category", "small category", "company", "tel", "factory tel", "factory address"])

large_page = 0

while True:
	large_page += 1
	if large_page == 100:
		break

	# 產品大類，小類列表
	url = "http://www.tami.org.tw/category/p_list.php?on=" + str(large_page).zfill(2)
	print url
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "lxml")

	if len(soup.select(".product-link")) == 0:
		continue

	large_category = soup.select(".style27")[0].text.encode("big5", "ignore").strip()

	# 產品小類
	for i in soup.select(".product-link"):		
		# 分類名稱
		category = i.text.encode("big5", "ignore").replace(i["href"][-6:], "").strip()
		small_page = 0

		# 產品小類公司
		while True:
			small_page += 1
			category_url = "http://www.tami.org.tw/category/product4.php?on=" + str(small_page) + "&prod_sn=" + i["href"][-6:]
			print category_url
			category_res = requests.get(category_url)
			category_soup = BeautifulSoup(category_res.text, "lxml")

			# 若該頁沒有公司則跳下一分類
			if len(category_soup.select(".company-word3")) == 0:
				break

			# company information
			for j in range(1, len(category_soup.select(".company-word3")), 2):
				print j
				
				ms = category_soup.select(".company-word3")[j]["onclick"][-8:-3]
				# 公司基本資料網址
				comp_url = "http://www.tami.org.tw/category/contact_2.php?ms=" + ms + "&on=" + str(small_page)
				print comp_url

				comp_res = requests.get(comp_url)
				comp_soup = BeautifulSoup(comp_res.text, "lxml")
				comp_info = comp_soup.select(".banner-table")[0]

				comp = comp_info.select(".list_td")[0].text.encode("big5", "ignore").strip()
				tel = comp_info.select(".list_td")[1].text.encode("big5", "ignore").strip()
				address = comp_info.select(".list_td")[3].text.encode("big5", "ignore").strip()
				factory_tel = comp_info.select(".list_td")[4].text.encode("big5", "ignore").strip()
				factory_address = comp_info.select(".list_td")[6].text.encode("big5", "ignore").strip()

				data.append([large_category, category, comp, tel, address, factory_tel, factory_address])



# print data

with open("tami.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)



