
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

class MessageHandler(pyrestful.rest.RestHandler):
    def err(self,s):
        return {
            "ret":0,
            "msg":s
        }

    @get(_path="/message")
    def get_index(self):
        self.render("message/index.html")

    @post(_path="/message/submit_message",_produces=mediatypes.APPLICATION_JSON)
    def add_message(self):
        message = self.get_body_argument("message", None)
        nickname = self.get_body_argument("nickname", None)

        if not nickname or nickname == "":
            nickname = "匿名用户"
        if not message or message == "":
            return self.err("");

        print(message,nickname)
        return {
            '昵称': nickname,
            '留言内容':message,
            'message':",能正确接收数据但是还没有做入库处理！"

        }
