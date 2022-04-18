from django.shortcuts import render
import json
from django.db.models import Q
from django.http import *
import numpy as np
import requests
import json
from .models import *
import hashlib
from django.shortcuts import *


## 密码加密函数 finish
def hash_md5(str):
    hash = hashlib.md5()
    hash.update(bytes(str.encode('utf-8')))
    return hash.hexdigest()


## request初始化
def init(request):
    username = request.POST['name']
    phone = request.POST['tel']
    mail = request.POST['mail_add']
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
    login = {'username':username,'phone':phone,'mail':mail, 'password':password, 'status':status}
    return login


## TODO 发布者登陆
def pro_login(request):
    pw = hash_md5(request.POST['password'])
    account = request.POST['tel']
    if '@' not in account:
        if Producer.objects.filter(tel=account).exists():
            Pro = Producer.objects.get(tel=account)
            if Pro.password == pw:
                code = 200
                info = Pro.to_dict()
                request.session['producer'] = info
            else:
                code = 402
        else:
            code = 404
    else:
        if Producer.objects.filter(email_add=account).exists():
            Pro = Producer.objects.get(email_add=account)
            if Pro.password == pw:
                code = 200
                info = Pro.to_dict()
                request.session['producer'] = info
            else:
                code = 402
        else:
            code = 404
    data = {'code': code, "userInfo": info}
    return JsonResponse(data)


## TODO 接单者登陆
def con_login(request):
    pw = hash_md5(request.POST['password'])
    account = request.POST['account_id']
    if '@' not in account:
        if Consumer.objects.filter(tel=account).exists():
            Con = Consumer.objects.get(tel=account)
            if Con.password == pw:
                request.session['consumer'] = Con.to_dict()
                code = 200
            else:
                code = 402
        else:
            code = 404
    else:
        if Consumer.objects.filter(email_add=account).exists():
            Con = Consumer.objects.get(email_add=account)
            if Con.password == pw:
                request.session['consumer'] = Con.to_dict()
                code = 200
            else:
                code = 402
        else:
            code = 404
    data = {'code': code}
    return JsonResponse(data)


## TODO 发布者注册
def pro_register(request):
    reg = init(request)
    if reg['status'] == 0:
        if Producer.objects.filter(tel=reg['phone']).exist():
            code = 404
        elif Producer.objects.filter(email_add=reg['email']).exist():
            code = 404
        else:
            new = Producer()
            new.tel = reg['phone']
            new.email_add = reg['email']
            new.account_id = reg['username']
            new.password = reg['password']
            new.save()
            code = 200
        data = {'code': code}
    else:
        data = {'code':404}
    return JsonResponse(data)


## TODO 接单者注册
def con_register(request):
    reg = init(request)
    if reg['status']==0:
        if Consumer.objects.filter(tel=reg['phone']).exist():
            code = 404
        elif Consumer.objects.filter(email_add=reg['email']).exist():
            code = 404
        else:
            new = Consumer()
            new.phone = reg['phone']
            new.email = reg['email']
            new.username = reg['username']
            new.password = reg['password']
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


## TODO 接单者注销
def con_logout(request):
    try:
        del request.session['consumer']
        code = 200
    except Exception:
        code = 404
    return JsonResponse({'code':code})
