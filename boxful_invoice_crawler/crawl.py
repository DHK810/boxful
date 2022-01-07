import time
from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
from html_table_parser import parser_functions as parser
import requests
import csv

headers = ['invoice_id','location','name','email','Amount','outstandingamount','status','txID','created']
start_date = ["2021-10", "2021-11", "2021-12", "2022-01"]
start_page = 1
end_page = 70
count = 1
with open("invoicesasdf.csv","w",newline='') as f:
    writer = csv.DictWriter(f, fieldnames=headers)

    driver = webdriver.Chrome(executable_path="C:/Users/boxful/Desktop/crawl/chromedriver.exe")

    driver.get('https://www.boxful.kr/ko/log-in')
    time.sleep(2) # Let the user actually see something!

    driver.find_element_by_name('username').send_keys('***')
    driver.find_element_by_name('password').send_keys('***')
    driver.find_element_by_xpath('//*[@id="box1"]/div/div[4]/form/fieldset/div[3]/button').click()
    time.sleep(2) # Let the user actually see something!

    driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/ul/li[5]/a').click()
    time.sleep(2) # Let the user actually see something!

    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/input').click()
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[5]/div[1]/div[1]/ul/li[2]').click()
    time.sleep(3) # Let the user actually see something!

    for i in range(start_page,end_page): #수기로 가져올 것

        if count <= 5:
            driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div/ul/li['+str(count)+']').click()
            time.sleep(2)
            depth_1_tbody = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[3]/table/tbody')
            depth_2_tr = depth_1_tbody.find_elements_by_tag_name('tr')
            for td in depth_2_tr:
                row = td.text
                row_list = row.split("\n")
                print(len(row_list))

                print(row_list[len(row_list)-1][:7])
                if row_list[len(row_list)-1][:7] in start_date:
                    if len(row_list) == 7:  # 지점 정보, txID 없는 경우, 프랜차이즈가 아닌 지점이면서 아직 결제하지 않은 경우
                        goods_info = {
                            'invoice_id' : row_list[0],
                            'location' : '지점',
                            'name' : row_list[1],
                            'email' : row_list[2],
                            'Amount' : row_list[3],
                            'outstandingamount' : row_list[4],
                            'status' : row_list[5],
                            'txID' : 0,
                            'created' : row_list[6]
                        }
                    if len(row_list) == 8: #지점 정보는 있으나 tx_id가 없는경우 - 프랜차이즈인 지점 고객이 아직 결제 하지 않은 경우
                        if row_list[1][-1] =='점':
                            goods_info = {
                                'invoice_id' : row_list[0],
                                'location' : row_list[1],
                                'name' : row_list[2],
                                'email' : row_list[3],
                                'Amount' : row_list[4],
                                'outstandingamount' : row_list[5],
                                'status' : row_list[6],
                                'txID' : 0,
                                'created' : row_list[7]
                            }
                        else:
                            goods_info = {
                                'invoice_id' : row_list[0],
                                'location' : '지점',
                                'name' : row_list[1],
                                'email' : row_list[2],
                                'Amount' : row_list[3],
                                'outstandingamount' : row_list[4],
                                'status' : row_list[5],
                                'txID' : row_list[6],
                                'created' : row_list[7]
                            }
                    if len(row_list) == 9: #모든 정보 있음, 프랜차이즈이면서 결제한 경우
                        goods_info = {
                            'invoice_id' : row_list[0],
                            'location' : row_list[1],
                            'name' : row_list[2],
                            'email' : row_list[3],
                            'Amount' : row_list[4],
                            'outstandingamount' : row_list[5],
                            'status' : row_list[6],
                            'txID' : row_list[7],
                            'created' : row_list[8]
                        }
                    print(goods_info)
                    writer.writerow(goods_info)
                else:
                    continue
            count += 1
        else:
            driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[3]/div/ul/li[6]').click()
            time.sleep(2)
            depth_1_tbody = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[2]/div[3]/table/tbody')
            depth_2_tr = depth_1_tbody.find_elements_by_tag_name('tr')
            for td in depth_2_tr:
                row = td.text
                row_list = row.split("\n")
                print(row_list[len(row_list)-1][:7])
                if row_list[len(row_list)-1][:7] in start_date:
                    if len(row_list) == 7:  # 지점 정보, txID 없는 경우, 프랜차이즈가 아닌 지점이면서 아직 결제하지 않은 경우
                        goods_info = {
                            'invoice_id' : row_list[0],
                            'location' : '지점',
                            'name' : row_list[1],
                            'email' : row_list[2],
                            'Amount' : row_list[3],
                            'outstandingamount' : row_list[4],
                            'status' : row_list[5],
                            'txID' : 0,
                            'created' : row_list[6]
                        }
                    if len(row_list) == 8: #지점 정보는 있으나 tx_id가 없는경우 - 프랜차이즈인 지점 고객이 아직 결제 하지 않은 경우
                        if row_list[1][-1] =='점':
                            goods_info = {
                                'invoice_id' : row_list[0],
                                'location' : row_list[1],
                                'name' : row_list[2],
                                'email' : row_list[3],
                                'Amount' : row_list[4],
                                'outstandingamount' : row_list[5],
                                'status' : row_list[6],
                                'txID' : 0,
                                'created' : row_list[7]
                            }
                        else:
                            goods_info = {
                                'invoice_id' : row_list[0],
                                'location' : '지점',
                                'name' : row_list[1],
                                'email' : row_list[2],
                                'Amount' : row_list[3],
                                'outstandingamount' : row_list[4],
                                'status' : row_list[5],
                                'txID' : row_list[6],
                                'created' : row_list[7]
                            }
                    if len(row_list) == 9: #모든 정보 있음, 프랜차이즈이면서 결제한 경우
                        goods_info = {
                            'invoice_id' : row_list[0],
                            'location' : row_list[1],
                            'name' : row_list[2],
                            'email' : row_list[3],
                            'Amount' : row_list[4],
                            'outstandingamount' : row_list[5],
                            'status' : row_list[6],
                            'txID' : row_list[7],
                            'created' : row_list[8]
                        }
                    print(goods_info)
                    writer.writerow(goods_info)
                else:
                    continue
            count += 1
    f.close()
# headers = ['invoice_id','location','name','email','Amount','outstandingamount','status','txID','created']
