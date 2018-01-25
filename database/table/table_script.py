import os
import sys
import psycopg2
import configparser
import traceback
import time
import platform
import threading
import datetime
import getopt
import json
import csv
from random import random

isLinux = True;
if (platform.system() == 'Linux'):
    isLinux = True
else:
    isLinux = False

aliyun = True

import_yun = False

jump_import = False
jump_dump = False
# csv
opts, args = getopt.getopt(sys.argv[1:], "lyid", ['local', 'yun', 'import', 'dump'])
for op, value in opts:
    if op in ("-y", "--yun"):
        import_yun = True
    if op in ("-l", "--local"):
        aliyun = False
    if op in ("-i", "--import"):
        jump_import = True
    if op in ("-d", "--dump"):
        jump_dump = True
# 服务器
# server_ip = '192.168.1.100'
if aliyun:
    server_ip = ''
    g_db = 'pmg3'
else:
    server_ip = '127.0.0.1'
    g_db = 'piot'


# 需要保留数据的表
export_tables = ['ts_user']


def _round(a, b=None):
    return round(a, 5)


sql_database = ''
sql_user = 'postgres'
sql_password = ''
sql_host = '127.0.0.1'
sqL_port = 5432

path = ""
keyword = "exp.csv"


# path=cf.get("folder","path")
# keyword=cf.get("folder","keyword")

conn = psycopg2.connect(database=sql_database, user=sql_user, password=sql_password, host=sql_host, port=sqL_port)
cursor = conn.cursor();
print('connect successful!')

tables = []

# 定义表结构常量
global_field_name = 0
global_field_cname = 1
global_field_type = 2
global_field_length = 3
global_field_dec = 4
global_field_pkey = 8
global_unique = {
    't_ygxxcx': ['f_xm', 'f_userid'],
}
# 导入成功文件数， 文件数
sucess_add_main_num = 0
sucess_add_num = 0

# 生成sql文件
dump_cmd = 'pg_dump -U %s -h %s -p %s --role "postgres" --no-password  --format tar --encoding UTF8 --no-privileges --no-tablespaces --verbose --no-unlogged-table-data --file "sql\pmg.backup" ' % (
sql_user, sql_host, sqL_port)
dump_tables = []

sql_serial_update = ''


# 预处理，保留部分数据
def pre_handler(path):
    path = path.replace("\\", "/")
    path = path + "/"
    # for s in export_tables:
    #     cmd = export_cmd + '"COPY (select * from ' + s + ') to stdout with csv header encoding \'GBK\'" >' + path + s + '.csv'
    #     os.system(cmd)


# 关键字查询文件路径
def search(path, word):
    for filename in os.listdir(path):
        fp = os.path.join(path, filename)
        global sucess_add_num
        try:
            if (os.path.isfile(fp)) and word in filename:
                writeCSV(fp, filename)
                # 导入说明表成功计数
                sucess_add_num += 1
        except:
            traceback.print_exc()
            print("导入失败: " + filename)
            exit()


# 写入sql并执行
def sql_execute(sql):
    # 写入sql
    # open_sql.write(sql+';\n\n')
    try:
        print(sql)
        cursor.execute(sql)
        conn.commit()
    except:
        traceback.print_exc()



# 导入csv
def import_csv(path, tablename):
    path = path.replace('\\', '/')
    csvr = csv.reader(open(path))
    sql = "insert into " + tablename + " values"
    isStart = True
    idx = 1
    for row in csvr:
        if idx == 1:
            idx = 0
            continue
        if isStart:
            isStart = False
        else:
            sql += ","
        sql += "("
        isSStart = True
        for field in row:
            if isSStart:
                isSStart = False
            else:
                sql += ","
            sql += "'%s'" % field
        sql += ")"
    print(sql)
    sql_execute(sql)

    # sql = 'copy '+tablename+' from \''+path+''''
    #     with(
    #     FORMAt csv,
    #     DELIMITER ',',
    #     header true,
    #     quote '"',
    #     encoding 'gbk')'''
    # print(sql)
    # sql_execute(sql)
    # dump_tables.append(tablename)
    # if '_exp' not in tablename:
    #     tables.append(tablename)
    # print('table '+tablename+' import completed!')


# 创建说明表并导入csv
def writeCSV(path, filename):
    # 如果存在删除旧表
    tablename = filename[:-4]
    if tablename[:-4].lower() in export_tables:
        return
    sql = 'drop table if exists ' + tablename
    sql_execute(sql)
    # 创建新表
    sql = 'create table ' + tablename + '''(
        f_name character varying(30),
        f_cname character varying(40),
        f_type character varying(1),
        f_length smallint,
        f_dec smallint,
        f_showtype character varying(20),
        f_unit character varying(10),
        f_beneed smallint,
        f_pkey smallint,
        f_groupindex smallint,
        f_groupname character varying(20),
        f_order integer,
        f_note text,
        f_readonly smallint,
        f_null smallint,
        CONSTRAINT ''' + tablename + '_pkey PRIMARY KEY (f_name))'
    sql_execute(sql)

    # print('table '+tablename+' is created!')
    # 导入数据
    import_csv(path, tablename)
    # 创建主表
    writeMain(path, tablename)


def writeMain(path, tablename_exp):
    tablename = tablename_exp[:-4]
    # 如果存在删除旧表
    sql = 'drop table if exists ' + tablename
    sql_execute(sql)
    # 查询说明表
    cursor.execute("select * from " + tablename_exp)
    rows = cursor.fetchall()
    sql = 'create table ' + tablename + '(\n'
    pkey = ''
    for row in rows:
        # 命令，名称转小写
        row_sql = '        ' + row[global_field_name].lower()
        # 判断类型
        if row[global_field_type] == 'C':
            if row[global_field_length] < 10000:
                row_sql += ' character varying(' + str(row[global_field_length]) + '),'
            else:
                row_sql += ' text,'
        elif row[global_field_type] == 'D':
            row_sql += ' date,'
        elif row[global_field_type] == 'T':
            row_sql += ' timestamp without time zone,'
        elif row[global_field_type] == 'N':
            if row[global_field_length] > 0 and row[global_field_length] < 3:
                row_sql += ' smallint,'
            elif row[global_field_length] == 0:
                row_sql += ' integer,'
            else:
                row_sql += ' double precision,'
        elif row[global_field_type] == 'S':
            row_sql += ' serial,'
            global sql_serial_update
            sql_serial_update += "select setval('{0}_{1}_seq',max({1})) from {0};\n".format(tablename,
                                                                                            row[global_field_name])
        else:
            print(row[global_field_type] + " : has no method")
            continue
        if tablename in global_unique:
            if row[global_field_name].lower() in global_unique[tablename]:
                row_sql = ' '.join([row_sql[:-1], 'UNIQUE,'])
        # 添加命令
        sql += row_sql + '\n'
        # 判断是否主键
        if row[global_field_pkey]:
            pkey = row[global_field_name]

    if pkey == '':
        sql = sql[:-2] + ');'
    else:
        sql += 'CONSTRAINT ' + tablename + '_pkey PRIMARY KEY (' + pkey + '));'

    for row in rows:
        sql += '\nCOMMENT ON COLUMN %s.%s IS \'%s\';' % (
        tablename, row[global_field_name].lower(), row[global_field_cname])

    sql_execute(sql)

    # print('table '+tablename+' is created!')

    path1 = path[:-8] + '.csv'
    path = os.path.join(os.path.dirname(path1), os.path.basename(path1))
    if os.path.isfile(path) or True:
        import_csv(path, tablename)
        # 导入主表成功计数
        global sucess_add_main_num
        sucess_add_main_num += 1

def add_tables_exp():
    sql = ''
    for table in tables:
        cursor.execute("select f_cname from t_tables where f_tablename='%s'" % table)
        re = cursor.fetchone()
        if re:
            sql += 'comment on table "%s" is \'%s\';\n' % (table, (re[0]))
            sql_execute(sql)

if __name__ == '__main__':
    path = "tableInfo"

    search(path, keyword)







    print("运行结束")