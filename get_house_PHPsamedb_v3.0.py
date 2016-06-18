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
              '由由一村',
              '由由三村',
              '由由四村',
              '由由五村',
              '由由六村',
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
              '古桐一村',
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
              '玉兰香苑',
              '昭化小区',
              '宁康小区',
              '中山公寓',
              '煜王苑',
              '临沂一村',
              '临沂二村',
              '临沂三村',
              '临沂四村',
              '临沂五村',
              '临沂六村',
              '汇智湖畔家园',
              '伟莱家园',
              '东方丽景',
              '水仙苑',
              '明中龙祥',
              '旭辉亚瑟郡'
              ]

config = {
    'host':'127.0.0.1',
    'port':8889,
    'user':'root',
    'password':'root',
    'db':'house',
    'charset':'utf8',
    'unix_socket':'/Applications/MAMP/tmp/mysql/mysql.sock'
}

present_date = datetime.now().date()

def delete_today_data(config):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            # 执行sql语句，插入记录
            sql = "DELETE FROM house WHERE date = '%s' and source = 'fangdd'" %(present_date)
            cursor.execute(sql)
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        connection.commit()
    finally:
        connection.close()
    print('-----------------------delete success!----------------','\n')

def get_fangdd_url(url_number,housename):
    print('--------------------------',url_number,housename)
    urls = []
    url_begin = 'http://esf.fangdd.com/shanghai?query='
    url_end = '&city_id=121'      #上海房源
    for i in range(1,url_number+1):
        urls.append(i)
        url_middle = quote(housename[i-1])
        #print(url_middle)
        urls[i-1] = url_begin + url_middle + url_end
    return urls

def get_fangdd_house(urls,source):
    flag = 0
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
                print(name,'#######',price,area)
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
        flag = flag + 1
        print('#######################',flag)
    time.sleep(1)
    return flag

#delete_today_data(config)
flag = 38
house_name = house_name[flag:]

url_number = len(house_name)
source =['fangdd','lianjia','iwjw']

fangdd_url = get_fangdd_url(url_number,house_name)
go_on = get_fangdd_house(fangdd_url,source[0])