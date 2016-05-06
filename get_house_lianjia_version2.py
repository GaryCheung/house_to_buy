from bs4 import BeautifulSoup
import requests
from _datetime import date,datetime
import time
import pymysql
import re
from urllib.parse import quote

house_name = ['古桐公寓',
              '三泾南宅',
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
              '汤臣豪园'
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
            sql = "DELETE FROM house WHERE date = '%s' and source = 'lianjia'" %(present_date)
            cursor.execute(sql)
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        connection.commit()
    finally:
        connection.close()
    print('-----------------------delete success!----------------','\n')

def get_lianjia_url(url_number,housename):
    print('--------------------------',url_number,housename)
    urls = []
    url_begin = 'http://sh.lianjia.com/ershoufang/rs'
    for i in range(1,url_number+1):
        urls.append(i)
        url_middle = quote(housename[i-1])
        #print(url_middle)
        urls[i-1] = url_begin + url_middle
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

delete_today_data(config)
url_number = len(house_name)
source =['fangdd','lianjia','iwjw']

lianjia_url = get_lianjia_url(url_number,house_name)
get_lianjia_house(lianjia_url,source[1])