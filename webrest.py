import os
import tornado.ioloop
import pyrestful.rest

import pymysql

from pyrestful import mediatypes
from pyrestful.rest import get, post, put, delete
from handler_jieba import JiebaHandler
from handler_ybs import DoctorHandler
from tornado.log import access_log, app_log, gen_log
from tornado.options import define,options


class Application(pyrestful.rest.RestService):
    def __init__(self):
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
        #     host=options.mysql_host,
        #     user=options.mysql_user,
        #     password=options.mysql_password,
        #     db=options.mysql_database,
        #     charset='utf8mb4',
        #     cursorclass=pymysql.cursors.DictCursor
        # )




    def mylog(self,handler):
        if handler.__class__.__name__ == "GetServerInfo" or handler.__class__.__name__ == "GetServerMonitor":
            return
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

if __name__ == '__main__':
    try:
        print("Start the service")
        app = Application()
        app.listen(8888)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("\nStop the service")