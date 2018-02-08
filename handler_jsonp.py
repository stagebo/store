
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

class JsonpHandler(pyrestful.rest.RestHandler):

    @get(_path="/jsonp/test")
    def get_test(self):
        callback = self.get_argument('callback','callback')

        now = datetime.datetime.now()
        tar = datetime.datetime(2017,6,6, 21,0, 0)
        d = now - tar

        data = {
            'days':d.days,
            'seconds':d.seconds
        }

        ret = '%s(%s);'%(callback,json.dumps(data))
        self.finish(ret)


