from bs4 import BeautifulSoup
import requests
from _datetime import date,datetime
import time
import pymysql
import re

config = {
    'host':'127.0.0.1',
    'port':3306,
    'user':'root',
    'password':'19860112',
    'db':'house',
    'charset':'gb2312'
}

present_date = datetime.now().date()

def delete_today_data(config):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            # 执行sql语句，插入记录
            sql = "DELETE FROM house WHERE date = '%s'" %(present_date)
            cursor.execute(sql)
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        connection.commit()
    finally:
        connection.close()
    print('-----------------------delete success!----------------','\n')

def get_fangdd_url(url_number):
    url_fangdd = url_number
    urls = []
    for i in range(1,url_fangdd+1):
        urls.append(i)
    urls[0] = 'http://esf.fangdd.com/shanghai?query=%E5%8F%A4%E6%A1%90%E5%85%AC%E5%AF%93&city_id=121'
    urls[1] = 'http://esf.fangdd.com/shanghai?query=%E4%B8%89%E6%B3%BE%E5%8D%97%E5%AE%85&city_id=121'
    urls[2] = 'http://esf.fangdd.com/shanghai?query=%E4%B8%AD%E9%98%B3%E5%B0%8F%E5%8C%BA&city_id=121'
    urls[3] = 'http://esf.fangdd.com/shanghai?query=%E6%9C%97%E8%AF%97%E7%BB%BF%E8%89%B2%E8%A1%97%E5%8C%BA&city_id=121'
    urls[4] = 'http://esf.fangdd.com/shanghai?query=%E9%95%BF%E5%AE%81%E8%B7%AF1600%E5%BC%84&city_id=121'
    urls[5] = 'http://esf.fangdd.com/shanghai?query=%E6%98%A5%E5%A4%A9%E8%8A%B1%E5%9B%AD&city_id=121'
    urls[6] = 'http://esf.fangdd.com/shanghai?query=%E4%B8%89%E6%B3%BE%E5%8C%97%E5%AE%85&city_id=121'
    urls[7] = 'http://esf.fangdd.com/shanghai?query=%E9%87%91%E6%9D%A8%E4%BA%8C%E8%A1%97%E5%9D%8A&city_id=121'
    urls[8] = 'http://esf.fangdd.com/shanghai?query=%E9%87%91%E6%9D%A8%E4%BA%94%E8%A1%97%E5%9D%8A&city_id=121'
    urls[9] = 'http://esf.fangdd.com/shanghai?query=%E7%94%B1%E7%94%B1%E4%B8%83%E6%9D%91&city_id=121'
    urls[10] = 'http://esf.fangdd.com/shanghai?query=%E7%94%B1%E7%94%B1%E4%BA%8C%E6%9D%91&city_id=121'
    urls[11] = 'http://esf.fangdd.com/shanghai?query=%E7%BB%BF%E6%B3%A2%E5%9F%8E&city_id=121'
    urls[12] = 'http://esf.fangdd.com/shanghai?query=%E6%AF%95%E5%8A%A0%E7%B4%A2%E5%B0%8F%E9%95%87&city_id=121'
    urls[13] = 'http://esf.fangdd.com/shanghai?query=%E9%87%91%E5%88%A9%E5%85%AC%E5%AF%93&city_id=121'
    urls[14] = 'http://esf.fangdd.com/shanghai?query=%E5%85%86%E4%B8%B0%E8%8A%B1%E5%9B%AD&city_id=121'
    urls[15] = 'http://esf.fangdd.com/shanghai?query=%E4%B8%8A%E6%B5%B7%E5%BA%B7%E5%9F%8E&city_id=121'
    urls[16] = 'http://esf.fangdd.com/shanghai?query=%E9%BD%90%E7%88%B1%E4%BD%B3%E8%8B%91&city_id=121'    #齐爱佳苑
    urls[17] = 'http://esf.fangdd.com/shanghai?query=%E4%B8%8A%E6%B5%B7%E8%8A%B1%E5%9F%8E&city_id=121'    #上海花城
    urls[18] = 'http://esf.fangdd.com/shanghai?query=%E5%87%AF%E6%AC%A3%E8%B1%AA%E5%9B%AD&city_id=121'    #凯欣豪园
    urls[19] = 'http://esf.fangdd.com/shanghai?query=%E5%A4%A9%E5%B1%B1%E4%B8%AD%E5%8D%8E%E5%9B%AD&city_id=121'   #天山中华园
    urls[20] = 'http://esf.fangdd.com/shanghai?query=%E4%B8%8A%E6%B5%B7%E9%98%B3%E5%9F%8E&city_id=121'    #上海阳城
    urls[21] = 'http://esf.fangdd.com/shanghai?query=%E6%B0%B4%E8%AF%AD%E4%BA%BA%E5%AE%B6&city_id=121'    #水语人家
    urls[22] = 'http://esf.fangdd.com/shanghai?query=%E5%8D%8E%E6%B6%A6%E4%B8%AD%E5%A4%AE%E5%85%AC%E5%9B%AD&city_id=121'   #华润中央公园
    urls[23] = 'http://esf.fangdd.com/shanghai?query=%E7%A7%91%E5%AE%81%E5%85%AC%E5%AF%93&city_id=121'    #科宁公寓
    urls[24] = 'http://esf.fangdd.com/shanghai?query=%E5%BB%B6%E8%A5%BF%E5%B0%8F%E5%8C%BA&city_id=121'    #延西小区
    urls[25] = 'http://esf.fangdd.com/shanghai?query=%E4%BF%9D%E5%88%A9%E5%8F%B6%E8%AF%AD&city_id=121'    #保利叶语
    urls[26] = 'http://esf.fangdd.com/shanghai?query=%E9%87%91%E5%9C%B0%E8%89%BA%E5%A2%83&city_id=121'    #金地艺境
    urls[27] = 'http://esf.fangdd.com/shanghai?query=%E6%98%A5%E6%B8%AF%E4%B8%BD%E5%9B%AD&city_id=121'    #春港丽园
    urls[28] = 'http://esf.fangdd.com/shanghai?query=%E5%8F%A4%E6%A1%90%E4%BA%94%E6%9D%91&city_id=121'    #古桐五村
    urls[29] = 'http://esf.fangdd.com/shanghai?query=%E5%8F%A4%E6%A1%90%E4%BA%8C%E6%9D%91&city_id=121'    #古桐二村
    urls[30] = 'http://esf.fangdd.com/shanghai?query=%E5%8F%A4%E6%A1%90%E4%B8%89%E6%9D%91&city_id=121'    #古桐三村
    urls[31] = 'http://esf.fangdd.com/shanghai?query=%E5%8F%A4%E6%A1%90%E5%9B%9B%E6%9D%91&city_id=121'    #古桐四村
    urls[32] = 'http://esf.fangdd.com/shanghai?query=%E5%8F%A4%E6%A1%90%E5%85%AD%E6%9D%91&city_id=121'    #古桐六村
    urls[33] = 'http://esf.fangdd.com/shanghai?query=%E5%BB%BA%E4%B8%AD%E8%B7%AF461%E5%BC%84&city_id=121'   #建中路461弄
    urls[34] = 'http://esf.fangdd.com/shanghai?query=%E5%BB%BA%E4%B8%AD%E8%B7%AF171%E5%BC%84&city_id=121'   #建中路171弄
    urls[35] = 'http://esf.fangdd.com/shanghai?query=%E6%B1%A4%E8%87%A3%E8%B1%AA%E5%9B%AD&city_id=121'      #汤臣豪园
    return urls

def get_fangdd_house(urls,source):
    for url in urls:
        print('original url-------------------------',url,'\n')
        #proxy = '33.33.33.11:8118'
        web_data = requests.get(url)
        soup = BeautifulSoup(web_data.text,'lxml')
        house_page = soup.select('body > div.contain.w1200 > div.main.clearfix > div.house-info.pull-left > div.page-pagination > ul > li > a')
        #print(house_page)
        for page in house_page:
            if page.get_text().isdigit():
                pages = page.get_text()
            else:
                break
        if house_page==[]:
            pages=1
        url_base = 'http://esf.fangdd.com/shanghai'
        for page in range(1,int(pages)+1):
            more_page1 = '/list/q'
            more_page2 = '_pa'+str(page)
            urls = re.split(url_base,url)
            urls = re.split('=',urls[1])
            #print(url,'\n---------------------\n')
            urls = re.split('&',urls[1])
            #print(urls,'\n---------------------\n')
            url_new = url_base + more_page1 + urls[0] + more_page2
            print('real----------------',url,'\n')
            web_data = requests.get(url_new)
            soup = BeautifulSoup(web_data.text,'lxml')
            house_name = soup.select('body > div.contain.w1200 > div.main.clearfix > div.house-info.pull-left > div > div.bg_color.clearfix > div.content.pull-left > div.name-title.clearfix > a > span.name')
            house_price = soup.select('body > div.contain.w1200 > div.main.clearfix > div.house-info.pull-left > div > div.bg_color.clearfix > div.price-panel.pull-right > h4 > span')
            house_area = soup.select('body > div.contain.w1200 > div.main.clearfix > div.house-info.pull-left > div > div.bg_color.clearfix > div.content.pull-left > div.name-title.clearfix > a > span.area')
            for name,price,area in zip(house_name,house_price,house_area):
                #print(name,price,area)
                connection = pymysql.connect(**config)
                price = price.get_text()
                area = re.findall(r'(\w*[0-9]+\.*[0-9]+)\w*',area.get_text())
                price_per_area = float(price)/float(area[0])
                print('real mysql info',price,'-----',area,'-----',price_per_area,'-----------\n')
                try:
                    with connection.cursor() as cursor:
                # 执行sql语句，插入记录
                         sql = 'INSERT INTO house (date, house_name, house_price, house_area, source, price_per_area) VALUES (%s, %s, %s, %s, %s, %s)'
                         cursor.execute(sql, (present_date, name.get_text(), price, area, source, price_per_area))
                # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
                    connection.commit()
                finally:
                    connection.close()
    time.sleep(1)

def get_lianjia_url(url_number):
    url_lianjia = url_number
    urls = []
    for i in range(1,url_lianjia+1):
        urls.append(i)
    urls[0] = 'http://sh.lianjia.com/ershoufang/rs%E4%B8%89%E6%B3%BE%E5%8D%97%E5%AE%85'
    urls[1] = 'http://sh.lianjia.com/ershoufang/rs%E4%B8%8A%E6%B5%B7%E5%BA%B7%E5%9F%8E'
    urls[2] = 'http://sh.lianjia.com/ershoufang/rs%E4%B8%89%E6%B3%BE%E5%8C%97%E5%AE%85'
    urls[3] = 'http://sh.lianjia.com/ershoufang/rs%E5%8F%A4%E6%A1%90%E5%85%AC%E5%AF%93'
    urls[4] = 'http://sh.lianjia.com/ershoufang/rs%E4%B8%AD%E9%98%B3%E5%B0%8F%E5%8C%BA'
    urls[5] = 'http://sh.lianjia.com/ershoufang/rs%E6%9C%97%E8%AF%97%E7%BB%BF%E8%89%B2%E8%A1%97%E5%8C%BA'
    urls[6] = 'http://sh.lianjia.com/ershoufang/rs%E9%95%BF%E5%AE%81%E8%B7%AF1600%E5%BC%84'
    urls[7] = 'http://sh.lianjia.com/ershoufang/rs%E6%98%A5%E5%A4%A9%E8%8A%B1%E5%9B%AD'
    urls[8] = 'http://sh.lianjia.com/ershoufang/rs%E9%87%91%E6%9D%A8%E4%BA%8C%E8%A1%97%E5%9D%8A'
    urls[9] = 'http://sh.lianjia.com/ershoufang/rs%E9%87%91%E6%9D%A8%E4%BA%94%E8%A1%97%E5%9D%8A'
    urls[10] = 'http://sh.lianjia.com/ershoufang/rs%E7%94%B1%E7%94%B1%E4%B8%83%E6%9D%91'
    urls[11] = 'http://sh.lianjia.com/ershoufang/rs%E7%94%B1%E7%94%B1%E4%BA%8C%E6%9D%91'
    urls[12] = 'http://sh.lianjia.com/ershoufang/rs%E7%BB%BF%E6%B3%A2%E5%9F%8E'
    urls[13] = 'http://sh.lianjia.com/ershoufang/rs%E6%AF%95%E5%8A%A0%E7%B4%A2%E5%B0%8F%E9%95%87'
    urls[14] = 'http://sh.lianjia.com/ershoufang/rs%E9%87%91%E5%88%A9%E5%85%AC%E5%AF%93'
    urls[15] = 'http://sh.lianjia.com/ershoufang/rs%E5%85%86%E4%B8%B0%E8%8A%B1%E5%9B%AD'
    urls[16] = 'http://sh.lianjia.com/ershoufang/rs%E9%BD%90%E7%88%B1%E4%BD%B3%E8%8B%91'    #齐爱佳苑
    urls[17] = 'http://sh.lianjia.com/ershoufang/rs%E4%B8%8A%E6%B5%B7%E8%8A%B1%E5%9F%8E'    #上海花城
    urls[18] = 'http://sh.lianjia.com/ershoufang/rs%E5%87%AF%E6%AC%A3%E8%B1%AA%E5%9B%AD'    #凯欣豪园
    urls[19] = 'http://sh.lianjia.com/ershoufang/rs%E5%A4%A9%E5%B1%B1%E4%B8%AD%E5%8D%8E%E5%9B%AD'   #天山中华园
    urls[20] = 'http://sh.lianjia.com/ershoufang/rs%E4%B8%8A%E6%B5%B7%E9%98%B3%E5%9F%8E'    #上海阳城
    urls[21] = 'http://sh.lianjia.com/ershoufang/rs%E6%B0%B4%E8%AF%AD%E4%BA%BA%E5%AE%B6'    #水语人家
    urls[22] = 'http://sh.lianjia.com/ershoufang/rs%E5%8D%8E%E6%B6%A6%E4%B8%AD%E5%A4%AE%E5%85%AC%E5%9B%AD'    #华润中央公园
    urls[23] = 'http://sh.lianjia.com/ershoufang/rs%E7%A7%91%E5%AE%81%E5%85%AC%E5%AF%93'    #科宁公寓
    urls[24] = 'http://sh.lianjia.com/ershoufang/rs%E5%BB%B6%E8%A5%BF%E5%B0%8F%E5%8C%BA'    #延西小区
    urls[25] = 'http://sh.lianjia.com/ershoufang/rs%E4%BF%9D%E5%88%A9%E5%8F%B6%E8%AF%AD'    #保利叶语
    urls[26] = 'http://sh.lianjia.com/ershoufang/rs%E9%87%91%E5%9C%B0%E8%89%BA%E5%A2%83'    #金地艺境
    urls[27] = 'http://sh.lianjia.com/ershoufang/rs%E6%98%A5%E6%B8%AF%E4%B8%BD%E5%9B%AD'    #春港丽园
    urls[28] = 'http://sh.lianjia.com/ershoufang/rs%E5%8F%A4%E6%A1%90%E4%BA%94%E6%9D%91'    #古桐五村
    urls[29] = 'http://sh.lianjia.com/ershoufang/rs%E5%8F%A4%E6%A1%90%E4%BA%8C%E6%9D%91'    #古桐二村
    urls[30] = 'http://sh.lianjia.com/ershoufang/rs%E5%8F%A4%E6%A1%90%E4%B8%89%E6%9D%91'    #古桐三村
    urls[31] = 'http://sh.lianjia.com/ershoufang/rs%E5%8F%A4%E6%A1%90%E5%9B%9B%E6%9D%91'    #古桐四村
    urls[32] = 'http://sh.lianjia.com/ershoufang/rs%E5%8F%A4%E6%A1%90%E5%85%AD%E6%9D%91'    #古桐六村
    urls[33] = 'http://sh.lianjia.com/ershoufang/rs%E5%BB%BA%E4%B8%AD%E8%B7%AF461%E5%BC%84'    #建中路461弄
    urls[34] = 'http://sh.lianjia.com/ershoufang/rs%E5%BB%BA%E4%B8%AD%E8%B7%AF171%E5%BC%84'    #建中路171弄
    urls[35] = 'http://sh.lianjia.com/ershoufang/rs%E6%B1%A4%E8%87%A3%E8%B1%AA%E5%9B%AD'    #汤臣豪园
    return urls

def get_lianjia_house(urls,source):
    for url in urls:
        print(url)
        web_data = requests.get(url)
        soup = BeautifulSoup(web_data.text,'lxml')
        house_page = soup.select('body > div.wrapper > div.main-box.clear > div > div.page-box.house-lst-page-box > a')
        for page in house_page:
            if page.get_text().isdigit():
                pages = page.get_text()
            else:
                break
        url_base = 'http://sh.lianjia.com/ershoufang/'
        for page in range(1,int(pages)+1):
            more_page = 'd'+str(page)
            urls = re.split(url_base,url)
            url = url_base + more_page + urls[1]
            web_data = requests.get(url)
            soup = BeautifulSoup(web_data.text,'lxml')
            house_name = soup.select('div.where > a > span')
            house_price = soup.select('div.price > span')
            house_area = soup.select('div.where > span:nth-of-type(2)')
            for name,price,area in zip (house_name,house_price,house_area):
                print(name,price,area)
                connection = pymysql.connect(**config)
                price = price.get_text()
                area = re.findall(r'(\w*[0-9]+\.*[0-9]+)\w*',area.get_text())
                price_per_area = float(price)/float(area[0])
                print(price,'-----',area,'-----',price_per_area,'-----------\n')
                try:
                     with connection.cursor() as cursor:
                     # 执行sql语句，插入记录
                         sql = 'INSERT INTO house (date, house_name, house_price, house_area, source, price_per_area) VALUES (%s, %s, %s, %s, %s, %s)'
                         cursor.execute(sql, (present_date, name.get_text(), price, area, source, price_per_area))
                     # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
                     connection.commit()
                finally:
                     connection.close()
        time.sleep(1)

def get_iwjw_url(url_number):
    url_fangdd = url_number
    urls = []
    for i in range(1,url_fangdd+1):
        urls.append(i)
    urls[0] = 'http://www.iwjw.com/sale/shanghai/g3id8664/?kw=%E5%8F%A4%E6%A1%90%E5%85%AC%E5%AF%93'
    urls[1] = 'http://www.iwjw.com/sale/shanghai/?kw=%E4%B8%8A%E6%B5%B7%E5%BA%B7%E5%9F%8E'
    urls[2] = 'http://www.iwjw.com/sale/shanghai/?kw=%E4%B8%89%E6%B3%BE%E5%8D%97%E5%AE%85'
    urls[3] = 'http://www.iwjw.com/sale/shanghai/?kw=%E4%B8%89%E6%B3%BE%E5%8C%97%E5%AE%85'
    urls[4] = 'http://www.iwjw.com/sale/shanghai/g3id3221/?kw=%E4%B8%AD%E9%98%B3%E5%B0%8F%E5%8C%BA'
    urls[5] = 'http://www.iwjw.com/sale/shanghai/?kw=%E6%9C%97%E8%AF%97%E7%BB%BF%E8%89%B2%E8%A1%97%E5%8C%BA'
    urls[6] = 'http://www.iwjw.com/sale/shanghai/?kw=%E9%95%BF%E5%AE%81%E8%B7%AF1600%E5%BC%84'
    urls[7] = 'http://www.iwjw.com/sale/shanghai/g3id2616/?kw=%E6%98%A5%E5%A4%A9%E8%8A%B1%E5%9B%AD'
    urls[8] = 'http://www.iwjw.com/sale/shanghai/g3id7432/?kw=%E9%87%91%E6%9D%A8%E4%BA%8C%E8%A1%97%E5%9D%8A'
    urls[9] = 'http://www.iwjw.com/sale/shanghai/g3id7423/?kw=%E9%87%91%E6%9D%A8%E4%BA%94%E8%A1%97%E5%9D%8A'
    urls[10] = 'http://www.iwjw.com/sale/shanghai/g3id7200/?kw=%E7%94%B1%E7%94%B1%E4%B8%83%E6%9D%91'
    urls[11] = 'http://www.iwjw.com/sale/shanghai/?kw=%E7%BB%BF%E6%B3%A2%E5%9F%8E'
    urls[12] = 'http://www.iwjw.com/sale/shanghai/?kw=%E6%AF%95%E5%8A%A0%E7%B4%A2%E5%B0%8F%E9%95%87'
    urls[13] = 'http://www.iwjw.com/sale/shanghai/g3id8336/?kw=%E9%87%91%E5%88%A9%E5%85%AC%E5%AF%93'
    urls[14] = 'http://www.iwjw.com/sale/shanghai/g3id3230/?kw=%E5%85%86%E4%B8%B0%E8%8A%B1%E5%9B%AD'
    urls[15] = 'http://www.iwjw.com/sale/shanghai/?kw=%E7%94%B1%E7%94%B1%E4%BA%8C%E6%9D%91'
    urls[16] = 'http://www.iwjw.com/sale/shanghai/g3id8342/?kw=%E9%BD%90%E7%88%B1%E4%BD%B3%E8%8B%91'
    urls[17] = 'http://www.iwjw.com/sale/shanghai/g3id2649/?kw=%E4%B8%8A%E6%B5%B7%E8%8A%B1%E5%9F%8E'
    urls[18] = 'http://www.iwjw.com/sale/shanghai/g3id3104/?kw=%E5%87%AF%E6%AC%A3%E8%B1%AA%E5%9B%AD'     #凯欣豪园
    urls[19] = 'http://www.iwjw.com/sale/shanghai/g3id2657/?kw=%E5%A4%A9%E5%B1%B1%E4%B8%AD%E5%8D%8E%E5%9B%AD'   #天山中华园
    urls[20] = 'http://www.iwjw.com/sale/shanghai/g3id10120/?kw=%E4%B8%8A%E6%B5%B7%E9%98%B3%E5%9F%8E'     #上海阳城
    urls[21] = 'http://www.iwjw.com/sale/shanghai/g3id10247/?kw=%E6%B0%B4%E8%AF%AD%E4%BA%BA%E5%AE%B6'    #水语人家
    urls[22] = 'http://www.iwjw.com/sale/shanghai/g3id11071/?kw=%E5%8D%8E%E6%B6%A6%E4%B8%AD%E5%A4%AE%E5%85%AC%E5%9B%AD'   #华润中央公园
    urls[23] = 'http://www.iwjw.com/sale/shanghai/g3id50729/?kw=%E7%A7%91%E5%AE%81%E5%85%AC%E5%AF%93'    #科宁公寓
    urls[24] = 'http://www.iwjw.com/sale/shanghai/g3id2859/?kw=%E5%BB%B6%E8%A5%BF%E5%B0%8F%E5%8C%BA'     #延西小区
    urls[25] = 'http://www.iwjw.com/sale/shanghai/g3id9036/?kw=%E4%BF%9D%E5%88%A9%E5%8F%B6%E8%AF%AD'     #保利叶语
    urls[26] = 'http://www.iwjw.com/sale/shanghai/g3id9164/?kw=%E9%87%91%E5%9C%B0%E8%89%BA%E5%A2%83'     #金地艺境
    urls[27] = 'http://www.iwjw.com/sale/shanghai/?kw=%E6%98%A5%E6%B8%AF%E4%B8%BD%E5%9B%AD'     #春港丽园
    urls[28] = 'http://www.iwjw.com/sale/shanghai/?kw=%E5%8F%A4%E6%A1%90%E4%BA%94%E6%9D%91'    #古桐五村
    urls[29] = 'http://www.iwjw.com/sale/shanghai/g3id8666/?kw=%E5%8F%A4%E6%A1%90%E4%BA%8C%E6%9D%91'     #古桐二村
    urls[30] = 'http://www.iwjw.com/sale/shanghai/g3id8665/?kw=%E5%8F%A4%E6%A1%90%E4%B8%89%E6%9D%91'     #古桐三村
    urls[31] = 'http://www.iwjw.com/sale/shanghai/g3id8667/?kw=%E5%8F%A4%E6%A1%90%E5%9B%9B%E6%9D%91'     #古桐四村
    urls[32] = 'http://www.iwjw.com/sale/shanghai/g3id8669/?kw=%E5%8F%A4%E6%A1%90%E5%85%AD%E6%9D%91'     #古桐六村
    urls[33] = 'http://www.iwjw.com/sale/shanghai/?kw=%E5%BB%BA%E4%B8%AD%E8%B7%AF461%E5%BC%84'     #建中路461弄
    urls[34] = 'http://www.iwjw.com/sale/shanghai/?kw=%E5%BB%BA%E4%B8%AD%E8%B7%AF171%E5%BC%84'     #建中路171弄
    urls[35] = 'http://www.iwjw.com/sale/shanghai/?kw=%E6%B1%A4%E8%87%A3%E8%B1%AA%E5%9B%AD'    #汤臣豪园
    return urls

def get_iwjw_house(urls,source):
    for url in urls:
        print(url)
        web_data = requests.get(url)
        soup = BeautifulSoup(web_data.text,'lxml')
        house_page = soup.select('div.mod-lists.mb50.clearfix > div.List.mod-border-box.mod-list-shadow > div > p > a')
        print(house_page)
        for page in house_page:
            if page.get_text().isdigit():
                pages = page.get_text()
            else:
                break
        if house_page==[]:
            pages=1
        url_base = 'http://www.iwjw.com/sale/shanghai/'
        for page in range(1,int(pages)+1):
            more_page = 'p'+str(page)+'/'
            urls = re.split(url_base,url)
            url = url_base + more_page + urls[1]
            web_data = requests.get(url)
            soup = BeautifulSoup(web_data.text,'lxml')
            house_name = soup.select('div.mod-lists.mb50.clearfix > div:nth-of-type(1) > ol > li > div > h4 > b > a > i')
            house_price = soup.select('div.mod-lists.mb50.clearfix > div:nth-of-type(1) > ol > li > div > h5 > i.Hp > b')
            house_area = soup.select('div.mod-lists.mb50.clearfix > div:nth-of-type(1) > ol > li > div > h5 > i.i2')
            for name,price,area in zip (house_name,house_price,house_area):
                print(name,price,area)
                connection = pymysql.connect(**config)
                name = name.get_text().strip()
                name = name.encode('UTF-8', 'ignore')
                price = price.get_text()
                area = re.findall(r'(\w*[0-9]+\.*[0-9]+)\w*',area.get_text())
                price_per_area = float(price)/float(area[0])
                print(price,'-----',area,'-----',price_per_area,'-----------\n')
                try:
                     with connection.cursor() as cursor:
                     # 执行sql语句，插入记录
                         sql = 'INSERT INTO house (date, house_name, house_price, house_area, source, price_per_area) VALUES (%s, %s, %s, %s, %s, %s)'
                         cursor.execute(sql, (present_date, name, price, area, source, price_per_area))
                     # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
                     connection.commit()
                finally:
                     connection.close()
        time.sleep(1)

delete_today_data(config)

url_number = 36
source =['fangdd','lianjia','iwjw']

fangdd_url = get_fangdd_url(url_number)
get_fangdd_house(fangdd_url,source[0])

lianjia_url = get_lianjia_url(url_number)
get_lianjia_house(lianjia_url,source[1])

iwjw_url = get_iwjw_url(url_number)
get_iwjw_house(iwjw_url,source[2])