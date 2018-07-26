#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    File Name:     r
    Author:        Administrator
    Date:          2018/7/25
    Description:   
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃       ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃  永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
__author__ = 'Administrator'

def ERR(msg=''):
    return {
        'result':-1,
        'msg':msg
    }
def OK(msg=''):
    return {
        'result':0,
        'msg':msg
    }
def POST_ARGS(handler,keys):
    ret = {}
    for k in keys:
        v = handler.get_body_arguments(k,[None])[0]
        ret[k] = v
    return ret
if __name__ == "__main__":
    print('main')