
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
import service
class UserHandler(pyrestful.rest.RestHandler):

    @get(_path="/test")
    def get_index(self):
        self.finish(' test')

    @get(_path="/user/list")
    def get_user_list(self):
        user_service = service.user_service.UserService()
        users = user_service.get_user_list()
        self.finish(users)

