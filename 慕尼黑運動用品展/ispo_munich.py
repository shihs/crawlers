# -*- coding: utf-8 -*-
# 爬取 2017年德國 ispo munich 慕尼黑運動用品展 參展廠商
# http://www.ispo-mediaservices.com/onlinecatalog/2017/Exhibitorlist?
from bs4 import BeautifulSoup
import requests
import csv


data = []


url = "http://www.ispo-mediaservices.com/onlinecatalog/2017/Exhibitorlist?"

page = 0
payload = {
	"LNG":"2",
	"nv":"1.2",
	"rqt_useScfListCaching":"yes",
	"MKID":"",
	"xMKID":"",
	"sb_c":"15",
	"sb_m":"1100",
	"sb_n":"suche",
	"sb_s":"",
	"once_sb_additionalFields":"50",
	"pag_styp":"4",
	"sb_useBondedCharactMode":"",
	"sb1":"taiwan",
	"sb1_n":"suche",
	"sb2":"ex",
	"sb2_n":"bereiche",
	"tmp_ListingRows":"60",
	"tmp_ListingType":"ext",
	"tmp_PrintType":"no",
	"tmp_pag_styp":"4",
	"StartRow_query_res_2":"61",
	"SRFieldtext":"text",
	"StartRow_query_res_text":page,
	"StartRow_query_res_5":"241",
	"StartRow_query_res_first":"1",
	"StartRow_query_res_previous":"1",
	"StartRow_query_res_next":"121",
	"StartRow_query_res_last":"241",
	"StartRow_query_res_nextSet":"241",
	"StartRow_query_res_previousSet":"1",
	"Previous_PageNumber_query_res":"2",
	"rqt_pagingQuery":"query_res",
	"rqt_pagingDef":"60"
}



while True:
	page = page + 1

	# playload頁數參數
	payload["StartRow_query_res_text"] = str(page)

	res = requests.post(url, data = payload)
	soup = BeautifulSoup(res.text, "html.parser")

	# 如果已抓取過則停止
	if page != 1:
		if check_company == soup.select(".jl_lexname")[1]:
			break
	# 該頁第一筆公司名稱([0]為廣告)
	check_company = soup.select(".jl_lexname")[1]


	for i in soup.select(".jl_lexname"):
		print i.text.encode("utf-8", "ignore")
		data.append([i.text.encode("utf-8")])

	
with open("ispo_numich.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)


