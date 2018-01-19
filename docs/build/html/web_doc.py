import os
import tornado.ioloop
import pyrestful.rest

from pyrestful.rest import get, post, put, delete





class Application(pyrestful.rest.RestService):
    def __init__(self):
        settings= dict(
            # template_path=os.path.join(os.path.dirname(__file__), ""),
            static_path=os.path.join(os.path.dirname(__file__), "_static"),
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
