# -*- coding: utf-8 -*-
# 新北市鞋類商業同業公會
from bs4 import BeautifulSoup
import requests
import csv
import time


data = []
data.append(["company", "tel"])

url = "http://www.footwearnet.org.tw/member.aspx"

header = {
	"Cookie":"ASP.NET_SessionId=pwjdk4hz4lcxqmugqrwvkn5e; lang=zh"
}

res = requests.get(url, headers = header)
soup = BeautifulSoup(res.text, "lxml")

for i in soup.select(".MemberList")[0].select("tr"):
	comp = i.select("td")[2].text.encode("big5", "utf-8")
	tel = i.select("td")[3].text.encode("big5", "utf-8")
	print comp, tel
	data.append([comp, tel])



with open("footwearnet.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)


print "DONE!"


