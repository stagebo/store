#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    File Name:     test_dao
    Author:        Administrator
    Date:          2018/7/26
    Description:   
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃       ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃  永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
__author__ = 'Administrator'

from sqlalchemy import *
from sqlalchemy.orm import *
from dao.base_dao import BaseDao
from model.test import Test

class TestDao(BaseDao):
    def __init__(self):
        super(TestDao,self).__init__()
        self.test_table = Table('t_test', self.metadata,
                                autoload=True)
        # 将实体类User映射到user表
        mapper(Test, self.test_table)

        # 生成一个会话类，并与上面建立的数据库引擎绑定
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)

        # 创建一个会话
        self.session = self.Session()

    def add_test(self, test_info):
        '''
            # 这个方法根据传递过来的用户信息列表新建一个用户
            # user_info是一个列表，包含了从表单提交上来的信息
        '''
        test = Test(
            test_info['id'],
            test_info['name']
        )
        try:
            self.session.add(test)  # 增加新用户
            self.session.commit()  # 保存修改
            return True,''
        except Exception as ex:
            self.session.rollback()
            return False,ex

    def get_test_byid(self, id):  # 根据用户名返回信息
        return self.session.query(Test).filter_by(id=id).all()[0]

    def get_test_list(self):  # 返回所有用户的列表
        return self.session.query(Test)

    def update_test_byid(self, test_info):  # 根据提供的信息更新用户资料
        id = test_info['id']
        user_info_without_name = {
            'id':test_info['id'],
            'name':test_info['name']
        }
        try:
            self.session.query(Test).filter_by(id=id).update(
                user_info_without_name)
            self.session.commit()
            return True,''
        except Exception as ex:
            return False,ex

    def delete_test_byid(self, id):  # 删除指定用户名的用户
        user_need_to_delete = self.session.query(Test).filter_by(
            id=id).all()[0]
        try:
            self.session.delete(user_need_to_delete)
            self.session.commit()
            return True,''
        except Exception as ex:
            return False,ex
if __name__ == "__main__":
    print('main')
    tdao = TestDao()
    # ret = tdao.AddTest({
    #     'id':7,
    #     'name':'tdqs'
    # })
    # print('ret:',ret)
    # tst = tdao.GetTestByID(7)
    # print(tst.to_dict())
    # tup = tdao.UpdateTestByID({'id':7,'name':'qsgf'})
    # print(tup)
    # tde = tdao.DeleteTestByID(7)
    # print(tde)