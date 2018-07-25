
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
from service import user_service
class UserHandler(pyrestful.rest.RestHandler):

    @get(_path="/test")
    def get_index(self):
        self.finish(' test')

    @get(_path="/user/list")
    def get_user_list(self):
        us = user_service.UserService()
        users = us.get_user_list()
        self.finish(json.dumps(users))

    def get_user_by_id(self,id):
        user = user_service.UserService().get_user_by_id(id)
        self.finish(json.dumps(user))
