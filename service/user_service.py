#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    File Name:     user_service
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
import json


class UserService():

    def get_user_list(self):
        users = {
            'result':0,
            'msg':'',
            'payload': [
            {"id": '1', 'name': 'aaa'},
            {"id": '2', 'name': 'bbb'},
            {"id": '3', 'name': 'ccc'}
        ]
        }
        return json.dumps(users)
if __name__ == "__main__":
    print('main')