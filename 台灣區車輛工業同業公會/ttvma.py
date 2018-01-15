# -*- coding: utf-8 -*-
# 台灣區車輛工業同業公會 crawler
from bs4 import BeautifulSoup
import requests
import csv
import time




data = []
data.append(["company", "company tel", "factory tel", "import"])

comps = set()

original_url = "http://www.ttvma.org.tw/cht/"


url = "http://www.ttvma.org.tw/cht/search_catalog1.php?location="
res = requests.get(url)
soup = BeautifulSoup(res.text, "lxml")
industry_categories = soup.select(".report_txt_red")[:4]

for industry_category in industry_categories:
	industry_category_url = original_url + industry_category["href"]
	print industry_category_url

	res = requests.get(industry_category_url)
	soup = BeautifulSoup(res.text, "lxml")

	for large_category in soup.select(".ca1"):
		large_category_url = original_url + large_category["href"]
		print large_category_url
		large_category_res = requests.get(large_category_url)
		large_category_soup = BeautifulSoup(large_category_res.text, "lxml")

		time.sleep(1)

		for small_category in large_category_soup.select(".ca1"):
			page = 0
			run = True
			while run:
				page = page + 1
				small_category_url = original_url + small_category["href"] + "&page=" + str(page)				
	
				time.sleep(1)
				small_category_res = requests.get(small_category_url)
				small_category_soup = BeautifulSoup(small_category_res.text, "lxml")
				
				comp_infos = small_category_soup.select(".report_txt2")
				# stop if there's no company data
				if len(comp_infos) == 0:
					run = False
					break

				print small_category_url

				# company data
				for comp_info in comp_infos:
					if comp_info.text in comps:
						continue
						
					comp_url = original_url + comp_info["href"]
					print comp_url
					comp_res = requests.get(comp_url)
					comp_soup = BeautifulSoup(comp_res.text, "lxml")
					comp = comp_soup.select(".report_txt")[1].text.encode("big5", "ignore")
					comp_tel = comp_soup.select(".bgw")[1].select("td")[1].text.encode("big5", "ignore").strip()
					factory_tel = comp_soup.select(".bgw")[3].select("td")[1].text.encode("big5", "ignore").strip()
					importer = comp_soup.select(".bgg")[7].select("td")[1].text.encode("big5", "ignore").strip()
					data.append([comp, comp_tel, factory_tel, importer])
					print comp_soup.select(".report_txt")[1].text.encode("utf-8")
					time.sleep(1)
	
	# 		break
	# 	break
	# break

with open("ttvma.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)


print "DONE!"



