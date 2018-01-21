#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:         common.py
#
# Purpose:      创建表的增删改查公共方法。
#
# Author:       Wan YongBo
#
# Created:      2018-1-18 9:17:46
#----------------------------------------------------------------------------
import sys
import os
import argparse
import psycopg2
import codecs
import datetime
import pymysql
import configparser
sys.path.append("..")
from database import dbHelper

cf = configparser.ConfigParser()
try:
    cf.read("../web.conf")
except:
    print("read config error.")
    sys.exit(1)
mysql_host = cf.get("mysql", "host")
mysql_uid = cf.get("mysql", "uid")
mysql_pwd = cf.get("mysql", "pwd")
mysql_db = cf.get("mysql", "db")
mysql_port = cf.getint("mysql", "port")
web_port = cf.getint("web", "port")

db = dbHelper.DbHelper(mysql_host,mysql_uid,mysql_pwd,mysql_port,mysql_db)
conn = db.conn
cursor = db.cursor
def copy_source_bak():
    os.system("copy common.py common_%s_bak.py"%datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))

def rm_prex(strs):
    return strs[strs.find("_")+1:]

def create_query_method(tablename,apis):
    table = rm_prex(tablename)

    apis.append("Query_%s"%table)
    method_str = '''
    def Query_%s(self, handler):
        """
             - 功能:    查询所有%s信息.

        """
        refdata,bauth =  self.select_all(handler,"%s")
        return refdata,bauth'''%(table,table,tablename)


    return method_str

def create_insert_method(tablename,apis):
    table = rm_prex(tablename)
    cursor.execute("select * from %s where f_name <> 'f_id'"%(tablename+"_exp"))
    table_info = cursor.fetchall()
    for info in table_info:
        print(info)

    apis.append("Insert_%s" % table)
    method_str = '''   
    def Insert_%s(self,handler):
        """
             - 功能:    添加%s
             - URL:     /版本号/insert_%s
             - HTTP:    POST
             - 参数:'''%(table,table,table)

    for info in table_info:
        field_name = info[0]
        field_cname = info[1]
        field_showtype = info[5]

        method_str += '''
                    * %s            %s              %s'''%(rm_prex(field_name),field_showtype,field_cname)


    method_str += '''
             - 返回值:
                    * 正确,返回结果.
                    * 错误:
                         * 正确返回:{"result":"0","msg":""}
                         * 错误:{"result":"-1","msg":"错误消息内容"}

        """
    '''
    method_str += '''
        tablename = "%s"
        try:
            res = handler.request.body.decode("utf-8")
            objs = json.loads(res)'''%tablename
    for info in table_info:
        field_name = info[0]
        field_cname = info[1]
        field_showtype = info[5]
        method_str += '''
            %s = objs.get("%s",None)'''%(field_name,rm_prex(field_name))
    method_str += '''
        except:
            return self._errmsg("接收参数失败！"),False '''

    for info in table_info:
        field_name = info[0]
        field_cname = info[1]
        field_showtype = info[5]
        field_null = info[14]
        if int(field_null) == 0:
            method_str += '''
        if not %s :
            return   self._errmsg("%s不能为空！"),False '''%(field_name,rm_prex(field_name))

    method_str += '''
        sql = "insert into %s ('''%tablename
    is_start = True
    for info in table_info:
        if not is_start:
            method_str += ','
        is_start = False
        field_name = info[0]
        method_str += field_name;
    method_str += ') values ('

    is_start = True
    for info in table_info:
        if not is_start:
            method_str += ','
        is_start = False
        method_str += '\'%s\''
    method_str += ')"%('

    is_start = True
    for info in table_info:
        if not is_start:
            method_str += ','
        is_start = False
        field_name = info[0]
        method_str += field_name
    method_str += ''')
        rel = self.dbhelper.db.execute(sql)
        if not rel:
            return self._errmsg("插入数据失败！"), False
        return [{"result":"0","msg":""}], True 
    '''




    return method_str

def create_update_method(tablename,apis):
    table = rm_prex(tablename)
    cursor.execute("select * from %s_exp "%tablename)
    table_info = cursor.fetchall()
    for info in table_info:
        print(info)

    apis.append("Update_%s" % table)
    method_str = '''
    def Update_%s(self,handler):
        """
             - 功能:    添加%s
             - URL:     /版本号/update_%s
             - HTTP:    POST
             - 参数:'''%(table,table,table)

    for info in table_info:
        field_name = info[0]
        field_cname = info[1]
        field_showtype = info[5]

        method_str += '''
                    * %s            %s              %s'''%(rm_prex(field_name),field_showtype,field_cname)


    method_str += '''
             - 返回值:
                    * 正确,返回结果.
                    * 错误:
                         * 正确返回:{"result":"0","msg":""}
                         * 错误:{"result":"-1","msg":"错误消息内容"}

        """
    '''
    method_str += '''
        tablename = "%s"
        try:
            res = handler.request.body.decode("utf-8")
            objs = json.loads(res)'''%tablename
    for info in table_info:
        field_name = info[0]
        field_cname = info[1]
        field_showtype = info[5]
        method_str += '''
            %s = objs.get("%s",None)'''%(field_name,rm_prex(field_name))
    method_str += '''
        except:
            return self._errmsg("接收参数失败！"),False '''

    for info in table_info:
        field_name = info[0]
        field_cname = info[1]
        field_showtype = info[5]
        field_null = info[14]
        if int(field_null) == 0:
            method_str += '''
        if not %s :
            return   self._errmsg("%s不能为空！"),False '''%(field_name,rm_prex(field_name))

    method_str += '''
        sql = "update %s set '''%tablename
    is_start = True
    for info in table_info:
        if not is_start:
            method_str += ','
        is_start = False
        field_name = info[0]
        field_cname = info[1]
        field_showtype = info[5]
        field_null = info[14]
        method_str += field_name+" = '%s'"
    method_str += " where f_id = '%s';\"%("


    for info in table_info:

        is_start = False
        field_name = info[0]
        field_cname = info[1]
        field_showtype = info[5]
        field_null = info[14]
        method_str += field_name
        method_str += ','
    method_str += "f_id)"
    method_str += '''
        rel = self.dbhelper.db.execute(sql)
        if not rel:
            return self._errmsg("更新数据失败！"), False
        return [{"result":"0","msg":""}], True 
    '''




    return method_str

def create_delete_method(tablename,apis):
    table = rm_prex(tablename)
    cursor.execute("select * from %s_exp "%tablename)
    table_info = cursor.fetchall()
    for info in table_info:
        print(info)

    apis.append("Delete_%s" % table)
    method_str = '''
    def Delete_%s(self,handler):
        """
             - 功能:    删除%s
             - URL:     /版本号/delete_%s
             - HTTP:    POST
             - 参数:'''%(table,table,table)

    info = table_info[0]
    field_name = info[0]
    field_cname = info[1]
    field_showtype = info[5]
    fileld_param_name = (table+field_name).replace('_','')
    method_str += '''
                    * %s            %s              %s'''%(fileld_param_name,field_showtype,field_cname)


    method_str += '''
             - 返回值:
                    * 正确,返回结果.
                    * 错误:
                         * 正确返回:{"result":"0","msg":""}
                         * 错误:{"result":"-1","msg":"错误消息内容"}

        """
    '''
    method_str += '''
        tablename = "%s"
        try:
            res = handler.request.body.decode("utf-8")
            objs = json.loads(res)
            f_id = objs.get("%s",None)'''%(tablename,fileld_param_name)

    method_str += '''
        except:
            return self._errmsg("接收参数失败！"),False '''
    method_str += '''
        sql = "delete from %s where %s = '''%(tablename,field_name)
    method_str += "'%s'"
    method_str += '"%' + field_name
    method_str += '''
        rel = self.dbhelper.db.execute(sql)
        if not rel:
            return self._errmsg("删除数据失败！"), False
        return [{"result":"0","msg":""}], True 
    '''




    return method_str

def write_append(file,strs):
    f = codecs.open(file,"a",'utf-8')
    f.write(strs)

def get_method(tiduq_list,tq_list):
    methods = []
    apis = []
    for table in table_q_list:
        method_str = create_query_method(table, apis)
        methods.append(method_str)

    for table in table_iduq_list:
        method_str = create_query_method(table, apis)
        methods.append(method_str)

    for table in table_iduq_list:
        method_str = create_insert_method(table,apis)
        methods.append(method_str)

    for table in table_iduq_list:
        method_str = create_update_method(table,apis)
        methods.append(method_str)

    for table in table_iduq_list:
        method_str = create_delete_method(table,apis)
        methods.append(method_str)

    return methods,apis

def write_file(methods,apis,file):
    header = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:         common.py
# Purpose:
#
# Author:       Create By Script 'create_function.py'
#
# Created:      %s
#----------------------------------------------------------------------------
import time
import psycopg2
from datetime import datetime
from tornado import gen
import tornado
import json
import traceback    
    '''%datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file.write(header)


    function_header = '''

class functions():
    def _errmsg(self,str):
        return {
            "result":"-1",
            "msg":str
        }
    #权限判断函数，加_前缀的是内部函数
    def _right(self,operatorID):
        return True

    def __init__(self, dbhelper):
        self.dbhelper = dbhelper

    def __test__(self, xmid):
        self._m8(xmid)
        self._m9(xmid)

    
    def _execute(self,sql):
       refdata = []
       try:
            cursor = yield self.dbhelper.execute(sql)
            refdata = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
       except psycopg2.Error as e:
             #打印错误，会打印到日志中。
             print(e)
             #抛出异常，系统管理员可得到通知
             raise
             return []

       return refdata

    
    def select_all(self,handler,tablename):
        right = self._right(handler.operatorid)
        if right is False:
            return [], False

        refdata  = yield self._execute("select * from %s" % tablename)
        return  refdata,True

    '''
    file.write(function_header)

    for method in methods:
        file.write(method)

if __name__ == "__main__":
    # 要做增删改查的表
    table_iduq_list = [      "t_jieba"            ]
    #只做查询的表
    table_q_list = [                   ]
    # 目标文件
    file = codecs.open("common.py","w",'utf-8')

    # 获取api和方法体
    methods,apis = get_method(table_iduq_list,table_q_list)

    # 写入文件
    write_file(methods,apis,file)

    #
    # copy_source_bak()