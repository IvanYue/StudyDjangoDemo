#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2020-04-27 01:50
# @Author  : Yue
# @File    : sqlheper.py
# @Software: PyCharm

import  pymysql
class SQLHelper(object):

    def __init__(self):
        self.connect()
        
    #连接
    def connect(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yyf13320', db='classProject',
                               charset='utf8')
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
    #获取列表
    def get_list(self,sql,args=[]):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return result
    #获取一条
    def get_one(self,sql,args=[]):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return result
    #修改，删除
    def modify(self,sql,args=[]):
        self.cursor.execute(sql, args)
        self.conn.commit()
    #增加并返回新增的id
    def create(self,sql,args=[]):
        self.cursor.execute(sql, args)
        self.conn.commit()
        return  self.cursor.lastrowid
    #批量操作
    def multiple_modify(self,sql,args=[]):
        # self.cursor.executemany('insert into tearch2class(tid, cid) VALUES (%s,%s)',[(1,2),(2,3),(3,5)])
        self.cursor.executemany(sql,args)
        self.conn.commit()
    #关闭
    def close(self):
        self.cursor.close()
        self.conn.close()