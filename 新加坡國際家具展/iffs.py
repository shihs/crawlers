# -*- coding: utf-8 -*-
#https://www.iffs.com.sg/ 
from bs4 import BeautifulSoup
import requests
import csv

data = []
data.append(["company", "contact name", "contact address", "contact number", "contact email", "contact website", "exhibitor booth"])


# with open("iffs.csv", "w") as f:
# 	f.write("company,contact name,contact address,contact number,contact email,contact website,exhibitor booth" + "\n")


for page in range(26):
	print page
	url = "https://www.iffs.com.sg/exhibitors/page/" + str(page+1) + "/"

	res = requests.get(url)
	soup = BeautifulSoup(res.text, "lxml")
	
	for i in soup.select(".type-exhibitor"):
		comp_info = i.select(".title")[0].select("a")[0]
		
		comp_url = comp_info["href"]
		comp = comp_info.text
		print comp_url
		comp_res = requests.get(comp_url)
		comp_soup = BeautifulSoup(comp_res.text, "lxml")

		comp = comp_info.text.encode(comp_res.encoding, "replace")
		contact_name = comp_soup.select("footer")[0].select(".contact-name")[0].text.encode(comp_res.encoding, "replace")
		contact_address = comp_soup.select("footer")[0].select(".contact-address")[0].text.encode(comp_res.encoding, "replace")
		contact_number = comp_soup.select("footer")[0].select(".contact-number")[0].text.encode(comp_res.encoding, "replace")
		contact_email = comp_soup.select("footer")[0].select(".contact-email")[0].text.encode(comp_res.encoding, "replace")
		contact_website = comp_soup.select("footer")[0].select(".contact-website")[0].text.encode(comp_res.encoding, "replace")
		exhibitor_booth = comp_soup.select("footer")[0].select(".exhibitor-booth")[0].text.encode(comp_res.encoding, "replace").replace("Booth Number:", "").strip()
	
		data.append([comp, contact_name, contact_address, contact_number, contact_email, contact_website, exhibitor_booth])
		# with open("iffs.csv", "a") as f:
		# 	f.write('"' + comp + "','" + contact_name + "','" + contact_address + "','" + contact_number + "','" + contact_email + "','" + contact_website + "','" + exhibitor_booth + '"\n')
		
	
with open("iffs.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)


