from bs4 import BeautifulSoup
import requests
from _datetime import date,datetime
import time
import pymysql
import re
from urllib.parse import quote

house_name = ['古桐公寓',
              '三泾南宅小区',
              '中阳小区',
              '朗诗绿色街区',
              '长宁路1600弄',
              '春天花园',
              '三泾北宅',
              '金杨五街坊',
              '金杨二街坊',
              '由由七村',
              '由由二村',
              '绿波城',
              '毕加索小镇',
              '金利公寓',
              '兆丰花园',
              '上海康城',
              '齐爱佳苑',
              '上海花城',
              '凯欣豪园',
              '天山中华园',
              '上海阳城',
              '水语人家',
              '华润中央公园',
              '科宁公寓',
              '延西小区',
              '保利叶语',
              '金地艺境',
              '春港丽园',
              '古桐五村',
              '古桐二村',
              '古桐六村',
              '古桐四村',
              '古桐三村',
              '建中路461弄',
              '建中路171弄',
              '汤臣豪园',
              '奥林匹克花园',
              '武夷花园',
              '精益公寓',
              '长宁路1488弄',
              '新青浦佳园',
              '新青浦花苑',
              '武夷大楼',
              '交江大楼',
              '玉兰香苑'
              ]

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
            sql = "DELETE FROM house WHERE date = '%s' and source = 'iwjw'" %(present_date)
            cursor.execute(sql)
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        connection.commit()
    finally:
        connection.close()
    print('-----------------------delete success!----------------','\n')


def get_iwjw_url(url_number,housename):
    print('--------------------------',url_number,housename)
    urls = []
    url_begin = 'http://www.iwjw.com/sale/shanghai/?kw='
    for i in range(1,url_number+1):
        urls.append(i)
        url_middle = quote(housename[i-1])
        #print(url_middle)
        urls[i-1] = url_begin + url_middle
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
            house_name = soup.select('div.mod-lists.mb50.clearfix > div:nth-of-type(1) > ol > li > div.f-l > h4 > b > a > span > span:nth-of-type(1)')
            house_area = soup.select('div.mod-lists.mb50.clearfix > div:nth-of-type(1) > ol > li > div.f-l > h4 > b > a > span > span:nth-of-type(3)')
            house_price = soup.select('div.mod-lists.mb50.clearfix > div:nth-of-type(1) > ol > li > div.house-price > span.total-text')
            print(house_name)
            for name,price,area in zip (house_name,house_price,house_area):
                print(name,price,area)
                connection = pymysql.connect(**config)
                name = name.get_text().strip()
                name = name.encode('UTF-8', 'ignore')
                price = price.get_text()
                area = re.findall(r'(\w*[0-9]+\.*[0-9]*)\w*',area.get_text())
                print('----------------------',area)
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
url_number = len(house_name)
source =['fangdd','lianjia','iwjw']

iwjw_url = get_iwjw_url(url_number,house_name)
get_iwjw_house(iwjw_url,source[2])