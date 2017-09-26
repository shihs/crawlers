# -*- coding: utf-8 -*-
# 台北市進出口商業同業公會會員名單 http://www.ieatpe.org.tw/en/member.html
import requests
import csv
import json



data = []
data.append(["company", "address"])


url = "http://www.ieatpe.org.tw/en/data/member.ashx?qry=%7B%22type%22%3A1%2C%22input%22%3A%22%22%7D"
res = requests.get(url)

companies = res.text.encode("utf-8", "ignore")
companies = json.loads(companies)

page = 0

for i in companies:
	page += 1
	print page, i["name"]
	data.append([i["name"], i["addr"]])



with open("ieatpe.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

