# -*- coding: utf-8 -*-
#爬取
#http://tc.mw.com.tw/company.php?id=1 台中市精密機械科技創新園區 與
#http://fc.mw.com.tw/company.php?id=1 台中市豐洲科技工業園區  資料
import requests
from bs4 import BeautifulSoup
import csv



def crawler(addr, zone, file_name):
	#儲存所有爬到的資料
	data = []
	#欄位名稱
	data.append(["zone", "company", "tel", "address"])
	#第一期、第二期
	number = ["1", "2"]
	#分別爬取第一期、第二期
	for i in number:
		url = addr + "company.php?id=" + i
		res = requests.get(url)
		soup = BeautifulSoup(res.text, "html.parser")
		for j in soup.select(".WebForm")[0].select("tr"):
			#如果有資料爬取
			if len(j.select("td")) != 0:
				#公司名稱
				name = j.select("td")[1].text.encode("big5")
				#公司地址
				address = j.select("td")[2].text.encode("big5")
				#如果地址第一個字為數字則地址內容改為空白
				if address[0].isdigit():
					address = "" 
				#如果有該公司的詳細資料頁面
				if len(j.select("td")[1].select("a")) != 0:
					url = addr +  j.select("td")[1].select("a")[0]["href"]
					print url
					res = requests.get(url)
					soup = BeautifulSoup(res.text, "html.parser")
					#公司電話
					tel = soup.select(".para")[0].text.encode("big5", "ignore")
				else:
					tel = ""
				
				data.append([zone.decode("utf-8").encode("big5"), name, tel, address])
	
	# f = open("../data/factory/taichung_chinmi.csv", "wb")
	f = open(file_name, "wb")
	w = csv.writer(f)
	w.writerows(data)
	f.close()


# crawler("http://tc.mw.com.tw/", "台中市精密機械科技創新園區", "taichung_chinmi.csv")

crawler("http://fc.mw.com.tw/", "台中市豐洲科技工業園區", "taichung_fonchou.csv")
