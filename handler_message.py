
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
import uuid
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
        email = self.get_body_argument("email", None)
        ip = self.request.remote_ip
        id = uuid.uuid1()
        rootid = "None"
        pid = "None"
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        userid = "None"
        usertype="-1"


        if not nickname or nickname == "":
            nickname = "匿名游客"
        if not message or message == "":
            return self.err("留言内容不能为空！");
        if not email or email == "":
            email = "example@qq.com"

        searcher = gl.gl_ip_searcher
        if ip == "::1":
            data = {'city': 127, "region": u"本地"}
            city = data["region"]
        else:
            data = searcher.btreeSearch(ip)
            city = data["region"].decode('utf-8')

        sql = """
        insert into t_comment
        (f_id,f_root_id,f_pid,f_time,f_user_id,f_user_type,f_nickname,f_content,f_ip,f_city,f_email) 
        values
        ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')
        
        """%(id,rootid,pid,time,userid,usertype,nickname,message,ip,city,email)
        print(sql)
        rel = self.application.db.execute_sql(sql)
        if not rel:
            logging.error("insert failed,sql:%s" % sql)
            return self.err("留言失败！");

        return {
            'ret': 1,
            'msg':'',
            'data':''
        }

    @tornado.web.asynchronous
    @tornado.gen.engine
    @get(_path="/message/search_message")
    def get_message(self):
        sql = 'select * from t_comment order by f_time desc'
        data = yield self.application.db.execute(sql)
        result = {
            'ret':1,
            'msg':'',
            'data':data
        }
        self.finish(result)