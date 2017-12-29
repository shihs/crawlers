# -*- coding: utf-8 -*-
# http://admin.taiwan.net.tw/index.aspx 中華民國交通部觀光局-觀光相關產業-旅行業
from bs4 import BeautifulSoup 
import requests
import csv
import time



data = []
data.append(["company", "tel"])


url = "http://admin.taiwan.net.tw/travel/travel.aspx?no=203"
res = requests.get(url)
soup = BeautifulSoup(res.text, "lxml")

for i in soup.select("#cOneTableC13")[0].select("tr"):
	comp = i.select("a")[0].text.encode("big5", "ignore")
	tel = i.select("td")[4].text.encode("big5", "ignore")
	data.append([comp, tel])




for page in range(1, 385):
	print page
	
	VIEWSTATE = soup.select("#__VIEWSTATE")[0]["value"]
	VIEWSTATEGENERATOR = soup.select("#__VIEWSTATEGENERATOR")[0]["value"]
	PREVIOUSPAGE = soup.select("#__PREVIOUSPAGE")[0]["value"]

	payload = {
		"__EVENTTARGET":"ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$AspxPager1$NextPageText",
		"__VIEWSTATE":VIEWSTATE,
		"__VIEWSTATEGENERATOR":VIEWSTATEGENERATOR,
		"__PREVIOUSPAGE":PREVIOUSPAGE,
		"ctl00$ctl00$iSearTp":"1",
		"ctl00$ctl00$twSearch":"請輸入關鍵字，並可搭配分類進行檢索",
		"ctl00$ctl00$Repeater1$ctl00$NNO":"174",
		"ctl00$ctl00$Repeater1$ctl01$NNO":"60",
		"ctl00$ctl00$Repeater1$ctl02$NNO":"83",
		"ctl00$ctl00$Repeater1$ctl03$NNO":"330",
		"ctl00$ctl00$Repeater1$ctl04$NNO":"101",
		"ctl00$ctl00$Repeater1$ctl05$NNO":"109",
		"ctl00$ctl00$Repeater1$ctl06$NNO":"114",
		"ctl00$ctl00$Repeater1$ctl07$NNO":"123",
		"ctl00$ctl00$Repeater1$ctl08$NNO":"127",
		"ctl00$ctl00$Repeater1$ctl09$NNO":"131",
		"ctl00$ctl00$Repeater1$ctl10$NNO":"138",
		"ctl00$ctl00$Repeater1$ctl11$NNO":"143",
		"ctl00$ctl00$Repeater1$ctl12$NNO":"147",
		"ctl00$ctl00$Repeater1$ctl13$NNO":"154",
		"ctl00$ctl00$Repeater1$ctl14$NNO":"166",
		"ctl00$ctl00$Repeater1$ctl15$NNO":"173",
		"ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$CityState1$County":"請選擇",
		"ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$CityState1$AREA":"請選擇",
		"ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$AspxPager1$tbPageSize":"10",
		"ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$AspxPager1$dlPageJump":page,
		"ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$Pager2$tbPageSize":"10",
		"ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$Pager2$dlPageJump":page
	}
	
	
	url = "http://admin.taiwan.net.tw/travel/travel.aspx?no=203"
	res = requests.post(url, data = payload)
	soup = BeautifulSoup(res.text, "lxml")
		
	for i in soup.select("#cOneTableC13")[0].select("tr"):
		comp = i.select("a")[0].text.encode("big5", "ignore")
		tel = i.select("td")[4].text.encode("big5", "ignore")
		data.append([comp, tel]) 

	time.sleep(3)



with open("tourism_bureau.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)


print "Done!"


