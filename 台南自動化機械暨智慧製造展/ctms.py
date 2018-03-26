# -*- coding: utf-8 -*-
# 台南自動化機械暨智慧製造展
from bs4 import BeautifulSoup
import requests
import time
import csv



data = []
data.append(["company"])



url = "http://cec.ctee.com.tw/ctms/content/2018tai-nan-zi-dong-hua-ji-jie-ji-zhi-hui-zhi-zao-zhan-chang-shang-zong-biao"
res = requests.get(url)
soup = BeautifulSoup(res.text, "lxml")

for i in soup.select(".field-label-hidden")[0].select("li"):
	category_url = i.select("a")[0]["href"]
	if "http" not in category_url:
		category_url = "http://" + category_url

	print category_url
	category_res = requests.get(category_url)
	# print category_res.text.encode("utf-8")
	category_soup = BeautifulSoup(category_res.text, "lxml")

	for i in category_soup.select(".even")[0].select("tr")[1:]:
		company = i.select("td")[1].text.encode("big5", "ignore")
		data.append([company])

	# break



with open("ctms.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)



print "DONE!"


