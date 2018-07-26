#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'wyb'
__mtime__ = '2018/7/12'
"""
import requests
session = requests.session()

def get_result(url,data={}):
    result = session.get(url,data=data)
    print('url:  %s    ===================================================================================' % url)
    print(result.status_code,result.text)
   # assert int(result.status_code) < 400
    return result.text

def post_result(url,data={}):
    result = session.post(url,data)
    print('url:  %s    ===================================================================================' % url)
    print(result.status_code, result.text)
    # assert int(result.status_code) < 400
    return result.text

def post_file(url,data,files={}):
    print('url:  %s    ===================================================================================' % url)
    result = session.request('post', url,
            params=None, data=data, headers=None, cookies=None, files=files,
            auth=None, timeout=5, allow_redirects=True, proxies=None,
            hooks=None, stream=None, verify=None, cert=None, json=None)
    print(result.status_code, result.text)
    # assert int(result.status_code) < 400
    return result.text

def get_download(url,data,fn):
    if not fn:
        print("文件名不能为空")
    print('url:  %s    ===================================================================================' % url)
    result = session.get(url,data=data)
    print(result.status_code,'download file %s succeed!')
    if int(result.status_code) < 400:
        ct = result.content
        with open(fn,'wb') as file:
            file.write(ct)

def post_download(url,data,fn):
    print('url:  %s    ===================================================================================' % url)
    result = session.post(url,data=data)
    print(result.status_code, 'download file %s succeed!')
    if int(result.status_code) < 400:
        ct = result.content
        with open(fn, 'wb') as file:
            file.write(ct)


if __name__ == "__main__":
    get_result('https://www.baidu.com')