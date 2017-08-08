# -*- coding: utf-8 -*-
#2017台北世貿半導體展
from bs4 import BeautifulSoup
import requests
import csv



with open("semicon_2017.csv", "w") as f:
	f.write("company" + "\n")


# url = "http://www.semicontaiwan.org/zh/exhibitor-list"

url = "http://expo.semi.org/taiwan2017/public/exhibitors.aspx?ID=18157&sortMenu=102000&langID=2&__hstc=268175441.db6318ec1ee5b9ec37384346bc900344.1501746643988.1501746643988.1501746643988.1&__hssc=268175441.1.1501746643988&__hsfp=2595774326"


res = requests.get(url)

soup = BeautifulSoup(res.text, "html.parser")


for exhibitor in soup.select(".exhibitorName"):
	company = exhibitor.text.encode("big5", "ignore")
	
	with open("semicon_2017.csv", "a") as f:
		f.write('"' + company + '"\n')





