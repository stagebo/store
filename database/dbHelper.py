import pymysql
import sys
import traceback

class DbHelper():
    def __init__(self):
        self.conn=None
        self.cursor=None

    def open(self,dbhost,dbuid,dbpwd,dbport,dbname):
        try:
            self.conn = pymysql.connect(
                host=dbhost,
                port=dbport,
                user=dbuid,
                password=dbpwd,
                db=dbname,
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.conn.cursor()
            return True
        except:
            traceback.print_exc()
            return False

    def execute_sql(self,sql):
        if not sql and sql=="":
            return False
        try:
            self.cursor.execute(sql)
            return True
        except:
            traceback.print_exc()
            return False

    def fetch_one(self,sql):
        if not sql and sql=="":
            return None
        try:
            self.cursor.execute(sql)
            data = self.conn.fetchone()
            return data
        except:
            traceback.print_exc()
            return None