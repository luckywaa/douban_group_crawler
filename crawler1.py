# -*- coding: UTF-8 -*-

import re

import requests
from bs4 import BeautifulSoup
import json
import time
import traceback

import pycurl

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


    def _get_new_urls(self,soup):
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
    c = pycurl.Curl()
    c.setopt(pycurl.URL, bot_url)
    c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json'])
    # c.setopt(pycurl.USERAGENT, 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML， like Gecko) Chrome/45.0.2454.101 Safari/537.36')
    post_data = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    c.setopt(pycurl.POSTFIELDS, json.dumps(post_data))
    c.perform()
    c.close()

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
                        if data['id']>max_id:
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

                        res.append(title + '\n' + link)
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
            time.sleep(600)



if __name__ == '__main__':
    root_url = 'https://www.douban.com/group/656297/discussion'
    page_num = 5
    # print('main begin')
    obj_spider = SpiderMain(root_url, page_num)
    res = obj_spider.craw()




    print(res)

