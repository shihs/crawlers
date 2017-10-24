# -*- coding: utf-8 -*-
# 爬取B2B Mit廠商 http://www.b2bmit.com/
from bs4 import BeautifulSoup
import requests
import csv
import time





def crawl_company(url):
	
	data = []

	# 台灣廠商
	url = url + "?coun_id=1778470648"
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "lxml")

	if len(soup.select(".sorryTitle")) != 0:
		return

	for i in soup.select(".main"):
		tel = ""
		contact_person = ""
		comp = i.select("h3")[0].select("a")[0].text.encode("utf-8")
		info_url = "http://www.b2bmit.com/" + i.select("h3")[0].select("a")[0]["href"]
		print comp
		info_res = requests.get(info_url)
		info_soup = BeautifulSoup(info_res.text, "lxml")

		if len(info_soup.select(".tel")) != 0:
			tel = info_soup.select(".tel")[0].text.encode("utf-8")

		l = len(info_soup.select(".txt"))-1
		contact_person = info_soup.select(".txt")[l].text.replace(info_soup.select(".txt")[l].select("h1")[0].text, "").strip().encode("utf-8")
		data.append([comp, tel, contact_person])

	return data



def main():
	count = 0

	data = []
	data.append(["company", "tel", "contact_person"])
	
	url = "http://www.b2bmit.com/category/agriculture.htm"
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "lxml")
	

	# 大分類
	for i in soup.select(".aside")[0].select("li"):

		large_category_url =  "http://www.b2bmit.com"+ i.select("a")[0]["href"]	
		large_category_res = requests.get(large_category_url)
		large_category_soup = BeautifulSoup(large_category_res.text, "lxml")
		
		# 中分類
		for j in large_category_soup.select(".cateBox2")[0].select("h3"):
	
			try:
				mid_category_url = "http://www.b2bmit.com" + j.select("a")[0]["href"]
				mid_category_res = requests.get(mid_category_url)
				mid_category_soup = BeautifulSoup(mid_category_res.text, "lxml")
			except:
				continue

			# 中分類後可能有小分類，可能沒有
			# 有小分類
			try:
				if len(mid_category_soup.select(".cateBox2")) != 0: 
					for k in mid_category_soup.select(".cateBox2")[0].select("h3"):
						# small_category = j.text.encode("utf-8")
						small_category_url = "http://www.b2bmit.com" + k.select("a")[0]["href"]
						print small_category_url
						d = crawl_company(small_category_url)
						
						if d == None:
							continue
						
						data.extend(d)
	
						time.sleep(0.5)
		
				# 沒有小分類
				else:
					print mid_category_url
					d = crawl_company(mid_category_url)
					if d == None:
						continue
		
					data.extend(d)
			except:
				continue

			time.sleep(5)


			if len(data) >= 300:
				with open("mit.csv", "ab") as f:
					w = csv.writer(f)
					w.writerows(data)
					data = []
			# break
		# break


	with open("mit.csv", "ab") as f:
		w = csv.writer(f)
		w.writerows(data)

	print "DONE!"
		






if __name__ == '__main__':
 	main()



