#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    File Name:     user_service
    Author:        Administrator
    Date:          2018/7/25
    Description:
"""
__author__ = 'Administrator'
import json
from dao.test_dao import TestDao
from base import r
class TestService():
    tdao = TestDao()
    def add_test(self,test):
        ret,msg = self.tdao.add_test(test)
        return ret,msg

if __name__ == "__main__":
    print('main')