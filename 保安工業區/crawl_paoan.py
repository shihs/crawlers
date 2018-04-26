# -*- coding: utf-8 -*-
#爬取http://www.pao-an.org.tw/company/selcom.asp 保安工業區
import requests
from bs4 import BeautifulSoup
import csv



url = "http://www.pao-an.org.tw/company/selcom.asp"

res = requests.get(url)
print res.encoding
soup = BeautifulSoup(res.text, "html.parser")

pages = int(soup.select("select")[2].select("option")[-1].text)

data = []
data.append(["zone", "company", "tel", "address"])
for page in range(pages):
	url = "http://www.pao-an.org.tw/company/selcom.asp?page=" + str(page+1)
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "html.parser")
	for j in soup.select("tr")[5:]:
		if len(j.select("table")) != 0:
			if len(j.select("table")[0].select("td")) == 10:
				company = j.select("table")[0].select("td")[1].text.encode(res.encoding, "ignore")#.decode("utf-8", "ignore").encode("big5", "ignore")
				tel = j.select("table")[0].select("td")[2].text.encode(res.encoding, "ignore")[4:]#.decode("utf-8", "ignore").encode("big5", "ignore")
				address = j.select("table")[0].select("td")[4].text.encode(res.encoding, "ignore").strip()#.decode("utf-8", "ignore").encode("big5", "ignore")
				data.append(["保安工業區".decode("utf-8").encode("big5"), company, tel, address])

# print data

f = open("paoan.csv", "wb")
w = csv.writer(f)
w.writerows(data)
f.close()