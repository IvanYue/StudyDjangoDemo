#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2020-05-06 11:31
# @Author  : Yue
# @File    : sqlheper.py
# @Software: PyCharm


import pymysql

def get_list(sql,args=[]):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yyf13320', db='classProject',
                           charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,args)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def modeify(sql,args):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yyf13320', db='classProject',
                           charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, args)
    conn.commit()
    cursor.close()
    conn.close()

def get_one(sql,args):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yyf13320', db='classProject',
                           charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,args)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def create(sql,args=[]):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='yyf13320', db='classProject',
                           charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql, args)
    conn.commit()
    last_row_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return  last_row_id


