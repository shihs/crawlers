# -*- coding: utf-8 -*-
# 爬取 愛台灣文創 http://www.lovetaiwan.com.tw/
from bs4 import BeautifulSoup
import requests
import csv
import time
import math



data = []
data.append(["company", "tel"])


url = "http://www.lovetaiwan.com.tw/index1.php/more_industry_category/index/1/"
res = requests.get(url)

soup = BeautifulSoup(res.text, "lxml")


for i in soup.select("#classify_1")[0].select("li"):
	category_url = i.select("a")[0]["href"]#.text.encode("utf-8")
	category_res = requests.get(category_url)
	category_soup = BeautifulSoup(category_res.text, "lxml")

	pages = category_soup.select("#page2")[0].select("td")[1].text.encode(res.encoding)
	pages = int(math.ceil(int(pages[3:pages.find(" ", 4)].strip())/10))+1

	for page in range(pages):
		for j in category_soup.select("#list")[0].select("tr")[1:]:
			comp_url = j.select("a")[0]["href"] + "/" + str(page+1)
			print comp_url
			comp_res = requests.get(comp_url)
			comp_soup = BeautifulSoup(comp_res.text, "lxml")
			
			info = comp_soup.select(".name")[0]
			comp = info.select("div")[0].text.encode(comp_res.encoding).decode("utf-8", "ignore").encode("big5", "ignore").replace("公司：".decode("utf-8").encode("big5"), "").strip()
			tel = info.select("div")[1].text.encode(comp_res.encoding).decode("utf-8", "ignore").encode("big5", "ignore").replace("電話：".decode("utf-8").encode("big5"), "")
			tel = tel[:tel.find(" ")].strip()
			# print comp, tel
			data.append([comp, tel])
			time.sleep(3)
			# break
		time.sleep(3)
		# break
	time.sleep(5)
	# break




with open("lovetaiwan.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)






