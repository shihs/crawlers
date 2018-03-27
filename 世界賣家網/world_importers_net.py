# -*- coding: utf-8 -*-
# World Importers Net (https://win.mofcom.gov.cn/) crawler 
from bs4 import BeautifulSoup 
from googletrans import Translator
import sys
import requests
import csv
import time
import warnings

warnings.filterwarnings('ignore')
reload(sys)
sys.setdefaultencoding( "utf-8" )





translator = Translator()

# save data
data = []
data.append(["company"])

# get companies name
def get_comp(data, soup):
	for i in soup.select(".px12_Arial"):
		# 公司名稱，簡體翻譯成繁體
		comp = translator.translate(i.text.encode("utf-8"), dest = "zh-TW").text.replace(" ", "").replace("\n", "").strip().replace("\t", "")
		begin = comp.find(".")
		end = comp.find("資".encode("utf-8"))
		comp = comp[(begin+1):end]
		data.append([comp.decode("utf-8", "ignore").encode("big5", "ignore")])
	
	return data



s = requests.Session()
url = "https://win.mofcom.gov.cn/importers/index.asp"
s.get(url, verify = False)


url = "https://win.mofcom.gov.cn/cbgnew/search2.asp"


payload = {
	"Ptype":"03",
	"keyword":" ",
	"p_area":"1",
	"p_coun":"Taiwan",
	"HavePic":"all",
	"pname":"SaledCount",
	"xname":"asc",
	"imageField3.x":"29",
	"imageField3.y":"10"
}
res = s.post(url, data = payload, verify = False)
soup = BeautifulSoup(res.text, "lxml")

# 第一頁公司
data = get_comp(data, soup)




pages = translator.translate(soup.select("font")[-3].text.encode("utf-8"), dest = "zh-TW").text
begin = pages.find("/")
end = pages.find("第".encode("utf-8"), begin)
pages = int(pages[(begin+1):(end-1)])

print "There are " + str(pages) + " pages need to crawl......"
print 

print "Page 1 is done."
print 


for page in range(1, pages):
	print "Now page " + str(page+1) + " is starting......"

	time.sleep(10)
	payload = {
		"Ptype":"07",
		"keyword":" ",
		"p_area":"1",
		"p_coun":"Taiwan",
		"HavePic":"all",
		"PageNo":str(page+1),
		"pname":"SaledCount",
		"xname":"asc",
		"speedto":str(page)
	}
	# 網址參數
	para = soup.select("form")[-1]["action"].replace("search2.asp", "")
	
	url_next = url + para
	# print url_next
	res = s.post(url_next, data = payload, verify = False)
	soup = BeautifulSoup(res.text, "lxml")
	data = get_comp(data, soup)

	print "Page " + str(page+1) + " is done."
	print 




with open("world_importers.csv", "wb") as f:
	w = csv.writer(f)
	w.writerows(data)

print "DONE!"


