
import tornado.web
import pyrestful.rest
import json
import jieba
import sys
import os
import datetime
sys.path.append("..")
from database import dbHelper
import logging
from pyrestful.rest import get, post, put, delete
from pyrestful import mediatypes
from database import redisdb
import traceback
import gl
import hashlib  # 导入md5加密模块
import time  # 导入时间模块
import sys
import re
import requests
class UserHandler(pyrestful.rest.RestHandler):

    @get(_path="/test")
    def get_index(self):
        self.finish(' test')

    @get(_path="/user/get_user_list")
    def get_user_list(self):
        users = [
            {"id":'1','name':'aaa'},
            {"id": '2', 'name': 'bbb'},
            {"id": '3', 'name': 'ccc'}
        ]
        self.finish(json.dumps(users))

