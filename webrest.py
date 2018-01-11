import os
import tornado.ioloop
import pyrestful.rest
import logging
import pymysql
import configparser
import sys

from pyrestful import mediatypes
from pyrestful.rest import get, post, put, delete
from handler_jieba import JiebaHandler
from handler_ybs import DoctorHandler
from tornado.log import access_log, app_log, gen_log
from tornado.options import define,options
sys.path.append("..")
from database import dbHelper
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='log/mylog.log',
                filemode='w')

class Application(pyrestful.rest.RestService):
    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.read_config()
        logging.info("tornado is tring to init...")
        settings= dict(
            #cookie_secret="SBwKSjz3SCWo04t68f/FOY7fPKZI20JYje1IYPBrxaM=",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            debug = False,
            #login_url = "/login",
            log_function = self.mylog
        )
        handlers=[
            MainHadler
           ,JiebaHandler
           ,DoctorHandler
           # ,StaticHandler
        ]
        super(Application, self).__init__(handlers, **settings)
        # self.db = pymysql.connect(
        #     host=self.mysql_host,
        #     user=self.mysql_uid,
        #     password=self.mysql_pwd,
        #     db=self.mysql_db,
        #     port=self.mysql_port,
        #     charset='utf8mb4',
        #     cursorclass=pymysql.cursors.DictCursor
        # )
        dbHelper.database=dbHelper.DbHelper(self.mysql_host,self.mysql_uid,self.mysql_pwd,self.mysql_port,self.mysql_db)

        logging.info("tornado is inited.")

    def read_config(self):

        try:
            self.cf.read("webrest.conf")
        except:
            logging.error("not find a config file named webrest.conf")
            sys.exit(1)
        self.mysql_host = self.cf.get("mysql", "host")
        self.mysql_uid = self.cf.get("mysql", "uid")
        self.mysql_pwd = self.cf.get("mysql", "pwd")
        self.mysql_db = self.cf.get("mysql", "db")
        self.mysql_port = self.cf.getint("mysql", "port")
        self.web_port = self.cf.getint("web", "port")

    def mylog(self,handler):
        if handler.get_status() < 400:
            log_method = access_log.info
        elif handler.get_status() < 500:
            log_method = access_log.warning
        else:
            log_method = access_log.error

        request_time = 1000.0 * handler.request.request_time()
        log_method("%d %s %.2fms", handler.get_status(),
                   handler._request_summary(), request_time)


# class StaticHandler(pyrestful.rest.RestHandler):
#     @get(_path="/static/plugins/{plugin}/{file}")
#     def getresource(self, plugin, file):
#         self.render("static/plugins/%s/%s"%(plugin, file))

class MainHadler(pyrestful.rest.RestHandler):
    @get(_path="/")
    def index(self):
        self.render("index.html")
    @get(_path="/main")
    def main_page(self):
        self.write("this is main page.")

    @get(_path="/about")
    def about_page(self):
        self.render("about.html")

if __name__ == '__main__':

    try:
        print("Start the service")
        app = Application()
        app.listen(app.web_port)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("\nStop the service")