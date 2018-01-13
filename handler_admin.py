
import tornado.web
import pyrestful.rest
import json
import jieba
import sys
import datetime
sys.path.append("..")
from database import dbHelper
import logging
from pyrestful.rest import get, post, put, delete
from pyrestful import mediatypes
import traceback
import gl

class AdminHandler(pyrestful.rest.RestHandler):

    @get(_path="/admin")
    def getpage(self):
        hq_cookie = self.get_cookie('xr_cookie')  # 获取浏览器cookie
        session = gl.gl_session.get(hq_cookie, None)  # 将获取到的cookie值作为下标，在数据字典里找到对应的用户信息字典
        if not session:  # 判断用户信息不存在
            self.redirect("/admin/login")
        else:
            if session.get('is_login', None) == True:  # 否则判断用户信息字典里的下标is_login是否等于True
                self.render("admin/index.html")
            else:
                self.redirect("/admin/login")

    @get(_path="/admin/login")
    def login(self):
        self.render("admin/login.html")