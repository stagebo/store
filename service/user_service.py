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
from dao import user_dao
from base import r
class UserService():

    def get_user_list(self):
        ud = user_dao.UserDAO()
        users = ud.get_user_list()
        ret = {
            'result': 0,
            'msg': '',
            'payload': users
        }
        return ret
    def get_user_by_id(self,id):
        user = user_dao.UserDAO().get_user_by_id(id)

        if not user:
            return r.err_result('用户不存在！')
        ret = {
            'result': 0,
            'msg': '',
            'payload':user
        }
        return ret
if __name__ == "__main__":
    print('main')