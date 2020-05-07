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


# 添加班级
def add_class(request):
    if request.method == 'GET':
        return render(request, 'addclass.html')
    else:
        v = request.POST.get('name')
        if len(v) > 0:
            obj = SQLHelper()
            obj.modify("insert into class(name) values(%s)", [v, ])
            obj.close()
            return redirect('/class/')
        else:
            return render(request, 'addclass.html', {"msg": "班级名称不能为空"})


# 删除班级
def delete_class(request):
    id = request.GET.get('id')
    # ###删除班级老师对应表
    # cursor.execute('delete from tearch2class  where cid = %s', id)
    obj = SQLHelper()
    obj.modify("delete from class where id=%s", id)
    obj.close()
    return redirect('/class/')


# 编辑班级
def edit_class(request):
    if request.method == "GET":
        id = request.GET.get("id")
        obj = SQLHelper()
        result = obj.get_one("select id,name from class where id = %s", id)
        obj.close()
        return render(request, 'edit_class.html', {"result": result})
    else:
        id = request.GET.get("id")
        # id = request.POST.get("id")
        name = request.POST.get("name")
        obj = SQLHelper()
        obj.modify("update class set name = %s where id = %s", [name, id, ])
        obj.close()
        return redirect("/class/")


# 学生列表
def students(request):
    obj = SQLHelper()
    student_list = obj.get_list("select student.id,student.sname,class.name,student.cid from student left join class on student.cid = class.id",
        [])
    class_list = obj.get_list('select id,name from class', [])
    obj.close()
    return render(request, "students.html", {"student_list": student_list, 'class_list': class_list})


# 添加学生
def addStudent(request):
    if request.method == "GET":
        obj = SQLHelper()
        classes = obj.get_list("select id,name from class")
        obj.close()
        return render(request, "addStudent.html", {'classes': classes})
    else:

        class_id = request.POST.get("class_id")
        sname = request.POST.get("sname")

        obj = SQLHelper()
        obj.modify("insert into student( sname, cid) value (%s,%s)", [sname, class_id])
        obj.close()
        return redirect("/students/")



# 删除学生
def deleteStudent(request):
    id = request.GET.get("id")

    obj = SQLHelper()
    obj.modify("delete from student  where id = %s", id)
    obj.close()

    return redirect("/students/")




# 编辑学生
def edit_student(request):
    if request.method == "GET":
        id = request.GET.get("id")
        obj = SQLHelper()
        class_list = obj.get_list("select id,name from class", [])
        student = obj.get_one(
            "select student.id,student.sname,student.cid,class.name from student left join class on  student.cid = class.id where student.id = %s",
            id)
        obj.close()
        return render(request, "edit_student.html", {"student": student, "class_list": class_list})
    else:
        id = request.POST.get("id")
        sname = request.POST.get("sname")
        cid = request.POST.get("class_id")
        obj = SQLHelper()
        obj.modify("update student set sname = %s,cid = %s where id = %s", [sname, cid, id, ])
        obj.close()
        return redirect("/students/")

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


# 添加老师
def addtearchers(request):
    if request.method == 'GET':
        obj = SQLHelper()
        class_list = obj.get_list('select * from class')
        obj.close()
        return render(request,'addTearcher.html',{"class_list":class_list})
    else:
        tname = request.POST.get('tname')
        clds = request.POST.getlist('class_ids')
        obj = SQLHelper()
        #老师表中添加数据 #获取老师id
        tearcher_id = obj.create('insert into tearcher(tname) values (%s)', [tname])
        #老师班级表中插入数据
        sql_args = []
        for cid in clds:
            temp = (tearcher_id,cid)
            sql_args.append(temp)
        obj.multiple_modify('insert into tearch2class(tid, cid) values (%s,%s)', sql_args)
        obj.close()

        return redirect('/tearchers/')

def editTearcher(request):

    if request.method == 'GET':
        tid = request.GET.get('tid')
        obj = SQLHelper()
        tearcher_info = obj.get_one('select tid,tname from tearcher where tid = %s',[tid])
        tearcher_class_list = obj.get_list('select cid from tearch2class where tearch2class.tid = %s',[tid,])
        class_list = obj.get_list('select id,name from class')
        obj.close()
        temp = []
        for i in tearcher_class_list:
            temp.append(i['cid'])
        return render(request,'edit_tearcher.html',{
            'info':tearcher_info,
            'tearcher_class_list':temp,
            'class_list':class_list
        })
    else:
        tid = request.GET.get('tid')
        class_ids = request.POST.getlist('class_ids')
        tname = request.POST.get('tname')
        #更新老师表
        obj = SQLHelper()
        obj.modify('update tearcher set tname=%s where tid = %s',[tname,tid])
        #更细老师班级关系表
        # 方案一：先删除老师和班级的对应关系删除，之后再做添加
        obj.modify('delete from tearch2class where tid = %s',[tid])
        sql_args = []
        for cid in class_ids:
            temp = (tid, cid)
            sql_args.append(temp)
        obj.multiple_modify('insert into tearch2class(tid, cid) values (%s,%s)', sql_args)
        obj.close()
        # 方案二：把新的班级数据和老的数据做对比进行删除和增加
        return  redirect('/tearchers/')
    
def deleteTearcher(request):
    tid = request.GET.get('tid')
    obj = SQLHelper()
    obj.modify('delete from tearcher  where tid = %s', tid)
    obj.modify('delete from tearch2class  where tid = %s', tid)
    obj.close()
    return redirect('/tearchers/')

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