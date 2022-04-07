import urllib.request
import UA

url = 'https://www.bilibili.com'
headers = {
    'User-Agent': UA.getRandomUA()  # 这里就调用了自己的工具库的方法来随机获取UA
}
request = urllib.request.Request(url=url, headers=headers)

response = urllib.request.urlopen(request)
con = response.read().decode('utf-8')

print(con)
