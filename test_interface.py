# -*- coding: utf-8 -*-

from flask import Flask
from flask import jsonify
from flask import Response
import requests
import json
import time

app = Flask(__name__)

host = 'http://172.16.0.51:9999/predict'


def predict():
    start_time = time.time()

    test_text_ls = [line.strip() for line in
                    open('E:/test_debug.txt', 'r', encoding='utf8').readlines()]
    post_data = {
        "topn": 5,
        "query": test_text_ls
    }
    json_data = post_data
    results = requests.request(method='post', url=host, json=json_data).text
    results = json.loads(results)['data']
    for j, item in enumerate(results):
        print('原句  :', item[0]['query'])
        for i, it in enumerate(item):
            print('相似题{}: {}--{}--{}'.format(i + 1, it['cwe'], it['probability'], it['similar_sent']))
        print('*' * 80 + '\n')

    end_time = time.time()
    print('Cost time:{} s'.format(end_time - start_time))
    print('Each sample cost time:{} s'.format((end_time - start_time) / len(test_text_ls)))


if __name__ == '__main__':
    predict()
