# -*- coding:utf-8 -*-
# 爬取 http://mission.taiwantrade.com.tw/ 展覽名單
import requests
from bs4 import BeautifulSoup
import csv



data = []
data.append(["exhibition date", "exhibition", "company", "contact person", "url", "email", "address", "tel"])


url = "http://mission.taiwantrade.com.tw/"
res = requests.get(url)
soup = BeautifulSoup(res.text, "lxml")



# 不同展覽
for i in soup.select("#tblTop")[0].select("tr")[3:]:
	#print i.text.encode("utf-8")
	if len(i.select(".Calendar-Date")) == 0:	
		continue
	date = i.select(".Calendar-Date")[0].text.encode("utf-8")
	exhi_url = i.select(".Calendar-MissionName")[0]["href"]
	print exhi_url
	exhi_name = i.select(".Calendar-MissionName")[0].text.encode("utf-8")
	print exhi_name
	
	# 展覽網址
	exhi_res = requests.get(exhi_url)
	#pritn exhi_res.text.encode("utf-8")
	exhi_soup = BeautifulSoup(exhi_res.text, "lxml")


	# exhibitors名單頁面
	if len(exhi_soup.select(".LeftMenu")) == 0 and len(exhi_soup.select("#Lmenu2")) == 0:
		continue
	elif len(exhi_soup.select(".LeftMenu")) != 0:
		exhibitors_url = exhi_soup.select(".LeftMenu")[1]["href"]
	else:
		exhibitors_url = exhi_soup.select("#Lmenu2")[0].select("a")[0]["href"]
	
	print exhibitors_url
	
	exhibitors_res = requests.get(exhibitors_url)
	exhibitors_soup = BeautifulSoup(exhibitors_res.text, "lxml")

	if len(exhibitors_soup.select(".PageUnSelected")) != 0:
		pages = int(exhibitors_soup.select(".PageUnSelected")[-1].text.encode("utf-8"))
	# else:
	# 	pages = int(exhibitors_soup.select(".PageUnSelected")[-1].text.encode("utf-8"))
	
	id_code = ""

	for page in range(pages):
		print page
		if page != 0:
			exhibitors_url = exhibitors_url + "&DataGridPage=" + str(page + 1) + "&DataGridSort=11&DataGridOrder=0"
			exhibitors_res = requests.get(exhibitors_url)
			exhibitors_soup = BeautifulSoup(exhibitors_res.text, "lxml")
		print "here"
		for j in exhibitors_soup.select("table")[0].select("table"):#[2].select("table"):

			# find the tag of company box
			if len(j.select("label")) != 0:
				comp = j.select("label")[0].text.encode("utf-8")
				
				if j.select("label")[0]["id"].replace("CN_", "") == id_code:
					#print comp
					
					continue
				id_code = j.select("label")[0]["id"].replace("CN_", "")
	
				# company information
				contact = ""
				comp_url = ""
				contact_email = ""
				comp_address = ""
				tel = ""

				comp_info = exhibitors_soup.select("#div_hiddenTable_" + id_code)[0]
				#print comp_info
				for pos in range(len(comp_info.select(".bodytext"))):
					if comp_info.select(".bodytext1")[pos].text == "Contact:":
						contact = comp_info.select(".bodytext")[pos].text.encode("utf-8")

					elif comp_info.select(".bodytext1")[pos].text == "URL:":
						comp_url = comp_info.select(".bodytext")[pos].text.encode("utf-8")

					elif comp_info.select(".bodytext1")[pos].text == "Email:":
						contact_email = comp_info.select(".bodytext")[pos].text.encode("utf-8")

					elif comp_info.select(".bodytext1")[pos].text == "Address: ":
						comp_address = comp_info.select(".bodytext")[pos].text.encode("utf-8")
						
					elif comp_info.select(".bodytext1")[pos].text == "Tel: ":
						tel = comp_info.select(".bodytext")[pos].text.encode("utf-8")

					else:
						continue
				
				
				data.append([date, exhi_name, comp, contact, comp_url, contact_email, comp_address, tel])
				print comp
		
with open("trade_mission.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

	

	
