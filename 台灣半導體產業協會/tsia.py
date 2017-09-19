# -*- coding:utf-8 -*-
# 爬取台灣半導體產業協會廠商名單http://www.tsia.org.tw/member_list.php?page=1
import requests
from bs4 import BeautifulSoup
import csv
import zipfile



data = []
data.append(["company", "boss", "tel", "web"])


for page in range(7):
	url = "http://www.tsia.org.tw/member_list.php?page=" + str(page + 1)
	res = requests.get(url)
	
	soup = BeautifulSoup(res.text, "lxml")
	
	for i in soup.select(".list_form_bg")[0].select("tr")[1:-2]:
		#comp = i.select(".list_form_subject")[0].text.encode(res.encoding).decode("utf-8").encode("utf-8").strip()
		#print comp
		comp_url = "http://www.tsia.org.tw/" + i.select(".list_form_subject")[0].select("a")[0]["href"]
	
		comp_res = requests.get(comp_url)
		comp_soup = BeautifulSoup(comp_res.text, "lxml")
	
		comp_info = comp_soup.select(".inside02Copy")[0].select(".member_info03")
		
		comp = comp_info[0].text.encode(res.encoding).decode("utf-8").encode("big5", "ignore").strip()
		boss = comp_info[1].text.encode(res.encoding).decode("utf-8").encode("big5", "ignore").strip()
		tel = comp_info[2].text.encode(res.encoding).decode("utf-8").encode("big5", "ignore").strip()
		web = comp_info[4].text.encode(res.encoding).decode("utf-8").encode("big5", "ignore").strip()
	
		print comp#, boss, tel, web

		data.append([comp, boss, tel, web])


with open("tsai.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

