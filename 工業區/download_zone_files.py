# -*- coding: utf-8 -*-
#下載所有
import urllib
import urllib2
import csv
import requests

#加工出口區
# url = 'http://www.epza.gov.tw/ExportPark.aspx?pageid=0&t=2'
# header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"}
# res = urllib2.Request(url, headers = header)

# response = urllib2.urlopen(res)
# content = response.read()

# with open("export_processing_zone.csv", 'wb') as f:
#     f.write(content)









# #新竹科學工業區
payload = {
	"serno":"201001210018",
	"mserno":"201001210037",
	"menudata":"ChineseMenu",
	"contlink":"ap/manufacturers_1_3.jsp",
	"op":"1",
	"Qstring":"",
	"clanguage":"1",
	"type1":"1",
	"f_base":"",
	"f_kind":"1",
	"f_repprod":"0000"
}

payload = urllib.urlencode(payload)

url = "http://www.sipa.gov.tw/ap/manufacturers_1_3_excel.jsp"

req = urllib2.Request(url)
req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36")
response = urllib2.urlopen(req, data = payload)

content = response.read()

with open("hsinchu_science_park.xls", 'wb') as f:
    f.write(content)




#台北市政府產業發展局 內湖科技園區與大彎南段工業區名單
# url = "http://www.ed.gov.taipei/cgi-bin/download/cgi-bin/Company/CM_Query.csv?keyword=&type=&op=2"
# downloadurl = urllib2.urlopen(url)
# content = downloadurl.read()
# with open("neihu_dawuan.csv", 'wb') as f:
#     f.write(content)






#經濟部工業局 台灣工業用地供給與服務資訊網，所有經濟部工業區工廠資料
# url = "http://idbpark.moeaidb.gov.tw/Excel/tblFactory_20161206042154.xls"
# downloadurl = urllib2.urlopen(url)
# content = downloadurl.read()
# with open("tblFactory.csv", 'wb') as f:
#     f.write(content)
