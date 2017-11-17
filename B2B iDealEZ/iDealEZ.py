# -*- coding: utf-8 -*-
# 爬取 taiwantrade iDealEZ http://www.idealez.com/home/zh_TW
from bs4 import BeautifulSoup
import requests
import csv
import time






def crawl_info(comp_id):

	# 檢查是否爬取過
	if comp_id in COMP_IDS:
		return
	COMP_IDS.add(comp_id)

	# 檢查公司資訊頁面種類
	if comp_id.isdigit():
		comp_url = "http://www.idealez.com/company-profile/zh_TW/" + comp_id
		import_market = "主要出口商品".decode("utf-8").encode("big5", "ignore")
		td = 1

	else:
		comp_url = "http://www.idealez.com/" + comp_id + "/company-profile/zh_TW"
		import_market = "主要出口市場".decode("utf-8").encode("big5", "ignore")
		td = 0

	print comp_url

	try:
		comp_res = requests.get(comp_url)
		comp_soup = BeautifulSoup(comp_res.text, "lxml")

	except requests.ConnectionError:
		with open("iDealEZ.csv", "ab") as f:
			w = csv.writer(f)
			w.writerows(data)
		data = []

		return "Connetion Error."



	# 不同種類的公司資訊頁面的公司名稱在不同tag
	try:
		if comp_id.isdigit():
			#comp = comp_soup.select(".company_profile")[0].select(".title")[0].text.encode("big5", "ignore").replace("介紹".decode("utf-8").encode("big5", "ignore"), "").strip()
			comp = comp_soup.select(".big2")[0].text.encode("big5", "ignore").strip()
		else:
			comp = comp_soup.select(".company_name")[0].text.encode("big5", "ignore").strip()
	except:
		return


	tel = ""
	contact_person = ""
	import_contry = ""

	# 公司資訊
	try:		
		for info in comp_soup.select(".tb_info")[0].select("tr"):
			if "電話".decode("utf-8").encode("big5", "ignore") in info.select("th")[0].text.encode("big5", "ignore"):
				tel = info.select("td")[0].text.encode("big5", "ignore")
			if "聯絡人".decode("utf-8").encode("big5", "ignore") in info.select("th")[0].text.encode("big5", "ignore"):
				contact_person = info.select("td")[0].text.encode("big5", "ignore")
			if import_market in info.select("th")[0].text.encode("big5", "ignore"):
				import_contry = info.select("td")[td].text.encode("big5", "ignore")
	except:
		return comp, tel, contact_person, import_contry

	return comp, tel, contact_person, import_contry





data = []
data.append(["company", "tel", "contact person", ])

url = "http://www.idealez.com/category/zh_TW/"
res = requests.get(url)
# print res

# 儲存已爬取過的公司id
COMP_IDS = set()

soup = BeautifulSoup(res.text, "lxml")


for i in soup.select(".title")[1:]:
	category = i.select("a")[0].text.encode("big5", "ignore").strip()
	page = 1
	print category

	while True:

		try:
			cat_url = "http://www.idealez.com/product-search/zh_TW/-1/-1/-1/-1/-1/90/"+ str(page) + "/-1/" + i.select("a")[0]["href"][46:48] + "/-1/-1/-1/-1/-1/-1/-1/-1/-1/-1/-1/CATEGORY4_DIGT_ID_NAME/0"			
			cat_res = requests.get(cat_url)
			cat_soup = BeautifulSoup(cat_res.text, "lxml")
		except requests.ConnectionError:
			with open("iDealEZ.csv", "ab") as f:
				w = csv.writer(f)
				w.writerows(data)
			data = []

			time.sleep(60)

		except:
			break

	
		if len(cat_soup.select(".result_info")) != 0:
			break
		
		print cat_url

		# 商品們
		for n in range(len(cat_soup.select(".p_name"))-5):
			commodity = cat_soup.select(".p_name")[n]
			product_url = commodity.select("a")[0]["href"]
			# print product_url
			
			# 公司資訊頁第一種模板
			if product_url.count("/") == 4:
				comp_id = product_url[1:product_url.find("/", 2)]
				info = crawl_info(comp_id)
						
			# 公司資訊頁第二種模板
			if product_url.count("/") == 3:
				comp_id = cat_soup.select(".btn_addcart")[n]["onclick"]
				pos = comp_id.find(",", 48)
				comp_id = comp_id[pos+2:(comp_id.find(",", pos+1)-1)]
				# print comp_id
				
				info = crawl_info(comp_id)


			if info == None:
				continue
			
			if info == "Connetion Error.":
				break
	
			
			data.append([info[0], info[1], info[2], info[3]])
		# break
		page += 1

		time.sleep(1)
	time.sleep(3)
	
	
	# break



with open("iDealEZ.csv", "ab") as f:
	w = csv.writer(f)
	w.writerows(data)


print "DONE!"

