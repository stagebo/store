import os
import tornado.ioloop
import pyrestful.rest
import logging
import pymysql
import configparser
import sys
import datetime
import json
import platform
import traceback
from pyrestful import mediatypes
from pyrestful.rest import get, post, put, delete
from handler_jieba import JiebaHandler
from handler_ybs import DoctorHandler
from handler_admin import AdminHandler
from handler_chatbot import ChatbotHandler
from handler_foru import ForuHandler
from tornado.log import access_log, app_log, gen_log
from tornado.options import define,options
sys.path.append("..")
from database import dbHelper


class Application(pyrestful.rest.RestService):
    def __init__(self):

        settings= dict(
            #cookie_secret="SBwKSjz3SCWo04t68f/FOY7fPKZI20JYje1IYPBrxaM=",
            template_path=os.path.join(os.path.dirname(__file__), "docs/build/html"),
            static_path=os.path.join(os.path.dirname(__file__), "docs/build/html"),
            xsrf_cookies=False,
            debug = False,
            # login_url = "admin/login",
            # log_function = self.mylog
        )
        handlers=[
            MainHadler
        ]
        super(Application, self).__init__(handlers, **settings)



#
class MainHadler(pyrestful.rest.RestHandler):

    @get(_path="/")
    def main_doc(self):
        self.render("index.html")



def main():

    try:
        print("Start the service")
        app = Application()
        app.listen(7001)
        print("access port %s" % 7001)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("\nStop the service")

if __name__ == '__main__':
    main()
