import requests
import pymysql
from lxml import etree
import re

# 数据库连接
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    database='pymysql',
    cursorclass=pymysql.cursors.DictCursor
)
#  伪装头
h = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}
# 伪装IP
proxies = {
    'http': '127.0.0.1:7890',
    'https': '127.0.0.1:7890'
}


def get_first_text(list_of_texts):
    """安全地返回文本列表中的第一个元素"""
    if list_of_texts:
        return list_of_texts[0].strip() if list_of_texts[0] is not None else ""
    return ""


def extract_director(text):
    """使用正则表达式提取导演名字"""
    match = re.search(r'导演: ([^ ]+)', text)
    return match.group(1) if match else text.strip()


def extract_actors(text):
    """使用正则表达式提取主演名字"""
    match = re.search(r'主演: ([^ ]+)', text)
    return match.group(1) if match else ""


# 生成需要抓取的URL列表
urls = [f'https://movie.douban.com/top250?start={i * 25}&filter=' for i in range(10)]

with connection:
    with connection.cursor() as cursor:
        try:
            for url in urls:
                response = requests.get(url, headers=h, proxies=proxies)
                html = etree.HTML(response.text)

                # 获取每部电影的列表
                lis = html.xpath('//*[@id="content"]/div/div[1]/ol/li')

                for li in lis:
                    # 提取图片地址
                    img = get_first_text(li.xpath('div/div[1]/a/img/@src'))

                    # 提取其他数据字段
                    title = get_first_text(li.xpath('div/div[2]/div[1]/a/span[1]/text()'))
                    src = get_first_text(li.xpath('div/div[2]/div[1]/a/@href'))

                    # 获取导演和主演信息
                    director_info = get_first_text(li.xpath('div/div[2]/div[2]/p[1]/text()'))
                    director = extract_director(director_info)
                    actors = extract_actors(director_info)

                    # 提取类型、评价和引用
                    type = get_first_text(li.xpath('div/div[2]/div[2]/p[1]/text()[2]')).strip()
                    comment = get_first_text(li.xpath('div/div[2]/div[2]/div/span[4]/text()'))
                    quote = get_first_text(li.xpath('div/div[2]/div[2]/p[2]/span/text()'))

                    # 将数据插入数据库
                    sql = """
                        INSERT INTO `movie_info2`(img, title, src, director, actors, type, comment, quote)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (img, title, src, director, actors, type, comment, quote))

            # 在循环结束后提交事务
            connection.commit()
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            cursor.close()
