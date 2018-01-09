
import tornado.web
import pyrestful.rest
import json
import jieba

from pyrestful.rest import get, post, put, delete
from pyrestful import mediatypes



class JiebaHandler(pyrestful.rest.RestHandler):

    @get(_path="/jieba")
    def getpage(self):
        self.render("templates/jieba/index.html")


    @get(_path="/jieba/split")
    def post_data(self):
        # self.write("123")
        err = json.dumps({
                "ret": "0",
                "msg": "数据结构错误",
            })
        cont = self.get_query_argument("cont")
        if not cont or cont == "":
            self.render("templates/jieba/index.html")
            self.write(err)
        seg_list = jieba.cut(cont, cut_all=True)
        data = "/".join(seg_list)

        self.write(json.dumps({
            "ret": "1",
            "msg": "",
            "data": data
            }))
