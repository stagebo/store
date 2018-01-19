import pymysql
import sys
import traceback

database = None

class DbHelper():
    """ 数据库工具函数.

            构造函数::

                    - dbhost: host name
                    - param dbuid: database user name
                    - param dbpwd: database password
                    - param dbport: database port
                    - param dbname: database name

        """
    """
    数据库工具函数.
    arguments:
    :param dbhost: host name
    :param dbuid: database user name
    :param dbpwd: database password
    :param dbport: database port
    :param dbname: database name

       """
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
        """
             - 功能:    执行sql
             - 参数:    sql       string
             - 返回值:
                        * 正确,True.
                        * 错误:False
             - 异常: mysql Error

        """
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
        """
             - 功能:    查询一条结果
             - 参数:    sql       string
             - 返回值:
                        * 正确,(data set).
                        * 错误:None
             - 异常: mysql Error

        """
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
        """
             - 功能:    查询所有结果
             - 参数:    sql       string
             - 返回值:
                        * 正确,[data set list].
                        * 错误:None
             - 异常: mysql Error

        """
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




