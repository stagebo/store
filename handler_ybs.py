
import tornado.web
import pyrestful.rest
import json
import jieba
import gl
import hashlib
import time
from pyrestful.rest import get, post, put, delete
from pyrestful import mediatypes


class DoctorHandler(pyrestful.rest.RestHandler):

    @get(_path="/doctor")
    def getpage(self):
        self.render("doctor/index.html")

    @get(_path="/doctor/login",_produces=mediatypes.APPLICATION_JSON)
    def login_ybs(self):
        session = gl.gl_session
        login_url = 'http://api.yiboshi.com/api/study/student/login'
        username = self.get_argument("username", '')
        password = self.get_argument("password", '')

        obj = hashlib.md5()  # 创建md5加密对象
        obj.update(bytes(password, encoding="utf-8"))
        key = obj.hexdigest()  # 获取加密后的密串

        user = {'password':key, 'username': username  }
        result = session.post(login_url, data=user)
        return result.json()

    @get(_path="/doctor/auth",_produces=mediatypes.APPLICATION_JSON)
    def auth_info(self):
        session = gl.gl_session
        auth_url = 'http://api.yiboshi.com/api/study/student/authJWT'
        token = self.get_argument("token", '')
        # TODO 小心浅拷贝
        headers = gl.headers.copy()
        headers["Authorization"]='Bearer '+token
        result = session.post(auth_url,data=None,headers=headers)

        return result.json()
