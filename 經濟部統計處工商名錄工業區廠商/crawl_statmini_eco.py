# -*- coding: utf-8 -*-
#抓取經濟部統計處工商名錄所有工業區廠商名單，並將每個工業區儲存成一份檔案
#https://dmz9.moea.gov.tw/gmweb/investigate/InvestigateFactory.aspx

import requests
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()
import csv
import os
from shutil import copyfileobj  # 下載檔案



url = "https://dmz9.moea.gov.tw/gmweb/investigate/InvestigateFactory.aspx"

s = requests.Session()

#先抓取所有工業區代碼並儲存
if not os.path.exists("../data/zone/zone_value.csv"):
	print "zone_value.csv dosen't exist!"
	headers = {
		"Accept":"*/*",
		"Accept-Encoding":"gzip, deflate",
		"Accept-Language":"zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4",
		"Cache-Control":"no-cache",
		"Connection":"keep-alive",
		# "Content-Length":"24966",
		"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
		"Cookie":"_ga=GA1.3.583926227.1474874583; ASP.NET_SessionId=gzqgvqgj0xhzqlzjhbzy0bw0",
		"Host":"dmz9.moea.gov.tw",
		"Origin":"https://dmz9.moea.gov.tw",
		"Pragma":"no-cache",
		"Referer":"https://dmz9.moea.gov.tw/gmweb/investigate/InvestigateFactory.aspx",
		"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
		"X-MicrosoftAjax":"Delta=true",
		"X-Requested-With":"XMLHttpRequest"
	}	

	value = {"1":"工業區", "2":"科學工業園區", "3":"加工出口區"}  # 工業區、科學園區、加工出口區
	
	data = []
	for v in value.keys():
		payload = {
			"ctl00$ContentPlaceHolder1$ScriptManager1":"ctl00$ContentPlaceHolder1$UpdatePanel2|ctl00$ContentPlaceHolder1$ddlIndustryType",
			"__EVENTTARGET":"ctl00$ContentPlaceHolder1$ddlIndustryType",
			"__EVENTARGUMENT":"",
			"__LASTFOCUS":"",
			"ContentPlaceHolder1_tvFactoryKind_ExpandState":"enccccccccccccccccccccccccccc",
			"ContentPlaceHolder1_tvFactoryKind_SelectedNode":"",
			"ContentPlaceHolder1_tvFactoryKind_PopulateLog":"",
			"ContentPlaceHolder1_tvFactoryCity_ExpandState":"nccccccccccccccccccccccnnnn",
			"ContentPlaceHolder1_tvFactoryCity_SelectedNode":"",
			"ContentPlaceHolder1_tvFactoryCity_PopulateLog":"",
			"__VIEWSTATE":"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",
			"__VIEWSTATEGENERATOR":"BDCFB64E",
			"__EVENTVALIDATION":"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",
			"ctl00$ContentPlaceHolder1$txtFactoryNo":"",
			"ctl00$ContentPlaceHolder1$txtFactoryName":"",
			"ctl00$ContentPlaceHolder1$txtProduct":"",
			"ctl00$ContentPlaceHolder1$txtMeterial":"",
			"ctl00$ContentPlaceHolder1$ddlEmployee":"",
			"ctl00$ContentPlaceHolder1$ddlYYMM_beg":"",
			"ctl00$ContentPlaceHolder1$ddlYYMM_end":"",
			"ctl00$ContentPlaceHolder1$ddlOrderBy":"",
			"ctl00$ContentPlaceHolder1$ddlOrderByType":"desc",
			"ctl00$ContentPlaceHolder1$ddlIndustryType":v,
			"ctl00$ContentPlaceHolder1$ddlIndustryList":"",
			"__ASYNCPOST":"true",
			"":"",
		}
		
		
		res = s.post(url, data = payload, verify = False, headers = headers)
		# print res.encoding
		soup = BeautifulSoup(res.text, "html.parser")
		# print res.text.encode('utf-8')
		for i in soup.select("#ContentPlaceHolder1_ddlIndustryList")[0].select("option")[1:]:
			
			zone = i.text.encode("utf-8")
			row = [v, value.get(v).decode("utf-8").encode("big5"), zone[0:2], zone[3:].decode("utf-8").encode("big5")]
			# print row
			data.append(row)
		
	f = open("../data/zone/zone_value.csv", "wb")
	w = csv.writer(f)
	w.writerows(data)
	f.close()
	print "zone_value.csv has been saved!"

	
#抓取讀取網頁的data form參數
def get_para():

	url = "https://dmz9.moea.gov.tw/gmweb/investigate/InvestigateFactory.aspx"
	
	headers = {
			"Accept":"*/*",
			"Accept-Encoding":"gzip, deflate",
			"Accept-Language":"zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4",
			"Cache-Control":"no-cache",
			"Connection":"keep-alive",
			# "Content-Length":"24966",
			"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
			"Cookie":"_ga=GA1.3.583926227.1474874583; ASP.NET_SessionId=gzqgvqgj0xhzqlzjhbzy0bw0",
			"Host":"dmz9.moea.gov.tw",
			"Origin":"https://dmz9.moea.gov.tw",
			"Pragma":"no-cache",
			"Referer":"https://dmz9.moea.gov.tw/gmweb/investigate/InvestigateFactory.aspx",
			"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
			"X-MicrosoftAjax":"Delta=true",
			"X-Requested-With":"XMLHttpRequest"
	}	
	
	s = requests.Session()
	res = s.get(url, headers = headers, verify = False)
	soup = BeautifulSoup(res.text, "html.parser")
	
	#參數抓取
	viewstate = soup.find("input", {"id": "__VIEWSTATE"}).attrs['value']
	eventvalidation = soup.find("input", {"id": "__EVENTVALIDATION"}).attrs['value']
	ContentPlaceHolder1_tvFactoryKind_ExpandState = soup.find("input", {"id": "ContentPlaceHolder1_tvFactoryKind_ExpandState"}).attrs['value']
	ContentPlaceHolder1_tvFactoryCity_ExpandState = soup.find("input", {"id": "ContentPlaceHolder1_tvFactoryCity_ExpandState"}).attrs['value']
	
	return s, viewstate, eventvalidation, ContentPlaceHolder1_tvFactoryKind_ExpandState, ContentPlaceHolder1_tvFactoryCity_ExpandState
	
	


#抓取每個工業區的檔案
url = "https://dmz9.moea.gov.tw/gmweb/investigate/InvestigateFactory.aspx"

headers = {
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Accept-Encoding":"gzip, deflate",
	"Accept-Language":"zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4",
	"Cache-Control":"max-age=0",
	"Connection":"keep-alive",
	# Content-Length:16358
	"Content-Type":"application/x-www-form-urlencoded",
	"Cookie":"_ga=GA1.3.583926227.1474874583; ASP.NET_SessionId=ns54zy05dlaxlooi0f1mqh2v",
	"Host":"dmz9.moea.gov.tw",
	"Origin":"https://dmz9.moea.gov.tw",
	"Referer":"https://dmz9.moea.gov.tw/gmweb/investigate/InvestigateFactory.aspx",
	"Upgrade-Insecure-Requests":"1",
	"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
}

count = 0
#先讀取選擇工業區後的網頁，再抓取檔案
#讀取檔案的工業區對應值(industry參數)，payload參數使用
with open("../data/zone/zone_value.csv", "r") as f:
	reader = csv.reader(f, delimiter=',')
	for row in reader:
		count = count +  1
		#重新讀取網頁產生session與data form參數
		s, viewstate, eventvalidation, ContentPlaceHolder1_tvFactoryKind_ExpandState, ContentPlaceHolder1_tvFactoryCity_ExpandState = get_para()
		#industrylist參數
		industrylist = row[2]
		payload = {
			"__EVENTTARGET":"",
			"__EVENTARGUMENT":"",
			"__LASTFOCUS":"",
			"ContentPlaceHolder1_tvFactoryKind_ExpandState":ContentPlaceHolder1_tvFactoryKind_ExpandState,
			"ContentPlaceHolder1_tvFactoryKind_SelectedNode":"",
			"ContentPlaceHolder1_tvFactoryKind_PopulateLog":"",
			"ContentPlaceHolder1_tvFactoryCity_ExpandState":ContentPlaceHolder1_tvFactoryCity_ExpandState,
			"ContentPlaceHolder1_tvFactoryCity_SelectedNode":"",
			"ContentPlaceHolder1_tvFactoryCity_PopulateLog":"",
			"__VIEWSTATE":viewstate,
			"__VIEWSTATEGENERATOR":"BDCFB64E",
			"__EVENTVALIDATION":eventvalidation,
			"ctl00$ContentPlaceHolder1$ddlOrderByType":"desc",
			"ctl00$ContentPlaceHolder1$ddlIndustryType":"",
			"ctl00$ContentPlaceHolder1$ddlIndustryList":industrylist,
			"ctl00$ContentPlaceHolder1$btnFactoryQuery":"查詢",
			"ContentPlaceHolder1_tvFactoryCityn0CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn1CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn2CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn3CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn4CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn5CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn6CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn7CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn8CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn9CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn10CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn11CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn12CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn13CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn14CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn15CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn16CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn17CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn18CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn19CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn20CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn21CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn22CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn23CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn24CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn25CheckBox":"on",
			"ContentPlaceHolder1_tvFactoryCityn26CheckBox":"on",
		}
		
		#讀取選擇工業區後的網頁
		res = s.post(url, verify = False, headers = headers, data = payload)
		#抓出參數__VIEWSTATE, __EVENTVALIDATION，for 抓取檔案頁面的data form參數使用
		soup = BeautifulSoup(res.text, "html.parser")
		viewstate = soup.select("#__VIEWSTATE")[0]['value']
		eventvalidation = soup.select("#__EVENTVALIDATION")[0]['value']

		if len(soup.select(".KindTable")) != 0:
			#抓取檔案頁面
			payload = {
				"__EVENTTARGET":"",
				"__EVENTARGUMENT":"",
				"__VIEWSTATE":viewstate,
				"__VIEWSTATEGENERATOR":"BDCFB64E",
				"__EVENTVALIDATION":eventvalidation,
				"ctl00$ContentPlaceHolder1$btnFactoryDownloadExcelList":"轉 Excel 檔(清單式)"
			}
	
			res = requests.post(url, data = payload, headers = headers, stream = True, verify = False)
			
			#存檔
			f = open("../data/factory/dep of stat ministry of economic affairs/" + row[3] + ".xls", "wb")
			copyfileobj(res.raw, f)
			f.close()
	
			print "save " + str(count) + " file, it has " + str(len(soup.select(".KindTable"))) + " factories"
		else:
			print str(count) + " dosen't exists!"

print "done!"