# -*- coding: utf-8 -*-
#爬取中經社刊物http://www.cens.com/cens/html/zh/publication/pub_list.html各雜誌內容的公司
from bs4 import BeautifulSoup
import requests
import csv
import datetime





data = []
data.append(["magazine", "area", "company", "products", "tel"])

#刊物群列表
url_begin = "http://www.cens.com/cens/html/zh/publication/pub_list.html"

res = requests.get(url_begin)
# print res.encoding
# print res.text.encode(res.encoding)
soup = BeautifulSoup(res.text, "html.parser")

data = []
data.append(["company", "address", "tel"])

for i in soup.select(".sub-cate"):
	for j in i.select("a"):
		mag_url = "http://www.cens.com/" + j["href"]
		print mag_url

		mag_res = requests.get(mag_url)
		mage_soup = BeautifulSoup(mag_res.text, "lxml")

		for k in mage_soup.select("#frm_suplist")[0].select("table")[2:]:
			comp_url = "http://www.cens.com" + k.select("a")[0]["href"]
			print comp_url
			if "PUB_ID" in comp_url:
				continue
			ENCODE = mag_res.encoding
			comp_res = requests.get(comp_url)
			comp_soup = BeautifulSoup(comp_res.text, "lxml")
			comp_info = comp_soup.select(".prd-key-contact")[0]
			comp = comp_info.select("div")[0].select(".nr")[0].text.encode(ENCODE, "ignore").decode("utf-8", "ignore").encode("big5", "ignore")

			try:
				if comp_info.select("div")[1].select(".nl")[0].text.encode(ENCODE, "ignore").decode("utf-8", "ignore").encode("utf-8", "ignore") == "地址:":
					address = comp_info.select("div")[1].select(".nr")[0].text.encode(ENCODE, "ignore").decode("utf-8", "ignore").encode("big5", "ignore")
				if comp_info.select("div")[1].select(".nl")[0].text.encode(ENCODE, "ignore").decode("utf-8", "ignore").encode("utf-8", "ignore") == "電話:":
					tel = comp_info.select("div")[2].select(".nr")[0].text.encode(ENCODE, "ignore").decode("utf-8", "ignore").encode("big5", "ignore")
					address = ""
					data.append([comp, address, tel])
					continue
					
			except:
				address = ""

			try:
				if comp_info.select("div")[1].select(".nl")[0].text.encode(ENCODE, "ignore").decode("utf-8", "ignore").encode("utf-8", "ignore") == "電話:":
					tel = comp_info.select("div")[2].select(".nr")[0].text.encode(ENCODE, "ignore").decode("utf-8", "ignore").encode("big5", "ignore")
			except:
				tel = ""

			print comp, tel

			data.append([comp, address, tel])

with open("tee.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)



# for i in soup.select(".boxtitle5"):
	
# 	#爬取雜誌網址與名稱
# 	if (len(i.select("a")) != 2 and len(i.select("font")) != 2):
# 		continue
# 	url = "http://www.cens.com/" + i.select("a")[0]["href"]
# 	mag = str(i.select("font")[0].text.encode("ISO-8859-1").strip()).decode("utf-8", "ignore").encode("big5", "ignore")

# 	print url

# 	res = requests.get(url)
# 	# print res.encoding
# 	soup = BeautifulSoup(res.text, "html.parser")
	
# 	#雜誌有三部分有公司名稱

# 	tel = ""
# 	print "advertising......"
# 	area = "精選廣告".decode("utf-8").encode("big5")
# 	for i in soup.select(".n_cate_innerK"):
# 		url_cg = "http://www.cens.com" + i.select("a")[0]["href"]
# 		url_cg = url_cg.replace(";", "&")
# 		print url_cg
# 		res = requests.get(url_cg)
# 		# print res.encoding
# 		soup_cg = BeautifulSoup(res.text, "html.parser")
# 		box = soup_cg.select(".boxtitle3")[0]#.text.encode("utf-8", "ignore").strip()
# 		company = box.select(".boxtitle")[0].text.encode("big5", "ignore").strip()
# 		products = box.select("font")[0].text.encode("big5", "ignore").strip().replace("...(more)", "")
		
# 		data.append([mag, area, company, products, tel])
	
# 	print "special......"
# 	area = "精選供應商".decode("utf-8").encode("big5")
# 	choice = soup.select(".title_supplier")
# 	for i in range(len(choice)/2):
# 		# print res.encoding
# 		company = str(choice[i*2+1].text.encode("ISO-8859-1", "ignore").strip()).decode("utf-8", "ignore").encode("big5", "ignore")
# 		# print company
# 		url_ch = choice[i*2+1].select("a")[0]["href"]
# 		res = requests.get(url_ch)
# 		print url_ch
# 		soup_ch = BeautifulSoup(res.text, "html.parser")
# 		products = ""
# 		if len(soup_ch.select(".desc-info")) >= 2 :
# 			products = str(soup_ch.select(".desc-info")[1].text.encode("ISO-8859-1", "ignore").strip()).decode("utf-8", "ignore").encode("big5", "ignore")
# 		tel = ""
# 		for i in range(len(soup_ch.select(".nl"))):
# 			if soup_ch.select(".nl")[i].text.encode("ISO-8859-1").strip() == "電話:":
# 				tel = str(soup_ch.select(".nr")[i].text.encode("ISO-8859-1", "ignore").strip()).decode("utf-8", "ignore").encode("big5", "ignore")
# 				tel = tel.replace("+", "")
# 				break
	
# 		data.append([mag, area, company, products, tel])
	
# 	print "brand......"
# 	area = "品牌專區".decode("utf-8").encode("big5")
# 	for i in soup.select(".featured_x"):
# 		# print i.select("a")[0]["href"]
# 		url_bd = "http://www.cens.com" + i.select("a")[0]["href"]
# 		print url_bd
# 		info = i.select("a")[0]["onmouseover"].split(",")
# 		# company
# 		company = str(info[0].encode("ISO-8859-1", "ignore").replace("popup2(", "").replace("'", "").strip()).decode("utf-8", "ignore").encode("big5", "ignore")
# 		res = requests.get(url_bd)
# 		soup_bd = BeautifulSoup(res.text, "html.parser")
# 		products = ""
# 		if len(soup_bd.select(".desc-info")) >= 2:
# 			products = str(soup_bd.select(".desc-info")[1].text.encode("ISO-8859-1", "ignore").strip()).decode("utf-8", "ignore").encode("big5", "ignore")
# 		tel = ""
# 		for i in range(len(soup_bd.select(".nl"))):
# 			if soup_bd.select(".nl")[i].text.encode("ISO-8859-1").strip() == "電話:":
# 				tel = str(soup_bd.select(".nr")[i].text.encode("ISO-8859-1", "ignore").strip()).decode("utf-8", "ignore").encode("big5")
# 				tel = tel.replace("+", "")
# 				break
		
# 		data.append([mag, area, company, products, tel])


# with open("tee_" + str(datetime.datetime.now())[0:9].replace("-", "") + ".csv", "wb") as f:
# 	w = csv.writer(f)
	# w.writerows(data)




