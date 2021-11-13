# -*- coding: UTF-8 -*-

import crawler1

if __name__ == '__main__':
    keywords = list()
    keywords.append('【开车】')
    keywords.append('[开车]')
    keywords.append('【羊毛】')
    keywords.append('[羊毛]')

    bots = list()
    bots.append('https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ca1db5f1-0f28-469a-b845-bca5a8021471')
    craw = crawler1.SpiderMain('https://www.douban.com/group/669481/discussion', 5)
    craw.monitor_douban(
        'kaiche',
        keywords,
        bots
    )
