
import tornado.ioloop
import pyrestful.rest

from pyrestful import mediatypes
from pyrestful.rest import get, post, put, delete
from jieba_h import JiebaHandler

class Application():
    def create(self):
        settings={}
        app = pyrestful.rest.RestService([
            JiebaHandler
           ,StaticHandler
        ])

        return app
class StaticHandler(pyrestful.rest.RestHandler):

    @get(_path="/static/plugins/{plugin}/{file}")
    def getresource(self, plugin, file):
        self.render("static/plugins/%s/%s"%(plugin, file))

if __name__ == '__main__':
    try:
        print("Start the service")
        app = Application().create()
        app.listen(8888)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("\nStop the service")