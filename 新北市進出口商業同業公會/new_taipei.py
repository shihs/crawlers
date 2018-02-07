# -*- coding: utf-8 -*-
#爬取http://www.taiwanproduct.org/tc/p5-mem_list.asp 新北市進出口商業同業公會廠商名單
import requests
from bs4 import BeautifulSoup
import urllib



next = True

s = requests.Session()
url = "http://www.taiwanproduct.org/tc/p5-mem_list.asp"

data = []
data.append(["company", "tel", "address", "email", "web", "items", "products", "import_prducts", "export_products"])
page = 1


while next:	
	print page
	payload = {
		"PKey":"",
		"Page":str(page),
		"Class1_PKey":"",
		"Category":"",
		"Year_PKey":"",
		"Item_PKey":"-1",
		"Search":"OK",
		"SearchWord":""
	}

	
	res = s.post(url, data = payload)
	
	soup = BeautifulSoup(res.text, "html.parser")
	
	if len(soup.select("#bt_next")) == 0:
		next = False
	for i in soup.select(".text")[0].select("table")[1].select("tr"):
		tr = i.select("a")[0]
		company = tr.text.encode("big5", "ignore")
		print tr.text.encode("utf-8", "ignore")
		start = tr["href"].find(",'")
		end = tr["href"].find("')")
		para = tr["href"][(start+2):end]
	
		products = i.select("td")[3].text.encode("big5", "ignore")
	
	
		url_detail = "http://www.taiwanproduct.org/tc/p5-mem_detail.asp"
		payload = {
			"PKey":para,
			"Page":"undefined",
			"Class1_PKey":"",
			"Category":"",
			"Year_PKey":"",
			"Item_PKey":"-1",
			"Search":"OK",
			"SearchWord":""
		}
	
		res = s.post(url_detail, data = payload)
		# print res.text.encode("utf-8")
		soup = BeautifulSoup(res.text, "html.parser")
	
		info = {
			"電　　話":"",
			#"傳　　真":"",
			"地　　址":"",
			"Email":"",
			"網　　址":"",
			"營業項目":"",
			"進　　口":"",
			"出　　口":"",
		}
	
		for i in soup.select(".line_02")[0].select("table")[0].select("tr")[1:]:
			# print info[i.select("td")[0].text.encode("utf-8")]
			name = i.select("td")[1].text.encode("utf-8").strip()
			info[name] = i.select("td")[3].text.encode("utf-8").strip()
			# print info.get(i.select("td")[1].text.encode("utf-8").strip())
			# print info.get(name)
	
		
		tel = info.get("電　　話").decode("utf-8", "ignore").encode("big5", "ignore")
		address = info.get("地　　址").decode("utf-8", "ignore").encode("big5", "ignore")
		email = info.get("Email").decode("utf-8", "ignore").encode("big5", "ignore")
		web = info.get("網　　址").decode("utf-8", "ignore").encode("big5", "ignore")
		items = info.get("營業項目").decode("utf-8", "ignore").encode("big5", "ignore")
		import_prducts = info.get("進　　口").decode("utf-8", "ignore").encode("big5", "ignore")
		export_products = info.get("出　　口").decode("utf-8", "ignore").encode("big5", "ignore")
	
		data.append([company, tel, address, email, web, items, products, import_prducts, export_products])
	
	page = page + 1



import csv
f = open("newtaipei.csv","wb")
w = csv.writer(f)
w.writerows(data)
f.close()
