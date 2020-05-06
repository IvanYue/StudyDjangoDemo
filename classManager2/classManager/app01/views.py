#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2020-04-06 22:33
# @Author  : Yue
# @File    : views.py
# @Software: PyCharm

from django.shortcuts import render, redirect, HttpResponse
from utils.SQLHelper import SQLHelper

# 班级列表
def classes(request):
    obj = SQLHelper()
    class_list = obj.get_list("select id,name from class")
    obj.close()
    return render(request, 'classes.html', {"class_list": class_list})


# 学生列表
def students(request):
    obj = SQLHelper()
    student_list = obj.get_list("select student.id,student.sname,class.name,student.cid from student left join class on student.cid = class.id",
        [])
    class_list = obj.get_list('select id,name from class', [])
    obj.close()
    return render(request, "students.html", {"student_list": student_list, 'class_list': class_list})



###老师列表
def tearchers(request):
    obj = SQLHelper()
    tearcher_list = obj.get_list('''
        SELECT tearcher.tid,tearcher.tname,tearch2class.cid,class.name from tearcher  
        LEFT JOIN tearch2class on tearcher.tid = tearch2class.tid    
        LEFT JOIN class ON class.id = tearch2class.cid;
    ''', [])
    result = {}
    for tearcher in tearcher_list:
        tid = tearcher['tid']
        if tid in result:
            result[tid]['classes'].append({'cid':tearcher['cid'],'name':tearcher['name']})
        else:
            result[tid] = {
                'tid':tearcher['tid'],
                'tname':tearcher['tname'],
                'classes':[{'cid':tearcher['cid'],'name':tearcher['name']}],

            }
    class_list = obj.get_list('select * from class')
    obj.close()
    return render(request, 'tearchers.html', {'result': result.values(),"class_list":class_list})




#############对话框#############

import json
from static import sqlheper


###班级
def model_add_class(request):
    name = request.POST.get('name')
    if len(name) > 0:
        sqlheper.modeify('insert into class(name) values (%s)', [name])
        # 刷新原因：FORM表单提交特性，一提交页面就会刷新
        # return  redirect('/class/')
        return HttpResponse('ok')
    else:
        return HttpResponse('标题不能为空')


def model_edit_class(request):
    ret = {'status': True, 'msg': None}
    try:
        id = request.POST.get('id')
        name = request.POST.get('name')
        sqlheper.modeify('update class set name=%s where id=%s', [name, id, ])
    except Exception as e:
        ret['status'] = False
        ret['msg'] = '处理异常'

    return HttpResponse(json.dumps(ret))


def model_delete_class(request):
    id = request.POST.get('id')
    try:
        sqlheper.modeify("delete from class  where id = %s", [id, ])
        #删除老师班级对应表里对应的数据
        sqlheper.modeify('delete from tearch2class  where cid = %s', id)
        return HttpResponse('删除成功')
    except Exception as e:
        return HttpResponse(str(e))


###学生
def model_add_student(request):
    ret = {'status': True, 'msg': None}

    sname = request.POST.get('sname')
    cid = request.POST.get('cid')

    try:
        sqlheper.modeify('insert into student(sname, cid) values (%s,%s)', [sname, cid])
    except Exception as e:
        ret['status'] = False
        ret['msg'] = str(e)

    return HttpResponse(json.dumps(ret))


def model_edit_student(request):
    ret = {'status': True, 'msg': None}
    cid = request.POST.get('cid')
    sname = request.POST.get('sname')
    sid = request.POST.get('sid')
    try:
        sqlheper.modeify("update student set sname=%s,cid=%s where id=%s", [sname, cid, sid])
    except Exception as e:
        ret['status'] = False
        ret['msg'] = str(e)
    return HttpResponse(json.dumps(ret))


def model_delete_student(request):
    sid = request.POST.get('sid')
    try:
        sqlheper.modeify("delete from student where id = %s", [sid])
        return HttpResponse('删除成功')
    except Exception as e:
        return HttpResponse(str(e))


def model_add_teacher(request):
    ret = {'status':True,'msg':None}
    try:
        tname = request.POST.get('tname')
        cids = request.POST.getlist("cids")
        tearcher_id = sqlheper.create('insert into tearcher(tname) values (%s)', [tname])
        obj = sqlheper.SQLHelper()
        sql_args = []
        for cid in cids:
            temp = (tearcher_id, cid)
            sql_args.append(temp)
        obj.multiple_modify('insert into tearch2class(tid, cid) values (%s,%s)', sql_args)
        obj.close()
    except Exception as e:
        ret['status'] = False
        ret['msg'] = str(e)

    return  HttpResponse(json.dumps(ret))



#获取全部班级
def get_all_class(requset):
    import  time
    time.sleep(0.25)
    obj = sqlheper.SQLHelper()
    class_list = obj.get_list('select id,name from class')
    obj.close()
    return  HttpResponse(json.dumps(class_list))


#登录
def login(request):
    if request.method == 'GET':
        return  render(request,'login.html')
    else:
        account = request.POST.get('account')
        pwd = request.POST.get('pwd')

        ret = {'status': False, 'msg': '账号或密码错误'}

        obj = sqlheper.SQLHelper()
        users = obj.get_list('select account,pwd from admin')
        obj.close()
        for item in users:

            if account == item['account']:
                if pwd == item['pwd']:
                    ret = {'status': True, 'msg': '登录成功'}
                    return HttpResponse(json.dumps(ret))
                else:
                    return HttpResponse(json.dumps(ret))
            else:
                ret = {'status': False, 'msg': '该用户尚未注册'}
                return HttpResponse(json.dumps(ret))

def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        account = request.POST.get('account')
        pwd = request.POST.get('pwd')
        ret = {'status': True, 'msg': '注册成功'}
        try:
            obj = sqlheper.SQLHelper()
            obj.modify('insert into admin(account,pwd) values (%s,%s)', [account, pwd, ])
            obj.close()
        except Exception as e:
            ret['status'] = False
            ret['msg'] = '注册失败'
        return HttpResponse(json.dumps(ret))

def layout(request):
    return render(request,'layout.html')