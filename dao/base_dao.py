#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    File Name:     base_dao
    Author:        Administrator
    Date:          2018/7/26
    Description:
"""
__author__ = 'Administrator'


from sqlalchemy import *
from sqlalchemy.orm import *
from base import cnf
from model.test import Test
class BaseDao():
    def __init__(self):
        '''
            # 这个方法就是类的构造函数，对象创建的时候自动运行
        '''
        self.engine = create_engine(  # 生成连接字符串，有特定的格式
            cnf.database_setting['database_type'] +
            '+' +
            cnf.database_setting['connector'] +
            '://' +
            cnf.database_setting['user_name'] +
            ':' +
            cnf.database_setting['password'] +
            '@' +
            cnf.database_setting['host_name'] +
            '/' +
            cnf.database_setting['database_name']
        )
        # self.engine = create_engine('mysql+pymysql://root:w1254117589@urmyall.xyz:3306/ycjj')
        self.metadata = MetaData(self.engine)


if __name__ == "__main__":
    print('main')