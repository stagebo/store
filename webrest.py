
import tornado.ioloop
import pyrestful.rest

from pyrestful import mediatypes
from pyrestful.rest import get, post, put, delete
from jieba_h import JiebaHandler


class UploadFileHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('''
                  <html>
                    <head><br>                      <title>Upload File</title><br>                    </head>
                    <body>
                      <form action='file' enctype="multipart/form-data" method='post'>
                        <input type='file' name='file'/><br/>
                        <input type='submit' value='submit'/>
                      </form>
                    </body>
                  </html>
                  ''')
if __name__ == '__main__':
    try:
        print("Start the service")
        app = pyrestful.rest.RestService([
            JiebaHandler,

        ])
        app.listen(8080)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("\nStop the service")