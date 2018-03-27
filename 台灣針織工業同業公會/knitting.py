# -*- coding: utf-8 -*-
# 台灣針織工業同業公會廠商名單 http://knitting.org.tw/
from bs4 import BeautifulSoup
import requests
import csv
import time
import urllib





def get_payload(soup):

	hidden  = soup.select("#form1")[0]
	__VIEWSTATE = hidden.select("#__VIEWSTATE")[0]["value"]
	__VIEWSTATEGENERATOR = hidden.select("#__VIEWSTATEGENERATOR")[0]["value"]
	__SCROLLPOSITIONX = "0"
	__SCROLLPOSITIONY = "0"
	__EVENTVALIDATION = hidden.select("#__EVENTVALIDATION")[0]["value"]

	# # break
	payload = {
		#"__EVENTTARGET": "GridView1$ctl17$ctl" + str(page).zfill(2),
		"__EVENTTARGET":"GridView1$ctl17$lbnNext",
		"__VIEWSTATE": __VIEWSTATE,
		"__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
		"__SCROLLPOSITIONX": __SCROLLPOSITIONX,
		"__SCROLLPOSITIONY": __SCROLLPOSITIONY,
		"__EVENTVALIDATION": __EVENTVALIDATION,
		"__VIEWSTATEENCRYPTED":"",
		"__EVENTARGUMENT":"" 
	}

	return payload



def get_info(company):
	comp_url = "http://knitting.org.tw/Firm_details.aspx?com_named_c=" + urllib.quote(company.text.encode("utf-8"))
	print comp_url
	comp_res = requests.get(comp_url)
	comp_soup = BeautifulSoup(comp_res.text, "lxml")
	tel = comp_soup.select("#DetailsView1_Label2")[0].text.encode("big5", "ignore")
	contact_person = comp_soup.select("#DetailsView1_Label5")[0].text.encode("big5", "ignore")

	return tel, contact_person








comp_first = ""
data = []
data.append(["company", "tel", "contact person"])

s = requests.Session()

url = "http://knitting.org.tw/Firm_list.aspx"
res = s.get(url)
# print res.text.encode("utf-8")
soup = BeautifulSoup(res.text, "lxml")

print "Page:1"
for i in range(14):
	comp = soup.select("#GridView1_HyperLink1_" + str(i))[0]
	
	tel, contact_person = get_info(comp)
	data.append([comp.text.encode("big5", "ignore"), tel, contact_person])

	# if i == 0:
	# 	comp_first = comp


page = 0
while True:
	print "Page:" + str(page+2)
	payload = get_payload(soup)
	res = s.post(url, data = payload)
	soup = BeautifulSoup(res.text, "lxml")
	
	# if soup.select("#GridView1_HyperLink1_" + str(0))[0] == comp_first:
	# 	print "here"
	# 	break
	
	try:
		for i in range(14):
			comp = soup.select("#GridView1_HyperLink1_" + str(i))[0]
		
			tel, contact_person = get_info(comp)
			data.append([comp.text.encode("big5", "ignore"), tel, contact_person])
	except:
		break
	
	page += 1

	# if page == 10:
	# 	break
	time.sleep(0.5)





with open("knitting.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

