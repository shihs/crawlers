# -*- coding: utf-8 -*-
# busytrade calwer, Taiwan companies
from bs4 import BeautifulSoup
import requests
import time
import csv


url = "http://www.busytrade.com/companies.html"
res = requests.get(url)
soup = BeautifulSoup(res.text, "lxml")

count = 0

data = []
data.append(["company", "tel"])

comps_set = set()


# all categories
for i in soup.select(".bold"):

    while True:
        try:
            category_url = "http://www.busytrade.com" + i.select(".dark_blue")[0]["href"]
            category_res = requests.get(category_url, timeout = 30)
            category_soup = BeautifulSoup(category_res.text, "lxml")
            break
        except requests.exceptions.ConnectionError as e:

            print e
            with open("busytrade.csv", "ab") as f:
                w = csv.writer(f)
                w.writerows(data)
            data = []
            time.sleep(30)
        except:
            continue

    # small categories
    for j in category_soup.select(".bold"):

        while True:
            try:
                small_category_url = "http://www.busytrade.com" + j.select(".dark_blue")[0]["href"]
                small_category_res = requests.get(small_category_url, timeout = 30)
                small_category_soup = BeautifulSoup(small_category_res.text, "lxml")
                break
            except requests.exceptions.ConnectionError as e:
                print e
                with open("busytrade.csv", "ab") as f:
                    w = csv.writer(f)
                    w.writerows(data)
                data = []
                time.sleep(30)
            except:
                continue
    
        # get companies
        for comps in small_category_soup.select(".blue"):
            count += 1
            print count

            comp = comps.text.encode("utf-8").replace("Company Name", "").strip()

            if comp in comps_set:
                continue

            print comp
            comps_set.add(comp)
            error_try = 0
            while True:
                try:
                    comp_url =  "http:"+ comps["href"] #+ "/contact_us.html"
                    print comp_url
                    comp_res = requests.get(comp_url, timeout = 30)
                    comp_soup = BeautifulSoup(comp_res.text, "lxml")

                    print comp_soup.select(".address")[0].text.encode("utf-8")
                    if "Taiwan" not in comp_soup.select(".address")[0].text.encode("utf-8"):
                        break
        
                    tel = comp_soup.select(".tel")[0].text.encode("utf-8").replace("T:", "").strip()
                    data.append([comp, tel])
#                    print data

                    break
                
                except requests.exceptions.ConnectionError as e:
                    error_try += 1
                    if error_try == 10:
                        break
                    print e
                    with open("busytrade.csv", "ab") as f:
                        w = csv.writer(f)
                        w.writerows(data)
                    data = []
                    time.sleep(30)
                
                except:
                    break
                
            time.sleep(1)
        time.sleep(3) 
    time.sleep(5)




with open("busytrade.csv", "ab") as f:
    w = csv.writer(f)
    w.writerows(data)

print "Done!"


