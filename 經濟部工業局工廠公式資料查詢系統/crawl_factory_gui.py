# -*- coding: utf-8 -*-
#利用http://gcis.nat.gov.tw/Fidbweb/index.jsp 經濟部工業局工廠公式資料查詢系統
#爬取已知工廠登記編號工廠的gui等資料


import requests
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()
import csv
import time
import urllib
import sys

#利用工廠登記編號查詢
def id_request(fac_id):
	try:
		#利用工廠登記編號送出查詢
		url_search = "http://gcis.nat.gov.tw/Fidbweb/factInfoListAction.do?csrfPreventionSalt=IwKgnzrVKVmOJlznuwb7&method=query&regiID=" + fac_id + "&estbID=&factName=&addrCityCode1=JJ+%BD%D0%BF%EF%BE%DC&addrCityCode2=JJ&factAddr=&orgCode=JJ&statCode=JJ&cityCode1=JJ+%BD%D0%BF%EF%BE%DC&cityCode2=JJ&profItem=JJ&prodItem=&prodItemCode=&isFoodAdditionVal=&profItemValue=undefined&tmp_profitem=JJ"
		s = requests.Session()
		res = s.get(url_search, timeout = 30)
		# print res
		return res, s
	except Exception as e:
		print str(e)

#利用工廠名稱查詢
def name_request(fac_name):
	try:
		#檔案本身編碼是big5
		#取「公司」以前的字搜尋
		pos = fac_name.find("公司".decode("utf-8").encode("big5"))		
		fac_name = fac_name[:pos]
		#網站編碼是big5，所以網址要轉碼成big5
		fac_name = urllib.quote(fac_name)
		#利用工廠登記編號送出查詢
		url_search = "http://gcis.nat.gov.tw/Fidbweb/factInfoListAction.do?csrfPreventionSalt=yjH4pALpdfRtTOKhMK9e&method=query&regiID=&estbID=&factName="+fac_name+"&addrCityCode1=JJ+%BD%D0%BF%EF%BE%DC&addrCityCode2=JJ&factAddr=&orgCode=JJ&statCode=JJ&cityCode1=JJ+%BD%D0%BF%EF%BE%DC&cityCode2=JJ&profItem=JJ&prodItem=&prodItemCode=&isFoodAdditionVal=&profItemValue=undefined&tmp_profitem=JJ"
		s = requests.Session()
		res = s.get(url_search, timeout = 30)
		return res, s
	except:
		# print str(e)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		print exc_type, exc_obj, exc_tb.tb_lineno


#查詢後的網址
def factory_detail(res, s):
	row = []
					
	try:
		#找出工廠基本資料連結頁面
		soup = BeautifulSoup(res.text, "html.parser")
		if len(soup.select(".td_lightyellow")) != 0:
			pos = soup.select(".td_lightyellow")[0].select("a")[0]["href"].find("method")
			#工廠基本資料網址
			url_detail = "http://gcis.nat.gov.tw/Fidbweb/factInfoAction.do?" + soup.select(".td_lightyellow")[0].select("a")[0]["href"][pos:]
			# print url_detail
			
			#工廠基本資料requests		
			res = s.get(url_detail, timeout = 30)
			# print res
			#parse工廠基本資料
			soup = BeautifulSoup(res.text, "html.parser")
			row.append(soup.select("#AutoNumber3")[0].select("b")[0].text.encode("MS950", "replace").replace(",", "，".decode("utf-8").encode("big5")).strip())
			for i in soup.select("#AutoNumber4")[0].select("tr"):
				length = len(i.select("td"))/2
				for j in range(length):
					row.append(i.select("td")[j*2+1].text.encode("MS950", "replace").replace(",", "，".decode("utf-8").encode("big5")).strip())
		
			row.append(soup.select("#AutoNumber4")[1].select("tr")[2].select("td")[0].select("font")[0].text.encode("MS950", "replace").replace(",", "，".decode("utf-8").encode("big5")).strip().replace("\r\n", "	"))
			row.append(soup.select("#AutoNumber4")[1].select("tr")[4].select("td")[0].select("font")[0].text.encode("MS950", "replace").replace(",", "，".decode("utf-8").encode("big5")).strip().replace("\r\n", "	"))
			
			return row
		else:
			return ""

	except:
		time.sleep(60)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		print exc_type, exc_obj, exc_tb.tb_lineno
		
		



eco_affair = True   # 經濟部統計處工廠名錄
tblfactory = False # 經濟部工業局台灣工業用地供給與服務資訊網


#資料來源：https://dmz9.moea.gov.tw/gmweb/investigate/InvestigateFactory.aspx  經濟部統計處工廠名錄
if eco_affair:
	count = 0
	#最後抓取寫檔
	result = open("..\cache\eco_affair_gui.csv", "wb")
	#資料來源讀檔
	with open("..\data\\factory\eco_affair.csv", "r") as f:
		reader = csv.reader(f, delimiter = ',')
		#原始檔欄位名稱
		col_name = next(reader)
		# for i in range(7000):
		# 	next(reader)
		#將原始檔欄位名稱寫進新的檔案
		for n in col_name:
			result.write(n + "_eco" + ",")
	
		#將爬取的欄位名稱
		col_name = ["工廠名稱_idb", "工廠登記編號_idb", "工廠設立許可案號_idb", "工廠地址_idb", "工廠市鎮鄉村里_idb", \
		"工廠負責人姓名_idb", "公司（營利事業）統一編號_idb", "工廠組織型態_idb", "工廠設立核准日期_idb", "工廠登記核准日期_idb", "工廠資本額_idb", "工廠登記狀態_idb", "最後核准變更日期_idb", \
		"工廠登記歇業核准日期_idb", "工廠登記廢止核准日期_idb", "工廠登記公告廢止核准日期_idb", "最後一次校正年度_idb", "最後一次校正結果_idb", \
		"產業類別_idb", "主要產品_idb"]
		#將編碼改為big5
		for i in range(len(col_name)):
			col_name[i] = col_name[i].decode("utf-8").encode("big5")
		result.write(",".join(col_name) + "\n")
		#依據工廠登記編號爬取資料
		for row in reader:
			count = count + 1
			fac_id = row[0]  # 工廠登記編號
			for i in range(10):
				try:
					print fac_id	
					res, s = id_request(fac_id)
					data = factory_detail(res, s)
					for n in row:
						result.write(n.replace("NA", "").strip() + ",")
					result.write(",".join(data) + "\n")
					# print data
					print str(count) + " rows done!"
					break
				except:
					exc_type, exc_obj, exc_tb = sys.exc_info()
					print exc_type, exc_obj
					print "line:" + str(exc_tb.tb_lineno)
			# if count == 10:
			# 	break
			
	result.close()








#資料來源：http://idbpark.moeaidb.gov.tw/ManufQuery/Default  經濟部工業局台灣工業用地供給與服務資訊網
if tblfactory:
	count = 0
	result = open("..\cache\\tblFactory_gui.csv", "wb")
	#tbl資料來源
	with open("..\data\\factory\\tblFactory.csv", "r") as f:
		reader = csv.reader(f, delimiter = ',')
		#原始檔欄位名稱
		col_name = next(reader)
		# for i in range(5515):
		# 	next(reader)

		#將原始檔欄位名稱寫進新的檔案
		for n in col_name:
			result.write(n + "_tbl" + ",")
	
		#將爬取的欄位名稱
		col_name = ["工廠名稱_idb", "工廠登記編號_idb", "工廠設立許可案號_idb", "工廠地址_idb", "工廠市鎮鄉村里_idb", \
		"工廠負責人姓名_idb", "公司（營利事業）統一編號_idb", "工廠組織型態_idb", "工廠設立核准日期_idb", "工廠登記核准日期_idb", "工廠資本額_idb", "工廠登記狀態_idb", "最後核准變更日期_idb", \
		"工廠登記歇業核准日期_idb", "工廠登記廢止核准日期_idb", "工廠登記公告廢止核准日期_idb", "最後一次校正年度_idb", "最後一次校正結果_idb", \
		"產業類別_idb", "主要產品_idb"]
		# print col_name
		#將爬取的欄位名稱轉碼並寫進檔案
		for i in range(len(col_name)):
			col_name[i] = col_name[i].decode("utf-8").encode("big5")
		result.write(",".join(col_name) + "\n")
		#依序讀取每一行資料
		for row in reader:
			count = count + 1
			#工廠登記編號
			fac_id = row[12]
			#寫進原始檔原有資料
			for n in row:
				#取代NA、「,」、「？」以及「?」
				result.write(n.replace("NA", "")  \
							  .replace(",", "，".decode("utf-8").encode("big5"))  \
							  .replace("？".decode("utf-8").encode("big5"), "")  \
							  .replace("?".decode("utf-8").encode("big5"), "")  \
							  .strip() + ",")
			#如果發生錯誤重新連線十次
			for i in range(10):
				try:				
					#如果工廠登記編號不為空白且為數字才抓取網址
					if fac_id != "" and fac_id.isdigit():
						res, s = id_request(fac_id)  # 利用工廠登記編號搜尋
						data = factory_detail(res, s)  # 爬取工廠資料
						#如果爬取結果有資料，則寫檔
						if data != "":	
							print fac_id			
							result.write(",".join(data) + "\n")
						#如果爬取結果無資料，利用工廠名稱重新搜尋
						else:
							fac_name = row[13]  # 工廠名稱
							print fac_name.decode("big5", "replace").encode("utf-8", "replace"), fac_id
							res, s = name_request(fac_name)  # 利用工廠名稱搜尋
							data = factory_detail(res, s)  # 爬取工廠資料
							#如果爬取結果有資料，則寫檔
							if data != "":
								result.write(",".join(data) + "\n")				
							#如果爬取結果無資料，則寫進空白
							else:
								for i in range(18):
									result.write("" + ",")
								result.write("" + "\n")
					#如果沒有工廠登記編碼，利用名稱搜尋
					else:
						fac_name = row[13]  # 工廠名稱
						print fac_name.decode("big5", "replace").encode("utf-8", "replace")
						res, s = name_request(fac_name)  # 利用工廠名稱搜尋 
						data = factory_detail(res, s)  # 爬取工廠資料
						#如果爬取結果有資料，則寫檔
						if data != "":
							result.write(",".join(data) + "\n")
						#如果爬取結果無資料，則寫進空白
						else:
							for i in range(18):
								result.write("" + ",")
							result.write("" + "\n")
		
					print str(count) + " rows done!"
					break

				except Exception as e:
					print str(e)
					exc_type, exc_obj, exc_tb = sys.exc_info()
					print exc_type, exc_obj
					print "line:" + str(exc_tb.tb_lineno)
		
	result.close()



