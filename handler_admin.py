
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
class AdminHandler(pyrestful.rest.RestHandler):
    @get(_path="/admin")
    def get_index(self):
        print("admin")
        self.redirect("admin/index")

    @get(_path="/admin/index")
    def get_page(self):
        hq_cookie = self.get_cookie('xr_cookie')  # 获取浏览器cookie
        print(hq_cookie)
        session = gl.gl_session.get(hq_cookie, None)  # 将获取到的cookie值作为下标，在数据字典里找到对应的用户信息字典
        if not session:  # 判断用户信息不存在
            self.redirect("/admin/login")
        else:
            if session.get('is_login', None) == True:  # 否则判断用户信息字典里的下标is_login是否等于True
                self.render("admin/index.html")
            else:
                self.redirect("/admin/login")

    @get(_path="/admin/login")
    def get_login(self):
        self.render("admin/login.html")

    @post(_path="/admin/login")
    def post_login(self):
        user = self.get_argument('user')  # 接收用户输入的登录账号
        pwd = self.get_argument('pwd')  # 接收用户输入的登录密码
        if user == 'admin' and pwd == 'admin':  # 判断用户的密码和账号

            obj = hashlib.md5()  # 创建md5加密对象
            obj.update(bytes(str(time.time()), encoding="utf-8"))  # 获取系统当前时间，传入到md5加密对象里加密
            key = obj.hexdigest()  # 获取加密后的密串
            gl.gl_session[key] = {}  # 将密串作为下标到container字典里，创建一个新空字典
            gl.gl_session[key]['yhm'] = user  # 字典里的键为yhm，值为用户名
            gl.gl_session[key]['mim'] = pwd  # 字典里的键为mim，值为用户密码
            gl.gl_session[key]['is_login'] = True  # 字典里的键为is_login，值为True
            self.set_cookie('xr_cookie', key, expires_days=1)  # 将密串作为cookie值写入浏览器
            self.redirect("index")  # 跳转到查看页面
        else:
            self.redirect("login")



