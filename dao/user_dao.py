#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    File Name:     user_dao
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

class UserDAO():

    def get_user_list(self):
        return  [
            {"id": '1', 'name': 'aaa'},
            {"id": '2', 'name': 'bbb'},
            {"id": '3', 'name': 'ccc'}
        ]
    def get_user_by_id(self,id):
        for u in  [
            {"id": '1', 'name': 'aaa'},
            {"id": '2', 'name': 'bbb'},
            {"id": '3', 'name': 'ccc'}
        ]:
            if str(id) == str(u['id']):
                return u
        return {}
if __name__ == "__main__":
    print('main')