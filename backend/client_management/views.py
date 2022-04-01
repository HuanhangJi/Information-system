from django.shortcuts import render
import json
from django.db.models import Q
from django.http import *
import numpy as np
import requests
import json
from models import *
import hashlib
from django.shortcuts import *


## 密码加密函数 finish
def hash_md5(str):
    hash = hashlib.md5()
    hash.update(bytes(str.encode('utf-8')))
    return hash.hexdigest()


## request初始化
def init(request):
    username = request.POST['user']
    phone = request.POST['phone']
    mail = request.POST['mail']
    password = request.POST['password']
    status = 0
    msg = ''
    if username == '':
        status = 1
        msg = '用户名未填写'
    elif len(phone)!= 11 or not phone.isdigit():
        status = 2
        msg = '手机号码格式错误'
    elif len(password) < 6:
        status = 3
        msg = '密码设置格式错误'
    if status == 0:
        password = hash_md5(password)
    login = {'username':username,'phone':phone,'mail':mail, 'password':password, 'status':status, 'msg':msg}
    return login


## TODO 发布者登陆
def pro_login(request):
    pw = hash_md5(request.POST['password'])
    info = ''
    account = request.POST['user']
    if '@' not in account:
        if Producer.objects.filter(phone=account).exists():
            Pro = Producer.objects.get(phone=account)
            if Pro.password == pw:
                code = 200
                msg = '登陆成功'
                info = Pro.to_dict()
                request.session['producer'] = info
            else:
                code = 402
                msg = '用户名或密码错误'
        else:
            code = 404
            msg = '用户名或密码错误'
    else:
        if Producer.objects.filter(email=account).exists():
            Pro = Producer.objects.get(email=account)
            if Pro.password == pw:
                code = 200
                msg = '登陆成功'
                info = Pro.to_dict()
                request.session['producer'] = info
            else:
                code = 402
                msg = '用户名或密码错误'
        else:
            code = 404
            msg = '用户名或密码错误'
    data = {'code': code, 'msg': msg, "userInfo": info}
    return JsonResponse(data)


## TODO 接单者登陆
def con_login(request):
    pw = hash_md5(request.POST['password'])
    info = ''
    account = request.POST['user']
    if '@' not in account:
        if Consumer.objects.filter(phone=account).exists():
            Con = Consumer.objects.get(phone=account)
            if Con.password == pw:
                request.session['consumer'] = Con.to_dict()
                code = 200
                msg = '登陆成功'
                info = Con.to_dict()
            else:
                code = 402
                msg = '用户名或密码错误'
        else:
            code = 404
            msg = '用户名或密码错误'
    else:
        if Consumer.objects.filter(email=account).exists():
            Con = Consumer.objects.get(email=account)
            if Con.password == pw:
                request.session['consumer'] = Con.to_dict()
                code = 200
                msg = '登陆成功'
                info = Con.to_dict()
            else:
                code = 402
                msg = '用户名或密码错误'
        else:
            code = 404
            msg = '用户名或密码错误'
    data = {'code': code, 'msg': msg, "userInfo": info}
    return JsonResponse(data)


## TODO 发布者注册
def pro_register(request):
    reg = init(request)
    if reg['status'] == 0:
        if Producer.objects.filter(phone=reg['phone']).exist():
            code = 404
            msg = '该手机已经被注册'
        elif Producer.objects.filter(email=reg['email']).exist():
            code = 404
            msg = '该邮箱已经被注册'
        else:
            new = Producer()
            new.phone = reg['phone']
            new.email = reg['email']
            new.username = reg['username']
            new.password = reg['password']
            new.save()
            code = 200
            msg = '注册成功'
        data = {'code': code, 'msg': msg}
    else:
        data = {'code':404, 'msg':reg['msg'] }
    return JsonResponse(data)


## TODO 接单者注册
def con_register(request):
    reg = init(request)
    if reg['status']==0:
        if Consumer.objects.filter(phone=reg['phone']).exist():
            code = 404
            msg = '该手机已经被注册'
        elif Consumer.objects.filter(email=reg['email']).exist():
            code = 404
            msg = '该邮箱已被注册'
        else:
            new = Consumer()
            new.phone = reg['phone']
            new.email = reg['email']
            new.username = reg['username']
            new.password = reg['password']
            new.save()
            code = 200
            msg = '注册成功'
        data = {'code': code, 'msg': msg}
    else:
        data = {'code':404,'msg':reg['msg']}
    return JsonResponse(data)

## TODO 发布者注销
def pro_logout(request):
    try:
        del request.session['producer']
        code = 200
    except Exception:
        code = 404
    return JsonResponse({'code':code})

## TODO 接单者注销
def con_logout(request):
    try:
        del request.session['consumer']
        code = 200
    except Exception:
        code = 404
    return JsonResponse({'code':code})