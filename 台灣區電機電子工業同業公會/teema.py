# -*- coding: utf-8 -*-
# 爬取TEEMA B2B 廠商 http://www.teemab2b.com.tw/Index.aspx?Culture=zh-TW
from bs4 import BeautifulSoup
import requests
import csv
import time



data = []
data.append(["GUI", "company", "tel"])

s = requests.Session()

url = "http://www.teemab2b.com.tw/FindPdtCmp.aspx?key=&kind=company&pro=company,companyKeyword&culture=zh-TW"
res = s.get(url, timeout = 30)
soup = BeautifulSoup(res.text, "lxml")

pages = soup.select("#Label_PageCount")[0].text
VIEWSTATE = soup.select("#__VIEWSTATE")[0]["value"]
PREVIOUSPAGE = soup.select("#__PREVIOUSPAGE")[0]["value"]




for page in range(1, int(pages)):
	print page
	payload = {
		"__EVENTTARGET":"GridView2",
		"__EVENTARGUMENT":"Page$" + str(page),
		"__VIEWSTATE":VIEWSTATE,
		"__PREVIOUSPAGE":PREVIOUSPAGE,
		"select2":"繁體中文",
		"HiddenField_pro":"company,companyKeyword",
		"HiddenField_page":"0"
	}
	
	
	res = s.post(url, data = payload, timeout = 30)
	# print type(res.text)
	soup = BeautifulSoup(res.text, "lxml")

	l = len(soup.select(".table_text01"))-2
	# print l
	for i in range(l):
		print soup.select("#GridView2_HyperLink1_" + str(i))[0].text.encode(res.encoding)
		comp_url = "http://www.teemab2b.com.tw/" + soup.select("#GridView2_HyperLink1_" + str(i))[0]["href"]
		print comp_url
		comp_res = s.get(comp_url, timeout = 30)
		
		with open("Output.txt", "w") as text_file:
			text_file.write(comp_res.text.encode(res.encoding))

		comp_soup = BeautifulSoup(open("Output.txt"), "html.parser")


		# comp_soup = BeautifulSoup(comp_res.text, "lxml")
		# print comp_soup

		comp = comp_soup.select("#ContentPlaceHolder_Main_Label_companyName")[0].text.encode("big5", "ignore")
		#print comp		
		tel = comp_soup.select("#ContentPlaceHolder_Main_Label_CmpTel")[0].text.encode("big5", "ignore")
		#print tel
		GUI = comp_soup.select("#ContentPlaceHolder_Main_Label_Tax")[0].text.encode("big5", "ignore")
		#print GUI

		data.append([GUI, comp, tel])
	# break



with open("teema.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

	

print "FINISHED!"

