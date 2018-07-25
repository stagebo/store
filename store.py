import os
import tornado.ioloop
import pyrestful.rest
import logging
import configparser
import sys
import datetime
import platform
import traceback
from pyrestful import mediatypes
from pyrestful.rest import get
from controller.user_controller import AdminHandler
from tornado.log import access_log

sys.path.append("..")
from database import redisdb,syncdb



class Application(pyrestful.rest.RestService):
    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.read_config()
        # 内存数据库
        self.redis = redisdb.RedisDb()

        logging.info("tornado is tring to init...")
        settings= dict(
            #cookie_secret="SBwKSjz3SCWo04t68f/FOY7fPKZI20JYje1IYPBrxaM=",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            debug = False,
            # ui_methods=uimethod, #'
            # ui_modules=uimodule,
            login_url = "admin/login",
            log_function = self.mylog
        )
        handlers=[
            MainHadler,
            AdminHandler,
        ]
        super(Application, self).__init__(handlers, **settings)
        self.db = syncdb.SyncDb(self.mysql_host, self.mysql_port, self.mysql_uid, self.mysql_pwd, self.mysql_db)
        logging.info("tornado is inited.")

    def read_config(self):

        try:
            self.cf.read("store.conf")
        except:
            logging.error("not find a config file named webrest.conf")
            sys.exit(1)
        self.mysql_host = self.cf.get("mysql", "host")
        self.mysql_uid = self.cf.get("mysql", "uid")
        self.mysql_pwd = self.cf.get("mysql", "pwd")
        self.mysql_db = self.cf.get("mysql", "db")
        self.mysql_port = self.cf.getint("mysql", "port")
        self.web_port = self.cf.getint("web", "port")
        print(self.mysql_host,self.mysql_uid,self.mysql_port,self.mysql_pwd,self.mysql_db)

    def mylog(self,handler):
        if handler.get_status() < 400:
            log_method = access_log.info
        elif handler.get_status() < 500:
            log_method = access_log.warning
        else :
            print('服务器异常！')
            log_method = access_log.error

        request_time = 1000.0 * handler.request.request_time()
        print("%d %s %.2fms"%(handler.get_status(), handler._request_summary(), request_time))
        log_method("%d %s %.2fms", handler.get_status(),handler._request_summary(), request_time)

#
class MainHadler(pyrestful.rest.RestHandler):
    @get(_path="/")
    def index(self):
        self.render("base.html")

    @get(_path="/main/test")
    def test(self):
        self.finish('main test')

    @get(_path="/main/restart")
    def restart(self):
        os.system("python3 restart.py")



def copy_log():
    logpath = os.path.join("..", "log")
    logfile =os.path.join(logpath,"pyweb.log") # "..\log\pyweb.log"
    logbak = os.path.join(logpath,"%s.log"%datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    cmd = ""
    print("init log file.")
    print("platform info:%s" % platform.platform())
    print( os.path.exists(logfile))
    if not os.path.exists(logfile):
        print("create log files.")
        os.makedirs(logpath)
        open(logfile, "w")
    elif "Windows" in platform.platform():
        try:
            cmd = "copy %s %s" % (logfile,logbak)
        except:
            traceback.print_exc()
    elif "Linux" in platform.platform():
        cmd = "cp %s %s" % (logfile,logbak)
    if cmd != "":
        p = os.popen(cmd)
        print(cmd)
        print(p)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=logfile,
                        filemode='w')

def main():
    '''

    :return:
    '''
    # copy_log()
    try:
        print("Start the service")
        app = Application()
        app.listen(app.web_port)
        print("access port %s" % app.web_port)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("\nStop the service")

if __name__ == '__main__':
    main()
