
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
import traceback
import gl
import hashlib  # 导入md5加密模块
import time  # 导入时间模块
import sys

class ForuHandler(pyrestful.rest.RestHandler):
    @get(_path="/foru")
    def get_index(self):
        self.render("foru/index.html")



