# get请求
import urllib.request


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Host": "httpbin.org"
}
proxies = {
    "http": "https://127.0.0.1：7890"
}
req = urllib.request.Request("https://httpbin.org/get", headers=headers, proxies=proxies)  # req本质上就是url
# r = urllib.request.urlopen(req)


proxy_handler = urllib.request.ProxyHandler(proxies)
opener = urllib.request.build_opener(proxy_handler)
r = opener.open(req)

print(r.status)
print(r.msg)
print(r.read().decode())