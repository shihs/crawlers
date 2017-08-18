# -*- coding: utf-8 -*-
# http://b2b.ifa-berlin.com/
from bs4 import BeautifulSoup
import requests
import csv



data = []
data.append(["company", "tel", "contact_person", "exportregions"])


for page in range(4):

	url = "https://www.virtualmarket.ifa-berlin.de/en/search?country%5B0%5D=593975&itemtype=company&page=" + str(page+1)

	res = requests.get(url)
	soup = BeautifulSoup(res.text, "lxml")

	for i in soup.select(".ngn-search-results")[0].select(".ngn-content-box-title"):
		company = i.text.encode("utf-8").strip()
		print company
		
		comp_url = "https://www.virtualmarket.ifa-berlin.de" + i.select("a")[0]["href"]
		# print comp_url
		comp_res = requests.get(comp_url)
		comp_soup = BeautifulSoup(comp_res.text, "lxml")

		tel = ""
		if len(comp_soup.select(".ngn-table")) != 0:
			if comp_soup.select(".ngn-table")[0].select("td")[0].text == "Phone:":
				tel = comp_soup.select(".ngn-table")[0].select("a")[0].text
				# print tel

		contact_person = ""
		for j in comp_soup.select(".ngn-content-box-wrapper")[1:]:
			contact_person = contact_person + j.select(".ngn-content-box-title")[0].text.encode("big5", "ignore").strip() + "/\n"
		contact_person = contact_person.strip()
		# print contact_person

		exportregions = ""
		if len(comp_soup.select("#exportregions")) != 0:
			for j in comp_soup.select(".ngn-is-pulldown-content")[-2].select(".ngn-content-box"):
				exportregions = exportregions + j.select("p")[0].text.encode("big5", "ignore").strip() + "\n"
		exportregions = exportregions.strip()
		# print exportregions

		data.append([company, tel, contact_person, exportregions])



with open("ifa.csv", "wb") as f:
		w = csv.writer(f)
		w.writerows(data)

	