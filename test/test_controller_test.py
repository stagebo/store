# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import configparser
import sys
import datetime
import xlrd
import req
web_address = "http://localhost:8001"
session = requests.Session()



if __name__ == "__main__":
    # web_address = "http://www.iotqsgf.com:9101"
    print("主机地址：%s"%web_address)

    # 1
    data = {'id':8,'name':'test post'}
    ret = req.post_result( '%s/test/addtest' % web_address,data=data)
