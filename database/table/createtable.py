import os
import sys
import pymysql
import configparser
import traceback
import time
import platform
import threading
import datetime
import getopt
import json
from random import random

import csv



def _round(a, b=None):
    return round(a, 5)


cf=configparser.ConfigParser()
cf.read("gmp.conf")

sql_database="pyweb"
sql_user='root'
sql_password='root'
sql_host='127.0.0.1'
sqL_port=3306

path='tableInfo'
keyword='exp.csv'


conn=pymysql.connect(database=sql_database,user=sql_user,password=sql_password,host=sql_host,port=sqL_port)
cursor=conn.cursor();

tables=['t_jieba']

#定义表结构常量
global_field_name = 0
global_field_cname = 1
global_field_type = 2
global_field_length = 3
global_field_dec = 4
global_field_pkey = 8
global_unique = {
    't_ygxxcx': ['f_xm', 'f_userid'],
}
#导入成功文件数， 文件数
sucess_add_main_num = 0
sucess_add_num = 0




#关键字查询文件路径
def search(path,word):
    for filename in os.listdir(path):
        fp = os.path.join(path,filename)
        global sucess_add_num
        try:
            if(os.path.isfile(fp)) and word in filename:
                writeCSV(fp, filename)   
                #导入说明表成功计数            
                sucess_add_num+=1
                
        except :
            traceback.print_exc() 
            print("导入失败: " + filename)
            exit()


#写入sql并执行
def sql_execute(sql):
    #写入sql
    #open_sql.write(sql+';\n\n')
    cursor.execute(sql)
    conn.commit()

#导入csv
def import_csv(path, tablename):
    csvr = csv.reader(open(path, encoding='utf-8', ))
    csvr_list = list(csvr)
    if len(csvr_list) < 2:
        print("%s do not have valid data" % path)
        return True

    sql ='insert into %s values '%tablename

    is_first = True
    t_start = True
    for row in csvr_list:
        if is_first:
            is_first=False
            continue
        if t_start:
            t_start = False
        else:
            sql += ','
        is_start = True
        sql += '('
        for field in row:
            if  is_start:
                is_start = False
            else:
                sql += ','
            sql += "'%s'"%field

        sql += ')'
    print(sql)
    sql_execute(sql)

    if '_exp' not in tablename:
        tables.append(tablename)
    print('table '+tablename+' import completed!')
     
#创建说明表并导入csv
def writeCSV(path, filename):
    #如果存在删除旧表
    tablename = filename[:-4]

    sql = 'drop table if exists '+tablename
    sql_execute(sql)
    #创建新表
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
    
    #print('table '+tablename+' is created!')
    #导入数据
    import_csv(path, tablename)   
    #创建主表
    writeMain(path, tablename)

def writeMain(path, tablename_exp):

    tablename = tablename_exp[:-4]
    if tablename in tables:
        return True
    #如果存在删除旧表
    sql='drop table if exists '+tablename
    sql_execute(sql)
    #查询说明表
    cursor.execute("select * from " +tablename_exp)
    rows=cursor.fetchall()
    sql = 'create table ' + tablename + '(\n'
    pkey = ''
    for row in rows:
        #命令，名称转小写
        row_sql='        '+row[global_field_name].lower()
        #判断类型
        if row[global_field_type] == 'C':
            if row[global_field_length]<10000:
                row_sql+=' nvarchar('+str(row[global_field_length])+'),'
            else:
                row_sql+=' text,'
        elif row[global_field_type] == 'D':
            row_sql+=' date,'
        elif row[global_field_type] == 'T':
            row_sql+=' datetime,'
        elif row[global_field_type] == 'N':
            if row[global_field_length] > 0  and row[global_field_length]<3 :
                row_sql+=' smallint,'
            elif row[global_field_length] == 0:
                row_sql+=' integer,'
            else:
                row_sql+=' double,'
        elif row[global_field_type] == 'S':
            row_sql+=' serial,'
            global sql_serial_update
            sql_serial_update +="select setval('{0}_{1}_seq',max({1})) from {0};\n".format(tablename, row[global_field_name])
        else:
            print(row[global_field_type]+" : has no method")
            continue

        #添加命令
        sql+=row_sql+'\n'
        #判断是否主键
        if row[global_field_pkey]:
            pkey = row[global_field_name]  
                      
    if pkey=='':
        sql=sql[:-2]+');'
    else:
        sql+='CONSTRAINT ' + tablename + '_pkey PRIMARY KEY (' + pkey + '));'
    #
    # for row in rows:
    #     sql+='\nCOMMENT ON COLUMN "%s"."%s" IS \'%s\';'%(tablename,row[global_field_name].lower(), row[global_field_cname] )

    sql_execute(sql)       
    
    #print('table '+tablename+' is created!')

    # path1 = path[:-8]+'.csv'
    # path = os.path.join(os.path.dirname(path1),os.path.basename(path1))
    # print(path)
    # if os.path.isfile(path):
    #     import_csv(path, tablename)
    #     #导入主表成功计数
    #     global sucess_add_main_num
    #     sucess_add_main_num+=1

def add_tables_exp():
    sql = ''
    for table in tables:
        cursor.execute("select f_cname from t_tables where f_tablename='%s'"%table)
        re = cursor.fetchone()
        if re:
            sql += 'comment on table "%s" is \'%s\';\n'%(table, (re[0]))
            sql_execute(sql)


if __name__=='__main__':
    search(path,keyword)
    # add_tables_exp()#添加表说明
