
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


class AdminHandler(pyrestful.rest.RestHandler):

    @get(_path="/admin")
    def getpage(self):
        self.render("admin/index.html")

