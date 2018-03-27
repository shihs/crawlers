# -*- coding: utf-8 -*-
# Taiwan Bicycle cralwer
from bs4 import BeautifulSoup
import requests
import time
import csv



data = []
data.append(["company", "contact person", "tel"])


url = "http://taiwan-bicycle.com.tw/company.asp"
res = requests.get(url)
soup = BeautifulSoup(res.text, "lxml")

s102 = soup.select(".s1202")
s102_len = len(s102)/2


for i in range(s102_len):
	# 大分類
	large_category_url = "http://taiwan-bicycle.com.tw/" + s102[i*2+1]["href"]
	print large_category_url

	time.sleep(1)
	large_category_res = requests.get(large_category_url)
	large_category_soup = BeautifulSoup(large_category_res.text, "lxml")

	for j in large_category_soup.select(".s1403"):

		page = 0
		run = True
		while run:
			page = page + 1
			# 小分類
			small_category_url = "http://taiwan-bicycle.com.tw/" + j["href"] + "&Page_No=" + str(page)			
			print small_category_url
			time.sleep(1)

			small_category_res = requests.get(small_category_url)
			small_category_soup = BeautifulSoup(small_category_res.text, "lxml")
	
			comps = small_category_soup.select("table")[0]
			for pos in range(10):
				table_pos = 10+pos*2
				comp_info = comps.select("table")[table_pos]
	
				if len(comp_info.select("font")) == 0:
					run = False
					break
				if "Taiwan" not in comp_info.select("font")[0]:
					continue
	
				comp_url = "http://taiwan-bicycle.com.tw/" + comp_info.select("a")[-2]["href"]
				print comp_url
	
				try:
					time.sleep(1)
					comp_res = requests.get(comp_url, timeout = 30)					
	
					comp_soup = BeautifulSoup(comp_res.text, "lxml")
					comp_info = comp_soup.select("tbody")[0]
					
					comp = comp_info.select("tr")[0].select("td")[1].text.encode("utf-8")
					contact_person = comp_info.select("tr")[2].select("td")[1].text.encode("utf-8")
					tel = comp_info.select("tr")[5].select("td")[1].text.encode("utf-8")
					print comp
					data.append([comp, contact_person, tel])
	
				except:
					print "oops"
	
				
	# 	break
	# break



with open("taiwan_bicycle.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

