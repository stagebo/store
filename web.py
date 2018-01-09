import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web



from tornado.options import define, options

from handler_jieba import JiebaHandler

define("port", default=8888, help="run on the given port", type=int)


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/jieba", JiebaHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()