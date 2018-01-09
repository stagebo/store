
import tornado.web
import pyrestful.rest


from pyrestful.rest import get, post, put, delete
from pyrestful import mediatypes


class Book(object):
    isbn = int
    title = str

class JiebaHandler(pyrestful.rest.RestHandler):

    @get(_path="/jieba")
    def getpage(self):
        self.render("templates/jieba/index.html")


