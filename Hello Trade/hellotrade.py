# -*- coding: utf-8 -*-
# Hello Trade(http://www.hellotrade.com/) crawler
from bs4 import BeautifulSoup 
import requests
import csv
import time
import random
import urllib




def get_proxies(file_name):
    ips = dict()
    with open(file_name, "r") as f:
        data = f.readlines()
        for ip in data:
            proxy = ip.split(",")
            ips[proxy[0]] = proxy[1]

    return ips



ips = get_proxies("ips.csv")
proxy = random.choice(ips.keys())
proxies = {"http":"http://"+proxy}


orginal_url = "http://www.hellotrade.com"
url = "http://www.hellotrade.com/business/"

s = requests.Session()

data = []
data.append(["company", "tel"])


headers = {
	"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
}


while True:
	try:
		print proxies
		print url
		res = requests.get(url, headers = headers, timeout = 30, proxies = proxies)
		soup = BeautifulSoup(res.text, "lxml")

		if len(soup.select(".ct-rbx")) == 0:
			ips.pop(proxy, None)
			proxy = random.choice(ips.keys())
			proxies = {"http":"http://"+proxy}
			continue

		break
	except:
		ips.pop(proxy, None)
		proxy = random.choice(ips.keys())
		proxies = {"http":"http://"+proxy}
	


comps = set()

# large categories
for i in soup.select(".ct-rbx"):
	# small categories
	for j in i.select("a"):
		taiwan = True
		time.sleep(random.randint(3, 5))
		category_url = orginal_url + j["href"] + "&country=taiwan"
		print category_url
		while True:
			try:
				time.sleep(5)
				category_res = requests.get(category_url, headers = headers, timeout = 30, proxies = proxies)
				# 確認網址導向是否有台灣supplier的頁面
				print category_res.url
				if "taiwan" not in category_res.url:
					print "There's no Taiwan company in this categroy."
					taiwan = False
					break

				category_soup = BeautifulSoup(category_res.text, "lxml")
				comp_name = category_soup.select(".comp-name")

				if len(comp_name) == 0:
					ips.pop(proxy, None)
					proxy = random.choice(ips.keys())
					proxies = {"http":"http://"+proxy}
					print proxies
					continue

				break
			except Exception as e:
				with open("hellotrade.csv", "ab") as f:
					w = csv.writer(f)
					w.writerows(data)
					data = []
				print "oops"
				print e
				# time.sleep(5)
				ips.pop(proxy, None)
				proxy = random.choice(ips.keys())
				proxies = {"http":"http://"+proxy}
				print proxies

		if not taiwan:
			continue
		
		for comp in comp_name:
			comp = comp.select("a")[0]["href"]

			if comp in comps:
				continue

			comps.add(comp)

			comp_url = orginal_url + comp + "contact.html"
			print comp_url
			time.sleep(random.randint(4, 6))
			
			while True:
				try:					
					time.sleep(5)
					comp_res = requests.get(comp_url, headers = headers, timeout = 30, proxies = proxies)
					comp_soup = BeautifulSoup(comp_res.text, "lxml")
					comp = comp_soup.select(".cname")[0].text
					break
				except Exception as e:
					with open("hellotrade.csv", "ab") as f:
						w = csv.writer(f)
						w.writerows(data)
						data = []
					print "oops"
					print e
					ips.pop(proxy, None)
					proxy = random.choice(ips.keys())
					proxies = {"http":"http://"+proxy}
					print proxies
	
			print comp
			try:
				tel = comp_soup.select(".con-phone")[0].text.replace("+(886)", "").replace("-", "")
			except:
				tel = ""
			# print tel

			data.append([comp, tel])
			print "Append " + comp


	# 		break
	# 	break
	# break



with open("hellotrade.csv", "ab") as f:
	w = csv.writer(f)
	w.writerows(data)

print "Done!"
