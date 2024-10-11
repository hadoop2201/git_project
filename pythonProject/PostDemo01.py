# post请求
import requests

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Host": "httpbin.org"}

# 伪装代理（ip）
proxies = {
    "http": "https://127.0.0.1：7890",
}
data = {
    'username': 'sy19617016',
    'password': 'sy123321',
    'authcode': '',  # 模仿验证码
    'toUrl': '',
    'app': 'account.login',
}

r = requests.post('https://www.nowapi.com/', headers=headers, proxies=proxies, data=data)


print(r.text)
