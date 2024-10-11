# get请求
import urllib.request

import pymysql.cursors


from lxml import etree

from bs4 import BeautifulSoup

import re

# 数据库连接
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             database='pymysql',
                             cursorclass=pymysql.cursors.DictCursor)

# 创建一个申请（request如同一个URL）
h = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
}
req = urllib.request.Request("https://movie.douban.com/top250", headers=h)

r = urllib.request.urlopen(req)

# print(r.status)
# print(r.read().decode())
r = urllib.request.urlopen(req)
html_doc = r.read().decode()


# 使用bs4或者re提取信息
soup = BeautifulSoup(html_doc, "html.parser")
#
items = soup.find_all("div", class_="item")  # 查找文档里某个标签
# print(items)
with connection:
    for item in items:
        img = item.find("div", class_="pic").a.img
        name = img['alt']
        url = img['src']
        # print("="*50)
        # 拔爬出来的数据存储到MySQL
        with connection.cursor() as cursor:
            # 创建一个新的记录
            sql = "INSERT INTO `movie_info`(`movie_name`, `movie_url`) VALUE (%s, %s)"
            cursor.execute(sql, (name, url))
    connection.commit()