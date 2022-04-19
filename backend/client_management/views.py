from django.http import *
from .models import *
import hashlib
from django.shortcuts import *
import os
import sys
sys.path.append(os.path.abspath('..'))
from task_management.models import *
import numpy as np
import requests
import json
from django.shortcuts import render
import json
from django.db.models import Q


## 补充id池
def full_user_id(request):
    for ids in range(10000000,10005000):
        id = user_id_pool()
        id.account_id = ids
        id.save()
    return HttpResponse('成功添加')


## 密码加密函数 finish
def hash_md5(str):
    hash = hashlib.md5()
    hash.update(bytes(str.encode('utf-8')))
    return hash.hexdigest()


## request初始化
def init(request):
    username = request.POST['nickname']
    phone = request.POST['tel']
    password = request.POST['password']
    status = 0
    if username == '':
        status = 1
    elif len(phone)!= 11 or not phone.isdigit():
        status = 2
    elif len(password) < 6:
        status = 3
    if status == 0:
        password = hash_md5(password)
    login = {'username':username,'phone':phone, 'password':password, 'status':status}
    return login


## TODO 发布者登陆
def pro_login(request):
    pw = hash_md5(request.POST['password'])
    account = request.POST['tel']
    info = ''
    if Producer.objects.filter(tel=account).exists():
        Pro = Producer.objects.get(tel=account)
        if Pro.password == pw:
            code = 200
            info = Pro.to_dict()
            request.session['producer'] = info
        else:
            code = 404
    else:
        code = 404
    data = {'code': code, "userInfo": info}
    return JsonResponse(data)


## TODO 标注者登陆
def con_login(request):
    pw = hash_md5(request.POST['password'])
    account = request.POST['tel']
    info = ''
    if Consumer.objects.filter(tel=account).exists():
        Con = Consumer.objects.get(tel=account)
        if Con.password == pw:
            request.session['consumer'] = Con.to_dict()
            code = 200
            info = Con.to_dict()
        else:
            code = 404
    else:
        code = 404
    data = {'code': code, "userInfo": info}
    return JsonResponse(data)


## TODO 发布者注册
def pro_register(request):
    reg = init(request)
    if reg['status'] == 0:
        if Producer.objects.filter(tel=reg['phone']).exist():
            code = 404
        else:
            new = Producer()
            ids = user_id_pool.objects
            id = ids.first()
            account_id = id.account_id
            new.account_id = account_id
            id.delete()
            w = wallet()
            w.account_id = account_id
            w.account_num = 0
            w.save()
            new.tel = reg['phone']
            new.account_id = reg['username']
            new.password = reg['password']
            new.account_type = 1
            new.save()
            code = 200
        data = {'code': code}
    else:
        data = {'code':404}
    return JsonResponse(data)


## TODO 标注者者注册
def con_register(request):
    reg = init(request)
    if reg['status'] == 0:
        if Consumer.objects.filter(tel=reg['phone']).exist():
            code = 404
        else:
            new = Consumer()
            ids = user_id_pool.objects
            id = ids.first()
            account_id = id.account_id
            new.account_id = account_id
            id.delete()
            w = wallet()
            w.account_id = account_id
            w.account_num = 0
            w.save()
            new.phone = reg['phone']
            new.username = reg['username']
            new.password = reg['password']
            new.account_type = 2
            new.save()
            code = 200
        data = {'code': code}
    else:
        data = {'code':404}
    return JsonResponse(data)


## TODO 发布者注销
def pro_logout(request):
    try:
        del request.session['producer']
        code = 200
    except Exception:
        code = 404
    return JsonResponse({'code':code})


## TODO 标注者注销
def con_logout(request):
    try:
        del request.session['consumer']
        code = 200
    except Exception:
        code = 404
    return JsonResponse({'code':code})


def upload_avatar(request):
    pass

def write_data(data, name):
    destination = '..../upload/avatar/'+name
    with open(destination,'wb+') as f:
        for chunk in data.chunks():
            f.write(chunk)
