from tornado_mysql import pools
import configparser
from tornado import  gen
import json
from tornado import ioloop
import logging


class SyncDb():
    def __init__(self,mysql_host, mysql_port, mysql_uid, mysql_pwd,mysql_db):

        self.db = pools.Pool(
            dict(host=mysql_host, port=mysql_port, user=mysql_uid, passwd=mysql_pwd,db=mysql_db, charset='utf8mb4'),
            max_idle_connections=3,
            max_open_connections=20,
            max_recycle_sec=3)

    @gen.coroutine
    def execute(self,sql):
        cur = yield self.db.execute(sql)
        # for row in cur.fetchall():
        #     print(row)
        #     for i,v in enumerate(row):
        #         print(i,v)
        reldata = [dict((cur.description[i][0],str(v)) for i, v in enumerate(row)) for row in cur.fetchall()]
        return reldata

    @gen.coroutine
    def execute_sql(self,sql):
        if sql == "":
            return False
        try:
            cur = yield self.db.execute(sql)
            return True
        except Exception as e:
            print(e)
            logging.error(e)
            return False

@gen.coroutine
def main():
    rel = yield sdb.execute("select * from t_jieba")
    print(rel)

if __name__ == "__main__":
    cf = configparser.ConfigParser()

    cf.read("../web.conf")
    mysql_host = cf.get("mysql", "host")
    mysql_uid = cf.get("mysql", "uid")
    mysql_pwd = cf.get("mysql", "pwd")
    mysql_db = cf.get("mysql", "db")
    mysql_port = cf.getint("mysql", "port")

    print((mysql_host,mysql_port,mysql_uid,mysql_pwd,mysql_db))

    sdb = SyncDb(mysql_host, mysql_port, mysql_uid, mysql_pwd, mysql_db)

    ioloop.IOLoop.current().run_sync(main)
    print(123)


