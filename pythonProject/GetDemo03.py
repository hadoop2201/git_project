# get请求
import requests

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Host": "httpbin.org"}

# 伪装代理（ip）
proxies = {
    'http': 'http://47.93.121.200:80',
    'https': 'https://47.93.121.200:80',
}

r = requests.get('http://httpbin.org/get', headers=headers, proxies=proxies)


print(r.text)
