
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
import gl
class ChatbotHandler(pyrestful.rest.RestHandler):
    @get(_path="/chatbot")
    def get_index(self):
        self.render("chatbot/index.html")

    @get(_path="/chatbot/getresponse",_produces=mediatypes.APPLICATION_JSON)
    def get_response(self,question):
        rel = str(gl.gl_chatbot.get_response(question))
        return {"data":rel}


