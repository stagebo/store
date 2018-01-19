
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

class AdminHandler(pyrestful.rest.RestHandler):
    """
        this is admin handler api.

        this object provides some method to query and controll system

        :param None:

        """
    def _right(self):
        # return True
        hq_cookie = self.get_cookie('xr_cookie')  # 获取浏览器cookie
        session = gl.gl_session.get(hq_cookie, None)  # 将获取到的cookie值作为下标，在数据字典里找到对应的用户信息字典
        if not session:  # 判断用户信息不存在
            return False
        else:
            if session.get('is_login', None) == True:  # 否则判断用户信息字典里的下标is_login是否等于True
                return True
            else:
                return False

    @get(_path="/admin")
    def get_index(self):
        self.redirect("admin/index")

    @get(_path="/admin/index")
    def get_page(self):
        if self._right():  # 否则判断用户信息字典里的下标is_login是否等于True
            self.render("admin/index.html")
        else:
            self.redirect("/admin/login")

    @get(_path="/admin/login")
    def get_login(self):
        self.render("admin/login.html")

    @post(_path="/admin/login",_produces=mediatypes.APPLICATION_JSON)

    def post_login(self):
        """
             - 功能:    登陆后台.
             - URL:     /admin/login
             - HTTP:    POST
             - 参数:    无
             - 返回值:
                        * 正确,{"rel": 1,"msg": "" }
                        * 错误:{ "rel":0,"msg":"用户名或密码错误！" }
        """
        user = self.get_body_argument("user",None)
        pwd = self.get_body_argument("pwd",None)
        if user == 'admin' and pwd == 'admin':  # 判断用户的密码和账号
            obj = hashlib.md5()  # 创建md5加密对象
            obj.update(bytes(str(time.time()), encoding="utf-8"))  # 获取系统当前时间，传入到md5加密对象里加密
            key = obj.hexdigest()  # 获取加密后的密串
            rd = self.application.redis

            gl.gl_session[key] = {}  # 将密串作为下标到container字典里，创建一个新空字典
            gl.gl_session[key]['username'] = user  # 字典里的键为yhm，值为用户名
            gl.gl_session[key]['password'] = pwd  # 字典里的键为mim，值为用户密码
            gl.gl_session[key]['is_login'] = True  # 字典里的键为is_login，值为True
            self.set_cookie('xr_cookie', key, expires_days=1)  # 将密串作为cookie值写入浏览器
            return {
                "rel": 1,
                "msg": ""
            }
        else:
            return {
                "rel":0,
                "msg":"用户名或密码错误！"
            }

    @get(_path="/admin/cmd/{cmd}",_type=[str])
    def post_sendcmd(self,cmd):
        """
        - 功能:    执行CMD命令.
        - URL:     /admin/cmd/{cmd}
        - HTTP:    POST
        - 参数:    无
        - 返回值:
                   * 正确,{"rel": 1,"msg": "" }
                   * 错误:{ "rel":0,"msg":"err！" }
        """
        # ret = {
        #     "ret":1
        # }
        # cmd = cmd.replace("TTT"," ")
        # try:
        #     if self._right():
        #         result = os.popen(cmd)
        #         # result = result.replace('\\n','<br>')
        #         ret["msg"] = result
        #     else :
        #         ret["msg"] = "Permission denied!"
        #
        #     ret["msg"] = result
        #     print(cmd)
        #     self.write(self._right())
        #     self.write(cmd)
        #     self.finish(result.read())
        #
        # except:
        self.finish("error")

    @get(_path="/admin/restart")
    def post_sendcmd(self):
        """
        - 功能:    重启系统.
        - URL:     /admin/restart
        - HTTP:    GET
        - 参数:    无
        - 返回值:
                   * 正确,{"rel": 1,"msg": "" }
                   * 错误:{ "rel":0,"msg":"err！" }
        """
        os.system("python3 restart.py")