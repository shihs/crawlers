# -*- coding: utf-8 -*-
# 中華民國世界貿易發展協會 http://www.worldtrade.org.tw/tw/
from bs4 import BeautifulSoup
from PIL import Image
import requests
import csv
import pytesseract
import shutil




def reg_number(img_url):

	headers = {
		"Referer":"http://b2c.worldtrade.org.tw/sunglory/contact/",
	}
	try:
		res = requests.get(img_url, headers = headers, stream = True, timeout = 30)
	except:
		return ""


	# 儲存電話號碼圖片
	with open('pic.jpg','wb') as f:
		f.write(res.content)
		
	# 讀取圖片
	image = Image.open('pic.jpg')
	
	# convert image to resize
	if image.mode != "RGB":
  	  image = image.convert("RGB")
  	# 調整圖片大小，以利判讀  
	image.resize((150, 50), Image.ANTIALIAS).save("pic.jpg")
	image = Image.open("pic.jpg")
	# 讀取
	tel = pytesseract.image_to_string(image).replace(" ", "").replace("-", "").replace("$", "")
	return tel



def main():

	data = []
	data.append(["category", "company", "address", "tel", "contact person"])
	
	
	url = "http://www.worldtrade.org.tw/tw/company/"
	
	res = requests.get(url)
	soup = BeautifulSoup(res.text, "lxml")
	
	# categories
	for c in soup.select(".px15")[:-1]:
		category = c.text.encode("big5", "ignore")
		category_url_ori = c["href"]
		print category
		
		page = 0

		while True:
			page = page + 1
			category_url = category_url_ori + "&page=" + str(page)
			print category_url
			category_res = requests.get(category_url)
			category_soup = BeautifulSoup(category_res.text, "lxml")
		
			if (len(category_soup.select(".list")) == 0):
				break

			try:
				# company info
				for i in category_soup.select(".list"):
					company_url = i.select("li")[0].select("a")[0]["href"] + "contact/"
					company = i.select(".px14")[0].text.encode("big5", "ignore")
					print company, company_url
			
					company_res = requests.get(company_url)
					company_soup = BeautifulSoup(company_res.text, "lxml")
			
					address = ""
					tel = ""
					contact_person = ""
					
					if (len(company_soup.select(".px13")) != 0):
						for j in company_soup.select(".px13")[0].select("tr")[1:-2]:
							if "公司地址" in j.select("td")[0].text.encode("utf-8"):
								address = j.select("td")[1].text.encode("big5", "ignore").strip()
				
							if "公司電話" in j.select("td")[0].text.encode("utf-8"):
								if len(j.select("img")) != 0:
									tel_img = j.select("img")[0]["src"]
									tel = reg_number(tel_img)
								else:
									tel = j.select("td")[1].text.encode("big5", "ignore").strip()
		
							if "聯 絡 人" in j.select("td")[0].text.encode("utf-8"):
								contact_person = j.select("td")[1].text.encode("big5", "ignore").strip()
							
					# print address, tel, contact_person
					data.append([category, company, address, tel, contact_person])
			
			except:
				with open("tw_world_trade.csv", "ab") as f:
					w = csv.writer(f)
					w.writerows(data)
					data = []
	
	
	
	
	with open("tw_world_trade.csv", "ab") as f:
		w = csv.writer(f)
		w.writerows(data)


if __name__ == '__main__':
	main()

		