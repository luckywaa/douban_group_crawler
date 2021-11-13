# -*- coding: UTF-8 -*-


import requests
import traceback
import json
import time


class HtmlDowloader(object):
    """docstring for UrlManger"""

    def __init__(self):
        pass

    def download(self, url, data):
        if url is None:
            return None
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}
        try:
            response = requests.post(url, data=data, headers=headers)
        except:
            err_str = traceback.format_exc()
            print(err_str)
        # Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0

        if response.status_code != 200:
            print(response.status_code)  # 有几次爬的太频繁了，直接被网站禁止访问了。一直不知道哪有错，直到打印了状态码才找到问题，这句还很重要。
            return None
        return response.content


res = set()
url = 'https://wap.hn.10086.cn/shop/simConfirm/getQueryNumsH5Online'
data = {'orderPreId':'898600E1181891086489'}
downloader = HtmlDowloader()
size = 0
while True:
    out = downloader.download(url,data)
    out = json.loads(out)
    for my_data in out['data']:
        res.add(str(my_data['serialNumber']+'\n'))
    time.sleep(10)
    f = open('numbers.txt','w')
    f.writelines(res)
    f.close()
    if size == len(res):
        break

    print(len(res))


