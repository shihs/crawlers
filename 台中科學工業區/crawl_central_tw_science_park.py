# -*- coding: utf-8 -*-
#爬取台中科學工業區廠商http://www.ctsp.gov.tw/chinese/11manufacturer/03search.aspx?v=1&fr=11&no=229
import requests
from bs4 import BeautifulSoup
import math
import csv

#先爬取廠商的編號，再爬取每個廠商的個別頁面
#爬取廠商數與post所需的參數
url = "http://www.ctsp.gov.tw/chinese/11manufacturer/03search.aspx?v=1&fr=11&no=229"
res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")

#廠商數量
amount = len(soup.select("#PageSplit1_CurrentPage")[0].select("option"))*10
#一次爬取五十個廠商所需爬取的頁數
pages = int(math.ceil(amount/50.0))
#post所需參數
viewstate = soup.select("#__VIEWSTATE")[0]["value"]
viewstategenerator = soup.select("#__VIEWSTATEGENERATOR")[0]["value"]
eventvalidation = soup.select("#__EVENTVALIDATION")[0]["value"]


# count = 0
#記錄廠商編號
numbers = []
#開始爬取
for page in range(pages):
    payload = {
        "__VIEWSTATE":viewstate, 
        "__VIEWSTATEGENERATOR":viewstategenerator, 
        "__EVENTVALIDATION":eventvalidation, 
        "keyword":"請輸入關鍵字", 
        "PageSplit1$PerPageSize":"50",
        "PageSplit1$CurrentPage":page + 1, 
        "PageSplit1$Button1":"GO!"
    }
    res = requests.post(url, data = payload)
    soup = BeautifulSoup(res.text, "html.parser")
    #抓取商商編號
    for i in soup.select(".line_1"):
        numbers.append(i.select("td")[0].text)
        # count = count + 1

count = 0


#記錄所有廠商記錄
data = []
data.append(["company", "category", "code", "boss", "tel", "address", "zone", "date", "country"])
#爬取廠商個別頁面
for number in numbers:
    #記錄每個廠商個別資訊
    row = []
    count = count + 1
    url = "http://www.ctsp.gov.tw/chinese/11manufacturer/03search_view.aspx?v=1&fr=11&no=229&sn=" + number
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    value = soup.select("#contentarea")[0].select(".w_01")[0]
    #取需要的list位置
    for j in list(value.select("span")[i] for i in [1, 3, 5, 7, 9, 11, 13, 15, 18]):
        # print j.text.encode("utf-8")
        row.append(j.text.encode("big5", "ignore"))

    data.append(row)
    print "there are " + str(count) + " done!"
    # if count == 3:
    #     break


#存檔
with open("central_tw_science_park.csv", "wb") as f:    
    w = csv.writer(f)
    w.writerows(data)



print "Done!"

