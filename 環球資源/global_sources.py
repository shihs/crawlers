# -*- coding: utf-8 -*-
# 爬取global sources四個展覽名單 http://www.taiwan.manufacturers.globalsources.com/
from bs4 import BeautifulSoup
import requests
import csv
import time




data = []
data.append(["company", "tel", "contact"])



# 依序爬取四個展覽
for shows in ["2808800044102", "2808800044185", "2808800044219", "2808800044276"]:
	page = 0
	while True:
		url = "http://www.globalsources.com/trdshw/GeneralManager?item_per_page=60&exNo=" + str(60*page) + "&action=ListExhibitor&language=zh&type=Exhibitor&tsid=" + shows + "&ctfilter=4294967170&country=TW"
		print url
		page += 1
		
		res = requests.get(url)
		# print res
		soup = BeautifulSoup(res.text, "lxml")
		
		if soup.select(".listing_h2")[0].text == "\n":
			break
		
		# 公司資訊
		for i in soup.select(".supplierTit"):
			comp = i.text.encode("utf-8").strip()
			print comp
	
			comp_url = "http://www.globalsources.com" + i["href"]
	
			comp_res = requests.get(comp_url)
			comp_soup = BeautifulSoup(comp_res.text, "lxml")
			
			# tel
			info = comp_soup.select(".com_info")[0].text.encode("utf-8").replace("\n", "")
			tel_pos = info.find("Tel")
			end = info.find("Fax:", tel_pos+5)
			tel = info[tel_pos+5:end].strip()
		
			# contact person
			if len(comp_soup.select(".com_contact")) != 0:
				contact = comp_soup.select(".com_contact")[0].text.encode("utf-8").replace("\n", " ").replace("Key Contact:", "").strip()		
			else:
				contact = ""
			print 
			
			data.append([comp, tel, contact])
			time.sleep(3)
			
	


with open("globalsources.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)


