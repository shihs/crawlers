# -*- coding: utf-8 -*-
# 台北市進出口商業同業公會

from bs4 import BeautifulSoup 
import urllib
import requests
import csv
import json





url = "http://www.ieatpe.org.tw/qry/query.aspx"
s = requests.Session()
s.get(url)

data = []
data.append(["company", "tel", "hscode", "hscode name", "io", "country"])


for category in range(1, 98):
	print category

	payload = {
		"qry":'{"type":3,"flow":"","input":"' + str(category).zfill(2) + '"}'
	}

	res = s.post(url, data = payload)
	js = json.loads(res.text)

	for nos in js:
		no = nos["no2"]
		print no

		payload_no = {
			"qry":'{"type":5,"input":"' + no + '"}'
		}

		res_no = s.post(url, data = payload_no)
		js_no = json.loads(res_no.text)

		for comps in js_no:
			comp_id = comps["id"]
			print comp_id

			payload_id = {
				"detl":'{"input":"' + comp_id + '"}'
			}

			res_id = s.post(url, data = payload_id)
			js_id = json.loads(res_id.text)

			for comp_info in js_id:
				tel = comp_info["tel"].replace(" ", "").encode("big5", "ignore")
				comp = comp_info["Cname"].encode("big5", "ignore")
				# print comp
				io = comp_info["obj"]
				# print io
				for io_info in io:
					eie = io_info["eie"].encode("big5", "ignore")
					ectr = io_info["Ectr"].encode("big5", "ignore")
					hscode = io_info["no"].encode("big5", "ignore")
					try:
						hscode_name = io_info["Cname"].encode("big5", "ignore")
					except:
						hscode_name = ""
					# print hscode, eie, ectr

					data.append([comp, tel, hscode, hscode_name, eie, ectr])
	# 		break
	# 	break
	# break




with open("ieatpe_io.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

print "DONE!"
