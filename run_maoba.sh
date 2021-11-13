#!/bin/bash
# 使用阿里云源安装必须组件
pip install -i https://mirrors.aliyun.com/pypi/simple/ --upgrade pip
pip install -i https://mirrors.aliyun.com/pypi/simple/ -r /app/requirements.txt

python /app/maoba_crawler1.py
