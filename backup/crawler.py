# -*- coding: UTF-8 -*-
import json
import time

import feedparser
import pycurl


def write_message(message, bot_url):
    c = pycurl.Curl()
    c.setopt(pycurl.URL, bot_url)
    c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json'])
    post_data = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    c.setopt(pycurl.POSTFIELDS, json.dumps(post_data))
    c.perform()
    c.close()


if __name__ == '__main__':
    root_url = 'https://www.douban.com/feed/group/656297/discussion'
    # root_url = 'c.xml'
    # print('main begin')
    # obj_spider = SpiderMain()
    # obj_spider.craw(root_url)
    while True:
        try:
            f = open('timestamp')
            last_time = f.read()
            f.close()

            last_time = float(last_time)
            d = feedparser.parse(root_url)
            feed_time = d.feed.published_parsed

            feed_time = time.mktime(feed_time)

            open_time_str = time.localtime(feed_time + 28800)
            open_time_str = time.strftime('%Y-%m-%d %H:%M:%S', open_time_str)
            print('监控时间:' + open_time_str)

            f = open('timestamp', 'w')
            f.write(str(feed_time))
            f.close()

            res = list()
            if feed_time != last_time:
                for entry in d.entries:
                    try:
                        title = entry.title[0: -12]
                        if not title.startswith('【开车】') and not title.startswith('[开车]'):
                            continue

                        structed_time = entry.published_parsed
                        structed_time = time.mktime(structed_time)
                        open_time_str = time.localtime(structed_time + 28800)
                        open_time_str = time.strftime('%Y-%m-%d %H:%M:%S', open_time_str)
                        if structed_time <= last_time:
                            break
                        link = entry.link

                        res.append(title + '\n' + link + '\n' + open_time_str)
                    except AttributeError:
                        print('解析异常')
                        continue
                if (len(res) == 0):
                    print('本次无开车数据')
                for message in reversed(res):
                    write_message(message,'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=99e2a51d-16fc-48da-ad0e-f095c3accea8')
                    write_message(message,'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=6423fdf6-043c-46e3-a85e-8bee92e58524')
                    print(message)
                    if len(res) > 20:
                        time.sleep(3)
            else:
                print('本次获取到的数据没有更新')
        except Exception:
            pass
        time.sleep(120)

