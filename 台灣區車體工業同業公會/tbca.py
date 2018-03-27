# -*- coding: utf-8 -*-
# http://www.tbca.com.tw/index.php 台灣區車體工業同業公會
from bs4 import BeautifulSoup
import requests
import csv



data = []
data.append(["company"])


for page in range(9):
    url = "http://www.tbca.com.tw/member.php?pageNum_RecAlbum=" + str(page)

    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")

    for i in soup.select(".font-mem02"):
        data.append([i.text.encode(res.encoding, "ignore")])




with open("tbca.csv", "wb") as f:
    w = csv.writer(f)
    w.writerows(data)

