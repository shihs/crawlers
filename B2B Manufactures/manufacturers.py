# -*- coding: utf-8 -*-
# 爬取B2B manufacturers廠商名單 http://www.manufacturers.com.tw/
from bs4 import BeautifulSoup
import requests
import csv
import time
import random



def crawl_company(comps_url, comps_name, data):
	comps_res = requests.get(comps_url, timeout = 30)
	comps_soup = BeautifulSoup(comps_res.text, "lxml")	

	# 沒有廠商名單
	if len(comps_soup.select(".item-title")) == 0:
		print "Empty list."
		return "None"

	# 公司資訊
	for comps in comps_soup.select(".item-title"):
		comp = comps.text.encode("utf-8")

		# 公司是否爬取過
		if comp in comps_name:
			print "Done before."
			continue
		comps_name.add(comp)

		comp_url = "http://www.manufacturers.com.tw" + comps.select("a")[0]["href"]
		print "company url: " + comp_url
	
		comp_res = requests.get(comp_url, timeout = 30)
		comp_soup = BeautifulSoup(comp_res.text, "lxml")	
	
		# 公司資訊
		if len(comp_soup.select(".top_contact")) == 0:
			data.append([comp, ""])
			continue

		contact_info = comp_soup.select(".top_contact")[0].select(".media-body")
		print comp
		
		if len(contact_info) >= 1:

			if contact_info[0].text.encode("utf-8") != "Taiwan":
				# data.append([comp, ""])
				continue

			if len(contact_info) > 1:
				tel = contact_info[2].text.encode("utf-8")
				data.append([comp, tel])
				continue
			
			data.append([comp, ""])

		else:
			data.append([comp, ""])

	return data

def crawl_all_company(TAG, comps_name, data):
	#print len(TAG)
	for products in TAG:
		#print products.select("a")
		comps_url = products.select("a")[0]["href"]

		if "http://www.manufacturers.com.tw" not in comps_url:
			comps_url = "http://www.manufacturers.com.tw" + comps_url
		print comps_url
		comps_res = requests.get(comps_url, timeout = 30)
		comps_soup = BeautifulSoup(comps_res.text, "lxml")

		# 抓取第二頁後的網址
		if len(comps_soup.select(".pagination")) == 0:
			continue
		if len(comps_soup.select(".pagination")[0].select("a")) > 1:
			comps_url = "http://www.manufacturers.com.tw" + comps_soup.select(".pagination")[0].select("a")[1]["href"][:-1]	

		else:
			print "companies url: " + comps_url
			data = crawl_company(comps_url, comps_name, data)
			# return data
			continue
			
		page = 0
		while True:
			print "companies url: " + comps_url + str(page+1)
			d = crawl_company(comps_url + str(page+1), comps_name, data)
			
			if d != "None":
				page += 1
				data = d
			else:
				break
		

	return data







comps_name = set()

data = []
data.append(["company", "tel"])

url = "http://www.manufacturers.com.tw"
res = requests.get(url, timeout = 30)
soup = BeautifulSoup(res.text, "lxml")

# 所有大分類
for i in soup.select(".col-md-6")[2:]:
	category_url = url + i.select("a")[0]["href"]
	print category_url
	category_res = requests.get(category_url, timeout = 30)
	category_soup = BeautifulSoup(category_res.text, "lxml")

	
	# 大分類的related products
	data = crawl_all_company(category_soup.select(".panel-body")[1].select(".col-sm-6"), comps_name, data)
	#print len(data)
	
	# 大分類底下的小分類
	for j in category_soup.select(".panel-body")[0].select(".col-sm-6"):
		j_res = requests.get(url + j.select("a")[0]["href"], timeout = 30)
		print url + j.select("a")[0]["href"]
		j_soup = BeautifulSoup(j_res.text, "lxml") 
		# print j_soup.select(".panel-body")[0].select(".col-sm-6")
		# break
		data = crawl_all_company(j_soup.select(".panel-body")[0].select(".col-sm-6"), comps_name, data)
		#print len(data)
	# break


	print


with open("manufacturers.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

print "DONE!"
