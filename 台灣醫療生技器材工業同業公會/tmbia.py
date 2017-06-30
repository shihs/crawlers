# -*- coding: utf-8 -*-
# 爬取http://www.tmbia.org.tw/台灣醫療生技器材工業同業公會廠商名單
from bs4 import BeautifulSoup
import requests
import csv


data = []
data.append(["company", "GUI", "boss", "address", "tel", "fac_address", "fac_tel", "items"])

page = 0 

while True:
	url = "http://www.tmbia.org.tw/big5/t_member.php?&show_num=" + str(page * 20)
	page = page + 1

	res = requests.get(url)
	
	soup = BeautifulSoup(res.text, "lxml")
	
	if len(soup.select(".center_text")) == 1:
		break
	
	for i in soup.select(".style2")[2:]:
		company = i.text.encode(res.encoding).decode("utf-8").encode("big5", "ignore")
		link = "http://www.tmbia.org.tw/big5/" + i.select("a")[0]["href"]
		print link
		res_link = requests.get(link)
		# print res_link
	
		soup_link = BeautifulSoup(res_link.text, "lxml")
	
		detail = soup_link.select(".center_text")
	
		GUI = detail[1].text.encode(res.encoding).decode("utf-8").encode("big5", "ignore")
		boss = detail[2].text.encode(res.encoding).decode("utf-8").encode("big5", "ignore")
		address = detail[4].text.encode(res.encoding).decode("utf-8").encode("big5", "ignore")
		tel = detail[5].text.encode(res.encoding).decode("utf-8").encode("big5", "ignore")
		fac_address = detail[7].text.encode(res.encoding).decode("utf-8").encode("big5", "ignore")
		fac_tel = detail[8].text.encode(res.encoding).decode("utf-8").encode("big5", "ignore")
		items = detail[10].text.encode(res.encoding).decode("utf-8").encode("big5", "ignore")
	
		row = [company, GUI, boss, address, tel, fac_address, fac_tel, items]	
		data.append(row)



with open("tmbai.csv", "ab") as f:
	w = csv.writer(f)
	w.writerows(data)
