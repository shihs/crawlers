# -*- coding: utf-8 -*-
# 爬取 2017年莫斯科Mosbuild國際建材暨家飾展 參展廠商
# http://www.worldbuild-moscow.ru/en-GB/about/exhibitor-list.aspx  # 2017
# http://www.worldbuild-moscow.ru/en-GB/about/exhibitor-list/exhibitor-list.aspx  # 2016
from bs4 import BeautifulSoup
import requests
import csv




def parameters(soup, doPostBack):
	'''獲取台灣廠商名單jsp所需的參數

	Args:
		soup: 上一頁的soup，含有下一頁的參數
		doPostBack: jsp的參數字串

	Return:
		payload的三個參數: __EVENTTARGET, __EVENTARGUMENT, __VIEWSTATE 

	'''

	begin = doPostBack.find("'") + 1
	end = doPostBack.find("','")
	
	__EVENTTARGET = doPostBack[begin:end]
	
	begin = end
	end = doPostBack.find("')")
	__EVENTARGUMENT = doPostBack[begin+3:end]

	# viewstate
	__VIEWSTATE = soup.select("#__VIEWSTATE")[0]["value"]

	return __EVENTTARGET, __EVENTARGUMENT, __VIEWSTATE



def crawler(__EVENTTARGET, __EVENTARGUMENT, __VIEWSTATE, data):
	''' 爬取該頁面的廠商名單
	Args:
		__EVENTTARGET, __EVENTARGUMENT, __VIEWSTATE: 三個payload參數
		data: 儲存廠商名稱的list

	Return:
		data: 儲存廠商名稱的list
		soup: 該頁面的soup

	'''
	payload = {
		"__EVENTTARGET":__EVENTTARGET,
		"__EVENTARGUMENT":__EVENTARGUMENT,
		"p$lt$ctl12$pageplaceholder$p$lt$ctl02$FilterExhibitorList$filterControl$ddlCountries":"220",  # Taiwan
		"__VIEWSTATE":__VIEWSTATE
	}

	# print payload
	res = s.post(url, data = payload)
	soup = BeautifulSoup(res.text, "html.parser")

	for i in soup.select(".showframe"):
		data.append([i.text])
		print i.text

	return data, soup




data = []

# 廠商名單首頁
#url = "http://www.worldbuild-moscow.ru/en-GB/about/exhibitor-list.aspx"
url = "http://www.worldbuild-moscow.ru/en-GB/about/exhibitor-list/exhibitor-list.aspx"
s = requests.Session()
res = s.get(url)
soup = BeautifulSoup(res.text, "html.parser")

# jsp參數
doPostBack = soup.select(".btn-container")[0].select("a")[0]["href"]
# 獲取台灣廠商名單jsp所需的參數
__EVENTTARGET, __EVENTARGUMENT, __VIEWSTATE = parameters(soup, doPostBack)
data, soup = crawler(__EVENTTARGET, __EVENTARGUMENT, __VIEWSTATE, data)

# 廠商名單頁數
link = soup.select(".link")


for i in link:
	__EVENTTARGET, __EVENTARGUMENT, __VIEWSTATE = parameters(soup, i["href"])
	data, soup = crawler(__EVENTTARGET, __EVENTARGUMENT, __VIEWSTATE, data)



with open("mosbuild_2016.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)




