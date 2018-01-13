
import tornado.web
import pyrestful.rest
import json
import jieba

from pyrestful.rest import get, post, put, delete
from pyrestful import mediatypes


class DoctorHandler(pyrestful.rest.RestHandler):

    @get(_path="/doctor")
    def getpage(self):
        self.render("doctor/index.html")


