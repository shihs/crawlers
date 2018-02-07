# -*- coding: utf-8 -*-
# crawling suppliers on global sources http://www.taiwan.manufacturers.globalsources.com/
from bs4 import BeautifulSoup
from get_proxies import main
import requests
import csv
import time
import datetime
import random





def error_action(data, ips, proxy):
	if data != []:
		save_file(data)
		print "Data has been saved!"
	ips.pop(proxy, None)

	if len(ips.keys()) == 0:
		main()
		ips = get_proxies("ips.csv")

	proxy = random.choice(ips.keys())

	return ips, proxy



def save_file(data):
	with open("global_source.csv", "ab") as f:
		w = csv.writer(f)
		w.writerows(data)



# Getting company infomation
def get_comp_info(comp_info, comps, ips, proxy, data):

	# check if it is taiwanese company
	if "Taiwan" not in comp_info.select(".supplierInfo_extra")[0].text:
		return

	comp_info = comp_info.select(".supplierTit")[0]
	# company's name
	comp = comp_info.text.encode("utf-8")

	# check if this company has been crawled
	if comp in comps:
		return
	comps.add(comp)
	
	comp_url = comp_info["href"]
	comp_url = comp_url[:comp_url.find("Homepage")] + "ContactUs.htm"

	print comp, comp_url

	time.sleep(4)
	# company information details
	headers_agent = {
		"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
	}	

	while True:
		try:
			comp_res = s.get(comp_url, headers = headers_agent, proxies = {"http":"http://"+proxy})
			# check if connect successfully
			if comp_res.status_code != requests.codes.ok:
				print data
				ips, proxy = error_action(data, ips, proxy)
				data = []
				continue
				
			comp_soup = BeautifulSoup(comp_res.text, "lxml")
			break
		except Exception as e:
			print "Something went wrong..." + str(e)
			print data
			ips, proxy = error_action(data, ips, proxy)
			data = []
			print {"http":"http://"+proxy}
	try:
		contact_person = comp_soup.select(".contName")[0].encode(formatter="html")
		contact_person = contact_person.replace(" ", "").replace("&nbsp;", " ").replace('<pclass="contNameml10mt10">', "").replace("</p>", "").replace("\t", "").replace("\n", "")
	except:
		contact_person = "" 

	try:
		tel = comp_soup.select(".proDetCont")[0].select(".clearfix")[6].select(".ml5")[0].encode(formatter="html")
		tel = tel.replace(" ", "").replace("&nbsp;", " ").replace("\t", "").replace("\n", "").replace('<pclass="flml5">', "").replace("</p>", "").strip()
	except:
		tel = ""

	return comp, tel, contact_person



def get_proxies(file_name):
    ips = dict()
    with open(file_name, "r") as f:
        data = f.readlines()
        for ip in data:
            proxy = ip.split(",")
            ips[proxy[0]] = proxy[1]

    return ips
	


if __name__ == "__main__":

	data = []
	data.append(["company", "tel", "contact"])

	ips = get_proxies("ips.csv")
	proxy = random.choice(ips.keys())
	proxies = {"http":"http://"+proxy}
	print proxies
	
	s = requests.Session()
	
	headers_agent = {
		"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
	}
	
	# categories url
	url = "http://www.globalsources.com/gsol/I/all-suppliers/s/2000000003844/3000000149681/-1.htm"
	while True:
		try:
			res = s.get(url, headers = headers_agent, proxies = proxies, timeout = 30)
			soup = BeautifulSoup(res.text, "lxml")
			
			# response cookies
			new_visited_us = res.cookies["new_visited_us"]
			new_visited_us_create_on = res.cookies["new_visited_us_create_on"]
			JSESSIONID = res.cookies["JSESSIONID"]
			NSC_htpm = res.cookies["NSC_htpm-fyu-x-smojq"]
			break
		except Exception as e:
			print "Something went wrong...." + str(e)
			ips, proxy = error_action(data, ips, proxy)
			data = []
			proxies = {"http":"http://"+proxy}
			print proxies

	
	comps = set()
	
	# crawl every category
	for i in soup.select(".browse-ttl"):
		time.sleep(5)
		
		# suppliers url
		category_url = "http://www.globalsources.com" + i.select("a")[0]["href"].replace("-manufacturers/b/", "-suppliers/s/") + "?view=suppList"
		print category_url
	
		headers = {
			"Cookie":"JSESSIONID="+JSESSIONID+"; gs_domain=www.globalsources.com; new_visited_us="+new_visited_us+"; new_visited_us_create_on="+new_visited_us_create_on+"; NSC_htpm-fyu-x-smojq="+NSC_htpm+"; __gads=ID=1dfaa3a8cc8a2167:T=1517197415:S=ALNI_Mbxg22fZ3aZ0qGYyG0i_NFx53YY1A; LAST_VIEW=suppListTab_new; _uetsid=_uet3937bd5b; _ga=GA1.2.182102853.1517197415; _gid=GA1.2.1595678735.1517197418; _gat=1; WT_FPC=id=19fed7a9-87da-4c54-91cd-8364bef5d105:lv=1517197417693:ss=1517197417693; _bizo_bzid=39a13b32-b059-4961-9797-23e6c2a070b9; _bizo_cksm=B7C28A8C7AAEAFE1; _bizo_np_stats=155%3D1619%2C1640%3D1844%2C",
			"Referer":"http://www.globalsources.com/gsol/I/all-suppliers/s/2000000003844/3000000149681/-1.htm",
			"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
		}
	
		# category page
		while True:
			try:
				category_res = s.get(category_url, headers = headers, proxies = proxies, timeout = 30)
				category_soup = BeautifulSoup(category_res.text, "lxml")
				pages = int(category_soup.select(".nonLink")[0].text.encode("utf-8"))

				break
			except Exception as e:
				print "Something went wrong..." + str(e)
				ips, proxy = error_action(data, ips, proxy)
				data = []
				proxies = proxies = {"http":"http://"+proxy}
				print proxies
	
				# break
	
		# supplier page, first page
		for comp_info in category_soup.select(".listing_table_row"):
			info = get_comp_info(comp_info, comps, ips, proxy, data) 
			if info == None:
				continue

			comp, tel, contact_person = info			
			data.append([comp, tel, contact_person])
	
		# supplier pages, next page, exclude first page
		category_url_next = category_url
		for page in range(pages):
	
			time.sleep(2)
			headers["Referer"] = category_url_next
			category_url_next = category_url.replace("-1.htm?view=suppList", "-1/"+str((page+1)*20)+".htm?view=suppList")
			print category_url_next
			while True:
				try:
					category_res = s.get(category_url_next, headers = headers, proxies = proxies, timeout = 30)
					if category_res.status_code != requests.codes.ok:
						ips, proxy = error_action(data, ips, proxy)
						data = []
						continue

					category_soup = BeautifulSoup(category_res.text, "lxml")
					break
				except Exception as e:
					save_file(data)
					data = []
					break
	
	
			for comp_info in category_soup.select(".listing_table_row"):
	
				info = get_comp_info(comp_info, comps, ips, proxy, data) 
				if info == None:
					continue

				comp, tel, contact_person = info			
				data.append([comp, tel, contact_person])

	
	
	
	
	save_file(data)
	
	
	print "Done!"
