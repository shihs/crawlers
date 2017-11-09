# -*- coding: utf-8 -*-
# 爬取 EC21 https://www.ec21.com/ 台灣廠商
from bs4 import BeautifulSoup
import requests
import csv
import time
import random
import string




COMPs = set()
data = []
data.append(["company", "tel", "contact_person"])


key_latest = "key"
try_time = 0

# 依字母搜尋
for alpha in string.ascii_lowercase:
	alpha_page = 1

	# 字母頁數
	while True:		
		url = "https://www.ec21.com/ec-market/TW/index/" + alpha + "/page-" + str(alpha_page) + ".html"
		print url
		
		# 字母底下的分類
		try:
			res = requests.get(url)
			if res.status_code != 200:
				with open("EC21.csv", "ab") as f:
					w = csv.writer(f)
					w.writerows(data)
				break

			soup = BeautifulSoup(res.text, "lxml")

		except requests.ConnectionError:
			with open("EC21.csv", "ab") as f:
				w = csv.writer(f)
				w.writerows(data)

			try_time += 1
			data = []

			if try_time == 15:
				break
			time.sleep(30)
		
		except:
			break
	
		# 是否為最後一頁
		if len(soup.select(".big_msg2")) != 0:
			break
		
		# 字母關鍵字
		for alpha_categroy in soup.select(".mf_key_list")[0].select("a"):
			# 關鍵字
			key = alpha_categroy["href"].replace("ec-market", "companies").replace(".html", "")[34:].strip()

			# 關鍵字是否包含之前的關鍵字內容	
			if key_latest in key:
				continue
			key_latest = key			

			# 字母關鍵字頁數
			page = 1
			while True:
				key_url = "https://www.ec21.com/companies/TW/" + key + "/page-" + str(page) + ".html"
				print key_url

				print "Alpha:" + alpha + ", page:" + str(alpha_page) + "; Key:" + key + ", page:" + str(page)
				
				try:
					key_res = requests.get(key_url)
					if key_res.status_code != 200:
						with open("EC21.csv", "ab") as f:
							w = csv.writer(f)
							w.writerows(data)
						break
					key_soup = BeautifulSoup(key_res.text, "lxml")
				except requests.ConnectionError:
					with open("EC21.csv", "ab") as f:
						w = csv.writer(f)
						w.writerows(data)
					data = []
					time.sleep(30)
				except:
					break
		
				# no result
				if len(key_soup.select(".key_msg_view")) != 0:
					break
	
				# 公司info
				for comp_tag in key_soup.select(".inlineTitle"):
					comp = comp_tag.text.encode("utf-8", "ignore")
	
					# 公司是否爬取過
					if comp in COMPs:
						continue
					print comp
					COMPs.add(comp)
	
					# 公司info網址
					comp_url = comp_tag.select("a")[0]["href"] + "company_contact_info.html"
					print comp_url
		
					try:
						comp_res = requests.get(comp_url)
						if comp_res.status_code != 200:
							with open("EC21.csv", "ab") as f:
								w = csv.writer(f)
								w.writerows(data)
							break
						comp_soup = BeautifulSoup(comp_res.text, "lxml")

					except requests.ConnectionError:
						with open("EC21.csv", "ab") as f:
							w = csv.writer(f)
							w.writerows(data)
						data = []
						time.sleep(30)
					except:
						break

					tel = ""
					contact_person = ""
					try:
						tel = comp_soup.select(".t_itc3")[3].select(".txt")[0].text.encode("utf-8", "ignore").strip().replace("\n", "").replace("	", "").replace(" ", "")
						contact_person = comp_soup.select(".t_itc3")[-1].select(".txt")[0].text.encode("utf-8", "ignore").strip()
					except:
						data.append([comp, tel, contact_person])

					data.append([comp, tel, contact_person])

					time.sleep(1)
	
				# 檢查是否有下一頁
				if len(key_soup.select(".bt_pr")) == 0:
					break

				# 字母關鍵字下一頁
				page += 1

				time.sleep(random.randint(3, 5))

			time.sleep(random.randint(3, 8))
			
		# 字母下一頁
		alpha_page += 1

		time.sleep(random.randint(10, 15))








with open("EC21.csv", "ab") as f:
	w = csv.writer(f)
	w.writerows(data)

print "DONE!"









