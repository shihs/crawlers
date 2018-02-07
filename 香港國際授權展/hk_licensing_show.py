# -*- coding: utf-8 -*-
# 香港國際授權展
from bs4 import BeautifulSoup
import requests
import csv
import urllib




data = []
data.append(["company", "tel"])


for page in range(3):
	url = "http://m.hktdc.com/fair/exlist/hklicensingshow-tc/%E9%A6%99%E6%B8%AF%E8%B2%BF%E7%99%BC%E5%B1%80%E9%A6%99%E6%B8%AF%E5%9C%8B%E9%9A%9B%E6%8E%88%E6%AC%8A%E5%B1%95/%E5%8F%83%E5%B1%95%E5%95%86%E5%90%8D%E5%96%AE.htm?bookmark=true&query=&breadcrumb=%0Aempclcountrynavigator%3Bempclcountry%3BTaiwan%3BTaiwan&page=" + str(page+1) + "&advanced=false&code=hklicensingshow&language=tc"
	print url
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "lxml")
	
	for i in soup.select(".noMarginB"):
		comp = i.text.encode("utf-8")
		comp_url = "http://m.hktdc.com/" + urllib.quote(i.select("a")[0]["href"].encode('utf8'))
		print comp
	
		comp_res = requests.get(comp_url)
		comp_soup = BeautifulSoup(comp_res.text, "lxml")
		
		for j in range(3, 6):
			try:
				info = comp_soup.select(".exhProfile")[j]
				if "電話號碼" in str(info.select(".col-xs-5")[0]):
					tel = info.select(".col-xs-7")[0].text.encode("utf-8")
					break
			except:
				tel = ""	
		data.append([comp, tel])


with open("hk_licensing_show.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

