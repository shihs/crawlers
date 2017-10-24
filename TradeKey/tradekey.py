# -*- coding: utf-8 -*-
# tradekey廠商名單 http://www.tradekey.com/
from bs4 import BeautifulSoup
import requests
import csv


data = []
data.append(["company", "contact person", "tel"])

for page in range(26):

	url = "http://www.tradekey.com/search/index.html?action=profile_search&criteria=2&keyword=taiwan&start_date=0&country=192&track=prlist__c_&page_no=" + str(page + 1)
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "lxml")
	
	for i in soup.select(".title"):
		comp = i.text.encode("utf-8")
		print comp
		comp_url = i["href"]
		begin = comp_url.rfind("-")
		end = comp_url.find(".html")	
		# company info url
		comp_url = "http://www.tradekey.com/profile_contact/uid/" + comp_url[(begin+1):end] + "/" + comp_url[(comp_url.rfind("/")+1):begin] + ".htm"
		print comp_url
	
		comp_res = requests.get(comp_url)
		
		with open("Output.txt", "w") as text_file:
			text_file.write(comp_res.text.encode(res.encoding))
		comp_soup = BeautifulSoup(open("Output.txt"), "html.parser")
		
		contact_person = comp_soup.select(".contact-info")[0].select(".ci-details")[0].select("p")[0].text.strip().replace(" ", "")
		tel = comp_soup.select(".contact-info")[0].select(".ci-details")[3].select("p")[0].text.strip().replace(" ", "")
	
		# print contact_person, tel
		data.append([comp, contact_person, tel])
		# break
	

with open("tradekey.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

	

print "FINISHED!"