# -*- coding: utf-8 -*-
# 桃園市產業園區http://www.tyht.nat.gov.tw/c/index.aspx
from bs4 import BeautifulSoup
import requests
import csv


data = []
f = open('tyht.csv','w')
for page in range(8):
	url = "http://www.tyht.nat.gov.tw/c/industries/t05_industries_01.aspx?page=" + str(page+1)
	res = requests.get(url)
	print res.encoding
	# print res.text.encode("utf-8")
	soup = BeautifulSoup(res.text, "lxml")

	for i in soup.select("#ctl00_cph_Content_gv_Data_ctl02_lab_C_Name"):
		# print i.text.encode("utf-8").strip().replace(" ", "")
		f.write(i.text.encode("big5").strip().replace(" ", "") + "\n")
		


f.close()