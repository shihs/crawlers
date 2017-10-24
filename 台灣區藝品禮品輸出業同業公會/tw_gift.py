# -*- coding: utf-8 -*-
# 爬取 台灣區藝品禮品輸出業同業公會 廠商名單 http://www.gift.com.tw/index.php?t=pc
from bs4 import BeautifulSoup
import requests
import csv
import time



data = []
data.append(["company", "tel", "boss"])

# url = "http://www.gift.com.tw/list.php#lis"
# res = requests.get(url)
# soup = BeautifulSoup(res.text, "lxml")

# for i in soup.select(".TAB2")[0].select(".ALIGN_LEFT"):
# 	# print i.text.encode(res.encoding)
# 	print "http://www.gift.com.tw/" + i.select("a")[0]["href"]

for category in range(48):
	url = "http://www.gift.com.tw/list_02.php?num=" + str(100) + "&class_id=" + str(category+1) + "#lis2"
	print url
	res = requests.get(url, timeout = 30)
	soup = BeautifulSoup(res.text, "lxml")

	for i in soup.select(".m_top"):
		comp = i.select("a")[0].text.encode(res.encoding)
		print comp
		comp_url = "http://www.gift.com.tw/" + i.select("a")[0]["href"]

		comp_res = requests.get(comp_url)
		comp_soup = BeautifulSoup(comp_res.text, "lxml")

		tel = comp_soup.select(".ALIGN_LEFT")[2].text.encode(res.encoding).decode("utf-8", "ignore").encode("big5", "ignore")
		boss = comp_soup.select(".ALIGN_LEFT")[0].text.encode(res.encoding).decode("utf-8", "ignore").encode("big5", "ignore")

		data.append([comp.decode("utf-8", "ignore").encode("big5", "ignore"), tel, boss])

		time.sleep(3)
	# break


with open("tw_gift.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

print "FINISHED!"
