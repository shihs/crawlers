# -*- coding: utf-8 -*-
#爬取南部科學工業區廠商http://www.stsp.gov.tw/web/WEB/Jsp/Page/cindex.jsp?frontTarget=DEFAULT&thisRootID=30
import requests
from bs4 import BeautifulSoup
import math
import csv




url = "http://www.stsp.gov.tw/web/WEB/Jsp/Page/company_list_c.jsp?F_KIND=0&F_NAMEC=%E8%AB%8B%E8%BC%B8%E5%85%A5%E5%BB%A0%E5%95%86%E5%90%8D%E7%A8%B1&ITEM_SCRPTC=%E8%AB%8B%E8%BC%B8%E5%85%A5%E7%94%A2%E5%93%81%E5%90%8D%E7%A8%B1&showlist=Y&BASE_ID=&hidpage=1"

res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")

# print res.text.encode(res.encoding)



#一頁10個廠商所需爬取的頁數
pages = int(math.ceil(int(soup.select("table")[0].select("table")[1].select("tr")[0].select("td")[0].text[3:6])/10.0))

# print page
data = []
data.append(["company", "company_en", "address", "tel", "zone"])
for page in range(pages):
	url = "http://www.stsp.gov.tw/web/WEB/Jsp/Page/company_list_c.jsp?F_KIND=0&F_NAMEC=%E8%AB%8B%E8%BC%B8%E5%85%A5%E5%BB%A0%E5%95%86%E5%90%8D%E7%A8%B1&ITEM_SCRPTC=%E8%AB%8B%E8%BC%B8%E5%85%A5%E7%94%A2%E5%93%81%E5%90%8D%E7%A8%B1&showlist=Y&BASE_ID=&hidpage=" + str(page+1)

	res = requests.get(url)
	soup = BeautifulSoup(res.text, "html.parser")
	for i in soup.select("table")[0].select("table")[1].select("tr")[2].select("table"):
		row = []
		for j in list(i.select("td")[ii] for ii in [0, 2, 4, 6]):
			print j.text.encode(res.encoding)
			row.append(j.text.encode("big5", "ignore"))
		row.append("南部科學工業園區".decode("utf-8").encode("big5"))
		data.append(row)



#存檔
with open("southern_tw_science_park.csv", "wb") as f:    
    w = csv.writer(f)
    w.writerows(data)
