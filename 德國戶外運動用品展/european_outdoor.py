# -*- coding: utf-8 -*-
# 2016年德國European Outdoor戶外活動用品展
# http://www.outdoor-show.com/od-en/
from bs4 import BeautifulSoup
import requests
import csv
import re


data = []
data.append(["company", "tel", "contact person", "contact person title", "contact person tel"])

url = "http://www.outdoor-show.com/od-en/index-of-exhibitors/?m=es&halle=&hs=&firm=&city=&land=Taiwan"


res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")

# company name
for i in soup.select(".listHeadline"):
	row = []
	# company name
	company = i.text.encode("utf-8")
	print company
	row.append(company)

	# company infomaion page 
	company_id = i.select("a")[0]["href"]
	url_company = "http://www.outdoor-show.com/od-en/index-of-exhibitors/" + company_id
	res_company = requests.get(url_company)

	soup = BeautifulSoup(res_company.text, "html.parser")

	# 有公司聯絡人資訊
	if len(soup.select(".elementKontakt")) == 2:
		i = soup.select(".elementKontakt")[1]

	# 無公司聯絡人資訊
	else:
		i = soup.select(".elementKontakt")[0]
	pos_1 = i.select(".contactleft")[0].text.find("\n", 2)			
	pos_2 = i.select(".contactleft")[0].text.find("\n", pos_1+1)			
	pos_3 = i.select(".contactleft")[0].text.find("\n", pos_2+1)			
	pos_4 = i.select(".contactleft")[0].text.find("\n", pos_3+1)
	phone = i.select(".contactleft")[0].text[pos_3:pos_4].replace("Phone:", "").strip().replace("=", "+")
	print phone
	row.append(phone)
	print 
		
	# parse公司聯絡人資訊
	if len(soup.select(".elementKontakt")) == 2:
		i = soup.select(".elementKontakt")[0]

		# 電話
		pos_1 = i.select(".contactleft")[0].text.find("Phone:")
		pos_2 = i.select(".contactleft")[0].text.find("Fax:")
		phone = i.select(".contactleft")[0].text[pos_1+6:pos_2].strip()		
		if pos_2 == -1:
			pos = re.search("[a-z]", phone).start()
			phone = phone[:pos]
		print phone
		
		# 聯絡人
		pos_1 = str(i.select(".contactleft")[0]).find('left">')
		pos_2 = str(i.select(".contactleft")[0]).find("<br/>")
		contact_person = str(i.select(".contactleft")[0])[pos_1+6:pos_2].strip()
		print contact_person
		
		# 聯絡人職稱
		pos_3 = str(i.select(".contactleft")[0]).find("<br/>", pos_2+1)
		title = str(i.select(".contactleft")[0])[pos_2+5:pos_3].strip()
		if title.find("Phone") != -1:
			title = ""
		print title

		print
		row.append(contact_person)
		row.append(title)
		row.append(phone)		

	data.append(row)

with open("european_outdoor.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

