# -*- coding: UTF-8 -*-

import re

import requests
from bs4 import BeautifulSoup
import json
import time
import traceback

import pycurl


class WXPusher:
    def __init__(self, usr, msg):
        self.base_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?'
        self.req_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='
        self.corpid = 'ww53cfec8fec6c6ec9'     # 上面提到的你的企业ID
        self.corpsecret = 'fi7pfkEL_OH_W8TqLY8R_pqcF6xQE1Riknt5VlerMCI'     # 上图的Secret
        self.agentid = 1000004          # 填写你的企业ID，不加引号，是个整型常数,就是上图的AgentId
        self.usr = usr
        self.msg = msg

    def get_access_token(self):
        urls = self.base_url + 'corpid=' + self.corpid + '&corpsecret=' + self.corpsecret
        resp = requests.get(urls).json()
        access_token = resp['access_token']
        return access_token

    def send_message(self):
        data = self.get_message()
        req_urls = self.req_url + self.get_access_token()
        res = requests.post(url=req_urls, data=data)
        print(res.text)

    def get_message(self):
        data = {
            "touser": self.usr,
            "toparty": "@all",
            "totag": "@all",
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {
                "content": self.msg
            },
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        data = json.dumps(data)
        return data

class HtmlDowloader(object):
    """docstring for UrlManger"""

    def __init__(self):
        pass

    def download(self, url):
        if url is None:
            return None
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}
        try:
            response = requests.get(url, headers=headers)
        except:
            err_str = traceback.format_exc()
            print(err_str)
        # Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0

        if response.status_code != 200:
            print(response.status_code)  # 有几次爬的太频繁了，直接被网站禁止访问了。一直不知道哪有错，直到打印了状态码才找到问题，这句还很重要。
            return None
        return response.content


class HtmlParser(object):
    """docstring for HtmlParser"""

    def __init__(self):
        pass

    def _get_id(self, url):
        id = url[:-1]
        id = id[id.rfind('/') + 1:]
        return int(id)

    def _get_new_urls(self, soup):
        res = list()
        # links1=soup.find_all('a',href=re.compile(r"/topic/\d+"))
        links_topic = soup.find_all('a', href=re.compile(r"/topic/\d+"))
        for link1 in links_topic:
            one = dict()
            title = link1.get_text().strip()
            my_url = link1.attrs['href']
            one['title'] = title
            one['url'] = my_url
            one['id'] = self._get_id(my_url)
            res.append(one)

        return res

    def parse(self, html_cont):
        if html_cont is None:
            return
        soup = BeautifulSoup(html_cont, "html.parser", from_encoding='utf-8')
        res = self._get_new_urls(soup)
        return res


def write_message(message, bot_url):
    content = message['title']
    url = message['url']
    content = content + '\n'+'<a href=\"'+url+'\">链接</a>'
    test = WXPusher(usr='@all', msg=content)
    test.send_message()



class HtmlOutputer(object):
    """docstring for HtmlOutputer"""

    def __init__(self):
        pass

    def output(self):
        print('craw successfully')

    def collect_data(new_data):
        print('get new data successfully')


class SpiderMain(object):
    """docstring for SpiderMain"""

    def __init__(self, url, page_num):
        # super(SpiderMain, self).__init__()
        # self.arg = arg# self.arg=arg
        print('SpiderMain begin')
        self.urls = list()
        if page_num == 1:
            self.urls.append(url)
        else:
            for i in range(0, page_num):
                self.urls.append(url + '?start=' + str(i * 25))

        # print(type(self.urls))
        # print(self.urls)
        self.downloader = HtmlDowloader()
        self.parser = HtmlParser()

    def craw(self):
        res = list()
        for new_url in self.urls:
            try:
                # print(new_url)
                # print(new_url.get_text())
                html_cont = self.downloader.download(new_url)

                res.extend(self.parser.parse(html_cont))

            except:
                print('craw failed')
        return res

    def monitor_douban(self, group_name, keywords, send_message_bots):
        while True:
            try:
                try:
                    f = open(group_name + '_timestamp')
                    last_time = f.read()
                    f.close()
                except Exception:
                    last_time = '0'

                last_time = int(last_time)
                datas = self.craw()

                max_id = 0

                res = list()

                for data in datas:
                    try:
                        if data['id'] > max_id:
                            max_id = data['id']
                        title = data['title']
                        match_keyword = False
                        for keyword in keywords:
                            if title.startswith(keyword):
                                match_keyword = True
                                break

                        if not match_keyword:
                            continue

                        if data['id'] <= last_time:
                            continue
                        link = data['url']
                        message = {}
                        message['title'] = title
                        message['url'] = link
                        res.append(message)
                    except AttributeError:
                        print('解析异常')
                        continue
                if (len(res) == 0):
                    print('本次无开车数据')
                f = open(group_name + '_timestamp', 'w')
                f.write(str(max_id))
                f.close()
                for message in reversed(res):
                    for bot in send_message_bots:
                        write_message(message, bot)

                    print(message)
                    if len(res) > 20:
                        time.sleep(3)

            except Exception:
                print('解析异常')
            time.sleep(200)


if __name__ == '__main__':
    root_url = 'https://www.douban.com/group/656297/discussion'
    page_num = 5
    # print('main begin')
    obj_spider = SpiderMain(root_url, page_num)
    res = obj_spider.craw()

    print(res)
