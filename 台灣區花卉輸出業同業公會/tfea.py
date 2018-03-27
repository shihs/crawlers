# -*- coding: utf-8 -*-
# http://tfea.tfea.org.tw/front/bin/home.phtml 台灣區花卉輸出業同業公會
from bs4 import BeautifulSoup
import requests
import csv








def get_company_info(soup, data):	
	for i in soup.select(".pt-tblist-tb")[0].select("tr")[1:]:
		# print "here"
		try:
			comp_url = "http://tfea.tfea.org.tw/front/bin/" + i.select("td")[0].select("a")[0]["href"]
			comp_res = requests.get(comp_url)
			comp_soup = BeautifulSoup(comp_res.text, "lxml")
			# print comp_res.text.encode("utf-8")
			info = comp_soup.select(".ptdet-text")[0].select("tr")
	
			comp = info[0].select("span")[0].text.encode(comp_res.encoding).decode("utf-8", "ignore").encode("big5", "ignore").strip()
			tel = info[1].select("td")[1].text.encode(comp_res.encoding).decode("utf-8", "ignore").encode("big5", "ignore").strip()
			# print comp, tel
			data.append([comp, tel])

		except Exception as e:
			# print e
			data.append([i.select("td")[0].text.encode(comp_res.encoding).decode("utf-8", "ignore").encode("big5", "ignore").strip(), ""])
			# print i.select("td")[0].select("a")[0]["href"]#i.text.encode(res.encoding).decode("utf-8", "ignore").encode("utf-8", "ignore").strip()

	payload = {}
	for i in soup.select("form")[-1].select("input"):
		# print i["name"]
		try:
			payload[i["name"]] = i["value"]
		except:
			payload[i["name"]] = "Next"

	return payload, data
	




if __name__ == "__main__":

	data = []
	data.append(["compnay", "tel"])
	
	url = "http://tfea.tfea.org.tw/front/bin/ptlist.phtml?Category=3"
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "lxml")
	
	
	payload, data = get_company_info(soup, data)
	print payload
	# print data

	# headers = {
	# 	"Referer":"http://tfea.tfea.org.tw/front/bin/ptlist.phtml?Category=3"
	# }

	while True:
		url = "http://tfea.tfea.org.tw/front/bin/ptlist.phtml"
		res = requests.post(url, data = payload)
		# print res.text.encode(res.encoding).decode("utf-8", "ignore").encode("utf-8", "ignore")
		soup = BeautifulSoup(res.text, "lxml")

		payload, data = get_company_info(soup, data)
		print payload

		if payload["Curpage"] == payload["Totalpage"]:
			break
		# break
	



	with open("tfea.csv", "wb") as f:
		w = csv.writer(f)
		w.writerows(data)


