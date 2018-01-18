
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

class JiebaHandler(pyrestful.rest.RestHandler):
    @get(_path="/jieba")
    def getpage(self):
        self.render("jieba/index.html")


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
            self.render("jieba/index.html")
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

        sql = "insert into t_jieba values('%s','%s','%s','%s')"%(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    cont,
                    ip,
                    city
                )

        if not dbHelper.database.execute_sql(sql):
            print("err")
            logging.warning("insert failed,sql:%s"%sql)

        seg_list = jieba.cut(cont, cut_all=False)
        data = "/".join(seg_list)

        self.write(json.dumps({
            "ret": "1",
            "msg": "",
            "data": data
            }))

    @get(_path="/jieba/gethistory",_produces=mediatypes.APPLICATION_JSON)
    def get_history(self):
        try:
            data = dbHelper.database.fetch_all("select * from t_jieba order by f_time desc")
            json_data = []

            dbFile = 'ip2region/data/ip2region.db'
            searcher = ip2region.ip2Region.Ip2Region(dbFile)
            for item in data:
                if not item["f_city"]:
                    ip = item["f_ip"]
                    if ip == "::1":
                        data = {'city': 127, "region": u"本地"}
                        city = data["region"]
                    else:
                        data = searcher.btreeSearch(ip)
                        city = data["region"].decode('utf-8')
                    print(city)
                    sql = "update t_jieba set f_city = '%s' where f_ip = '%s'"%(city,ip)
                    print(sql)
                    dbHelper.database.execute_sql(sql)

                json_data.append({
                    "time":str(item["f_time"]),
                    "cont":item['f_content'],
                    "ip":item["f_city"]
                })
            return {
                "ret": "1",
                "msg": "",
                "data": json.dumps(json_data)
                }
        except :
            traceback.print_exc()
            logging.error("some err occur in search jiebahistory.")
            return {
                "ret":0,
                "msg":"some error occur in search jieba history."
            }