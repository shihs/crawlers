# -*- coding: utf-8 -*-
# 爬取手提包輸出同業公會 http://www.bags.org.tw/factory/factory01.php
from bs4 import BeautifulSoup
import requests
import csv


data = []
data.append(["GUI"])


for page in range(14):
  #url = "http://www.bags.org.tw/factory/factory01.php"
  url = "http://www.bags.org.tw/factory/factory01.php?show=" + str(page*8) + "&total=106&searchsql2=YTo5OntzOjg6ImRvYWN0aW9uIjtzOjY6IlNFQVJDSCI7czoyOiJJRCI7czowOiIiO3M6NjoiQ09NUElEIjtzOjA6IiI7czoyMToiQkFHX1RXTl9DT1VOVFlaT05FX0lEIjtzOjA6IiI7czoxMjoiQ09NUE9XTkJSQU5EIjtzOjA6IiI7czoxMDoiQ09NUENITkFNRSI7czowOiIiO3M6MTA6IkNPTVBFTk5BTUUiO3M6MDoiIjtzOjc6ImltYWdlX3giO3M6MToiOSI7czo3OiJpbWFnZV95IjtzOjE6IjciO30=#"
  res = requests.get(url)
  soup = BeautifulSoup(res.text, "lxml")

  for i in soup.select("a")[:8]:

    if "VIEW" not in i["href"]:
      break
  
    comp_url = "http://www.bags.org.tw/factory/" + i["href"]
    comp_res = requests.get(comp_url)
    # print comp_res.encoding
    comp_soup = BeautifulSoup(comp_res.text, "lxml")
    print comp_soup.select(".fashion1")[0].text.encode("utf-8")
    data.append([comp_soup.select(".fashion1")[0].text.encode("utf-8")])


with open("bags.csv", "wb") as f:
    w = csv.writer(f)
    w.writerows(data)

