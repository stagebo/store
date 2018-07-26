
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
from service import user_service
from service.test_service import TestService
from base import r
class TestHandler(pyrestful.rest.RestHandler):
    tservice = TestService()
    @post(_path="/test/addtest")
    def add_test(self):
        params = r.POST_ARGS(self,['id','name'])
        if not params['id']:
            self.finish( r.ERR('id 不能为空!'))
            return
        if not params['name']:
            self.finish(r.ERR('name 不能为空！'))
            return
        ret,msg = self.tservice.add_test(params)
        if not ret:
            self.write(json.dumps(r.ERR(str(msg))))
            return
        self.finish(r.OK())


    @get(_path="/user/list")
    def get_user_list(self):
        us = user_service.UserService()
        users = us.get_user_list()
        self.finish(json.dumps(users))

    @get(_path="/user/get/{id}")
    def get_user_by_id(self,id):
        user = user_service.UserService().get_user_by_id(id)
        self.finish(json.dumps(user))
