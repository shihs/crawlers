# -*- coding: utf-8 -*-
#爬取台灣精品得獎名單http://www.taiwanexcellence.org/index.php/awards/now/cross_list/1/2017/2/1
from bs4 import BeautifulSoup
import requests
import csv
import math


company_url_set = set()
data = []
data.append(["GUI", "company", "tel", "address", "web"])
count = 0

url = "http://www.taiwanexcellence.org/index.php/awards/now/send_search/1/2017/2/1/cross_list"


payload = {
	"keyword":"",
	"awards[0]":"1",
	"awards[1]":"2",
	"awards[2]":"3",
	"years[0]":"2017",
	"years[1]":"2016",
	"industry[0]":"A",
	"industry[1]":"B",
	"industry[2]":"C",
	"industry[3]":"D",
	"industry[4]":"E",
	"industry[5]":"F",
	"industry[6]":"G",
	"industry[7]":"H",
	"industry[8]":"I",
	"industry[9]":"J",
	"industry[10]":"K",
	"industry[11]":"L",
	"industry[12]":"Z"
}


s = requests.Session()
res = s.post(url, data = payload)
soup = BeautifulSoup(res.text, "lxml")

# 搜尋結果筆數，每一頁有8筆，計算需要爬取的頁數
total_page = int(math.ceil(int(soup.select(".shiSearchResults")[0].select("strong")[1].text)/8.0))
print total_page


for page in range(total_page):
	url = "http://www.taiwanexcellence.org/index.php/awards/now/append_list/1/2017/" + str(page+1) + "/2/cross_list"
	res = s.get(url)
	
	soup = BeautifulSoup(res.text, "lxml")
	
	for i in soup.select(".boutique-item"):
		j = i.select(".company")[0]
		# print j
	
		company = j.text.encode("big5", "ignore")
		company_url = j.select("a")[0]["href"]
		GUI = company_url.replace("http://www.taiwanexcellence.org/index.php/awards/company/index/1/", "")
	
		# 若該公司已爬取過擇跳過
		if company_url in company_url_set:
			continue
		else:
			company_url_set.add(company_url)

		# 爬取公司資訊
		try:
			company_res = requests.get(company_url, timeout = 30)
			company_soup = BeautifulSoup(company_res.text, "html.parser")
	
		except:
			with open("taiwanexcellence.csv", "ab") as f:
				w = csv.writer(f)
				w.writerows(data)
				data = []
				continue
	
		try:
			tel = company_soup.select(".contact")[0].select("p")[1].text.encode("big5", "ignore").replace("電話:".decode("utf-8").encode("big5"), "").strip()
			web = company_soup.select(".contact")[0].select("p")[4].text.encode("big5", "ignore").replace("網址".decode("utf-8").encode("big5"), "").strip()
			address = company_soup.select(".contact")[0].select("p")[5].text.encode("big5", "ignore").replace("地址".decode("utf-8").encode("big5"), "").strip()
	
		# print company, tel, address
	
		except:
			tel = ""
			address = ""
	
		data.append([GUI, company, tel, address, web])
	
		print count 
		count = count + 1
		print company_url
	
with open("taiwanexcellence.csv", "ab") as f:
	w = csv.writer(f)
	w.writerows(data)

print "finished"