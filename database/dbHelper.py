import pymysql
import sys
import traceback

database = None

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
            return False
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            traceback.print_exc()
            return False

    def fetch_one(self,sql):
        if not sql and sql=="":
            return None
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            return data
        except:
            self.conn.rollback()
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
            self.conn.rollback()
            traceback.print_exc()
            return None
if __name__ == "__main__":
    pass




