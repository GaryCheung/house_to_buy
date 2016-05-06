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
            sql = "DELETE FROM house WHERE date = '%s' AND source = 'lianjia'" %(present_date)
            cursor.execute(sql)
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        connection.commit()
    finally:
        connection.close()
    print('-----------------------delete success!----------------','\n')

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

url_number = 27
source =['fangdd','lianjia','iwjw']

lianjia_url = get_lianjia_url(url_number)
get_lianjia_house(lianjia_url,source[1])