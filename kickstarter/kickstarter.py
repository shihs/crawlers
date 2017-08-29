# -*- coding:utf-8 -*-
# 爬取 Kickstarter Taiwan名單 https://www.kickstarter.com/discover/advanced?woe_id=2306179&sort=magic&
import requests
from bs4 import BeautifulSoup
import csv
import json



data = []
data.append(["name", "id", "api", "kickstarter page", "webs"])
page = 0

while True:

	page = page + 1
	print page
	url = "https://www.kickstarter.com/discover/advanced?google_chrome_workaround&woe_id=2306179&sort=magic&seed=2504461&page=" + str(page)
	#print url
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "lxml")

	# 確認該頁是否存在
	if len(soup.select(".js-project-group")[0].select(".js-react-proj-card")) == 0:
		break
	
	for i in soup.select(".js-project-group")[0].select(".js-react-proj-card"):
		
		js = json.loads(i["data-project"])
		
		# 該project api
		api_url = js["creator"]["urls"]["api"]["user"]
		print api_url
		api_res = requests.get(api_url) 
		js = json.loads(api_res.text)
		
		# 該名稱id
		project_id = js["id"]
		# kickstater上名稱
		name = js["name"]
		print name.encode("utf-8", "ignore")
	
		# kickstarter個人頁面
		web = js["urls"]["web"]["user"]
	
		# kickstarter個人資料頁面
		web_res = requests.get(web + "/about")
		web_soup = BeautifulSoup(web_res.text, "lxml")
		
		# kickstarter個人頁面提供的網站
		webs = ""
		if len(web_soup.select(".menu-submenu")) != 0:
			for j in web_soup.select(".menu-submenu")[0].select("li"):
				webs = webs + j.select("a")[0]["href"] + "\n"
			webs = webs.strip()
	
		data.append([name.encode("utf-8", "ignore"), project_id, api_url, web, webs])
	
with open("kickstarter.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)



