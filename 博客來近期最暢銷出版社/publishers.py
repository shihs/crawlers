# -*- coding: utf-8 -*-
# http://www.monster101.com/publishers 博客來近期最暢銷出版社名單
from bs4 import BeautifulSoup
import requests
import csv




url = "http://www.monster101.com/publishers"
res = requests.get(url)

soup = BeautifulSoup(res.text, "lxml")

publishers_set = set()

for i in soup.select(".bookdetail"):
	print i.text.encode("utf-8")
	publishers_set.add(i.text.encode("big5", "ignore"))


data = []
data.append(["publishers"])

for i in publishers_set:
	data.append([i])



with open("publishers.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)
