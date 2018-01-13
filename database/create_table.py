from dbHelper import DbHelper
import configparser
if __name__ == "__main__":
    cf = configparser.ConfigParser()
    cf.read("../webrest.conf")
    mysql_host = cf.get("mysql", "host")
    mysql_uid = cf.get("mysql", "uid")
    mysql_pwd = cf.get("mysql", "pwd")
    mysql_db = cf.get("mysql", "db")
    mysql_port = cf.getint("mysql", "port")
    web_port = cf.getint("web", "port")
    db = DbHelper(mysql_host,mysql_uid,mysql_pwd,mysql_port,mysql_db)

    sql = '''
    DROP TABLE IF EXISTS t_jieba;
    CREATE TABLE t_jieba (
      f_time datetime NOT NULL,
      f_content text NOT NULL
    )
    '''
    print(sql)
    d = db.execute_sql(sql)
    print(d)

