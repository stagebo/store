
import tornado.web
import pyrestful.rest
import json
import jieba
import sys
import datetime
sys.path.append("..")
from database import dbHelper
import logging
from pyrestful.rest import get, post, put, delete
from pyrestful import mediatypes
import traceback
import ip2region.ip2Region
from tornado import gen
class JiebaHandler(pyrestful.rest.RestHandler):
    @get(_path="/jieba")
    def getpage(self):
        self.render("jieba/index.html")

    @tornado.web.asynchronous
    @tornado.gen.engine
    @get(_path="/jieba/split")
    def post_data(self):
        # self.write("123")
        err = json.dumps({
                "ret": "0",
                "msg": "数据结构错误",
            })
        cont = self.get_query_argument("cont")
        ip = self.request.remote_ip
        if not cont or cont == "":
            self.write(err)

        # 定位IP
        dbFile = 'ip2region/data/ip2region.db'
        searcher = ip2region.ip2Region.Ip2Region(dbFile)
        method = 1
        if ip == "::1":
            data = {'city':127,"region":u"本地"}
            city = data["region"]
        else:
            data = searcher.btreeSearch(ip)
            city = data["region"].decode('utf-8')
        print(cont)
        sql = "insert into t_jieba values('%s','%s','%s','%s')"%(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    cont,
                    ip,
                    city
                )
        rel = self.application.db.execute_sql(sql)
        if not rel:
        # if not dbHelper.database.execute_sql(sql):
            print("err")
            logging.warning("insert failed,sql:%s"%sql)

        seg_list = jieba.cut(cont, cut_all=False)
        data = "/".join(seg_list)

        self.write(json.dumps({
            "ret": "1",
            "msg": "",
            "data": data
            }))

    @tornado.web.asynchronous
    @tornado.gen.engine
    # @gen.coroutine
    @get(_path="/jieba/gethistory")
    def get_history(self):
        try:
            sql = "select * from t_jieba order by f_time desc"
            sdb = self.application.db
            # data = yield tornado.gen.Task(sdb.execute, sql)
            data = yield sdb.execute(sql)
            print(data)
            # data = dbHelper.database.fetch_all("select * from t_jieba order by f_time desc")
            # data = dbHelper.database.execute(sql)
            ret = json.dumps(data)
            result =  {
                "ret": "1",
                "msg": "",
                "data": ret
                }
            self.finish(result)
        except Exception as e:
            traceback.print_exc()
            logging.error("some err occur in search jiebahistory.")
            logging.error(e)
            return {
                "ret":0,
                "msg":"some error occur in search jieba history."
            }