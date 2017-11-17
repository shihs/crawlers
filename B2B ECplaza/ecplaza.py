# -*- coding: utf-8 -*-
# 爬取 ECPLAZA https://www.ecplaza.net/ 台灣廠商
from bs4 import BeautifulSoup
import requests
import csv
import time




data = []
data.append(["company", "tel"])

comp_set = set()


# 所有分類列表
url = "https://www.ecplaza.net/company/TW"
res = requests.get(url)
soup = BeautifulSoup(res.text, "lxml")



# 所有分類網址
for category in soup.select(".row")[1].select("li"):
	category_url = category.select("a")[0]["href"]
	
	print category_url
	category_res = requests.get(category_url, timeout = 30)
	category_id = category_res.text.encode("utf-8")
	pos = category_id.find("categoryid")
	category_id = category_id[(pos+12):category_id.find(",", pos)]
	# 該分類的網址名稱	
	category_name = category_url[category_url.find("net/")+4:category_url.find('">')]
	# 新的分類重新計算頁數
	page = 1
	# 頁數
	while True:
		category_url = "https://www.ecplaza.net/company/" + category_name + "--" + category_id + "/TW?page=" + str(page)
		print category_url
	
		category_res = requests.get(category_url, timeout = 30)
		category_soup = BeautifulSoup(category_res.text, "lxml")
	
		comps = category_soup.select(".underline")

		# 如果沒有公司list則跳出該分類
		if len(comps) == 0:
			break
	
		for c in comps:
			# 公司名稱
			comp = c.text.encode("utf-8")
			
			# 若重覆則略過
			if comp in comp_set:
				continue
	
			comp_set.add(comp)

			comp_url = c["href"] + "/contact"
			comp_res = requests.get(comp_url, timeout = 30)
			comp_soup = BeautifulSoup(comp_res.text, "lxml")


			# 電話
			try:
				if "Phone" in comp_soup.select(".table")[0].select("th")[5].text.encode("utf-8"):
					tel = comp_soup.select(".table")[0].select("td")[5].text.encode("utf-8").strip()
					data.append([comp, tel])
					print comp, tel
					continue
		
				if "Phone" in comp_soup.select(".table")[0].select("th")[4].text.encode("utf-8"):
					tel = comp_soup.select(".table")[0].select("td")[4].text.encode("utf-8").strip()
					data.append([comp, tel])
					print comp, tel
					continue
		
				if "Phone" in comp_soup.select(".table")[0].select("th")[3].text.encode("utf-8"):
					tel = comp_soup.select(".table")[0].select("td")[3].text.encode("utf-8").strip()
					data.append([comp, tel])
					print comp, tel
					continue
			except:
				data.append([comp, ""])
				print comp, tel

			time.sleep(1)

		page += 1
		

		time.sleep(3)



	time.sleep(5)



with open("ecplaza.csv", "wb")	as f:
	w = csv.writer(f)
	w.writerows(data)



print "DONE!"
