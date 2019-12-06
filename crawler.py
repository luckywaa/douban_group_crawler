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


def monitor_douban(root_url, group_name, keywords, send_message_bots):
    while True:
        try:
            last_time = ''
            try:
                f = open(group_name + '_timestamp')
                last_time = f.read()
                f.close()
            except Exception:
                last_time = '0.0'

            last_time = float(last_time)
            d = feedparser.parse(root_url)
            feed_time = d.feed.published_parsed

            feed_time = time.mktime(feed_time)

            open_time_str = time.localtime(feed_time + 28800)
            open_time_str = time.strftime('%Y-%m-%d %H:%M:%S', open_time_str)
            print('监控时间:' + open_time_str)

            f = open(group_name + '_timestamp', 'w')
            f.write(str(feed_time))
            f.close()

            res = list()
            if feed_time != last_time:
                for entry in d.entries:
                    try:

                        title = str(entry.title)
                        title = title[0:str(title).rindex('(')]
                        match_keyword = False
                        for keyword in keywords:
                            if title.startswith(keyword):
                                match_keyword = True
                                break

                        if not match_keyword:
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
                    for bot in send_message_bots:
                        write_message(message, bot)

                    print(message)
                    if len(res) > 20:
                        time.sleep(3)
            else:
                print('本次获取到的数据没有更新')
        except Exception:
            pass
        time.sleep(120)
