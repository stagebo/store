import pymysql
import sys
import traceback


from tornado.options import define,options

define("port", default=8888, help="run on the given port", type=int)
define("mysql_host", default="39.106.157.61", help="blog database host")
define("mysql_port", default="3306", help="blog database port",type=int)
define("mysql_database", default="stagebo", help="blog database name")
define("mysql_user", default="root", help="blog database user")
define("mysql_password", default="", help="blog database password")


class DbHelper():
    def __init__(self,dbhost,dbuid,dbpwd,dbport,dbname):
        dbconfig = {
            'host': dbhost,
            'port': dbport,
            'user': dbuid,
            'password': dbpwd,
            'db': dbname,
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor,
        }
        try:
            self.conn = pymysql.connect(**dbconfig)
            self.cursor = self.conn.cursor()
            print("connect success")
        except:
            print("connect error")
            traceback.print_exc()


    def execute_sql(self,sql):
        if not sql and sql=="":
            return None
        try:
            self.cursor.execute(sql)
            return None
        except:
            traceback.print_exc()
            return None

    def fetch_one(self,sql):
        if not sql and sql=="":
            return None
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            return data
        except:
            traceback.print_exc()
            return None

    def fetch_all(self, sql):
        if not sql and sql == "":
            return None
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data
        except:
            traceback.print_exc()
            return None
if __name__ == "__main__":
    db=DbHelper(
        dbhost=options.mysql_host,
        dbport=3306,
        dbuid=options.mysql_user,
        dbname=options.mysql_database,
        dbpwd=options.mysql_password
    )



    data = db.fetch_all("select * from t_test")
    print(data)

