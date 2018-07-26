#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    File Name:     Test
    Author:        Administrator
    Date:          2018/7/26
    Description:   Test Model ,table :t_test
"""
__author__ = 'Administrator'
import json
class Test(object):
    def __init__(self, id,name):
        self.id = id
        self.name = name

    def to_string(self):
        return json(self)
    def to_dict(self):
        ret = {
            "id":self.id,
            "name":self.name
        }
        return ret
    def to_not_null_dict(self):
        ret = {}
        if self.id:
            ret['id'] = self.id
        if self.name:
            ret['name'] = self.name
        return ret
if __name__ == "__main__":
    print('main')