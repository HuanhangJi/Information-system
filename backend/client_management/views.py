from django.http import *
from .models import *
import hashlib
from django.shortcuts import *
import os
import datetime
import sys
sys.path.append(os.path.abspath('..'))
from task_management.models import *
import numpy as np
import requests
import json
from django.shortcuts import render
import json
from django.db.models import Q


## 补充id池 FINISH
def full_user_id(request):
    for ids in range(10000000,10005000):
        id = User_id_pool()
        id.account_id = ids
        id.save()
    return HttpResponse('成功添加')


## 密码加密函数 FINISH
def hash_md5(str):
    hash = hashlib.md5()
    hash.update(bytes(str.encode('utf-8')))
    return hash.hexdigest()


## request初始化 FINISH
def init(request):
    res = get_res(request)
    username = res['nickname']
    phone = res['tel']
    password = res['password']
    status = 0
    if status == 0:
        password = hash_md5(password)
    login = {'username':username,'phone':phone, 'password':password, 'status':status}
    return login


## request取数据 FINISH
def get_res(request):
    data = request.body.decode('utf-8')
    res = json.loads(data)
    return res



## TODO 发布者登陆
def pro_login(request):
    res = get_res(request)
    pw = hash_md5(res['password'])
    account = res['tel']
    info = ''
    if Producer.objects.filter(tel=account).exists():
        Pro = Producer.objects.get(tel=account)
        if Pro.password == pw:
            code = 200
            info = Pro.to_dict()
            request.session['user'] = info
        else:
            code = 404
    else:
        code = 404
    data = {'code': code, "userInfo": info}
    return JsonResponse(data)


## TODO 标注者登陆
def con_login(request):
    res = get_res(request)
    pw = hash_md5(res['password'])
    account = res['tel']
    info = ''
    if Consumer.objects.filter(tel=account).exists():
        Con = Consumer.objects.get(tel=account)
        if Con.password == pw:
            request.session['user'] = Con.to_dict()
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
            msg = '手机已绑定'
        else:
            new = Producer()
            ids = User_id_pool.objects
            id = ids.first()
            account_id = id.account_id
            new.account_id = account_id
            id.delete()
            w = Wallet()
            w.account_id = account_id
            w.account_num = 0
            w.save()
            new.tel = reg['phone']
            new.nickname = reg['username']
            new.password = reg['password']
            new.account_type = 1
            new.save()
            code = 200
        data = {'code': code,'msg':msg}
    else:
        msg = '网络拥堵，请稍后再试'
        data = {'code':404,'msg':msg}
    return JsonResponse(data)


def con_register(request):
    reg = init(request)
    if reg['status'] == 0:
        if Consumer.objects.filter(tel=reg['phone']).exists():
            code = 404
            msg = "手机号已绑定"
        else:
            new = Consumer()
            ids = User_id_pool.objects
            id = ids.first()
            account_id = id.account_id
            new.account_id = account_id
            id.delete()
            w = Wallet()
            w.account_id = account_id
            w.account_num = 0
            w.save()
            new.tel = reg['phone']
            new.nickname = reg['username']
            new.password = reg['password']
            new.account_type = 2
            new.save()
            code = 200
        data = {'code': code,"msg":msg}
    else:
        msg = "网络堵塞，请稍后"
        data = {'code':404,"msg":msg}
    return JsonResponse(data)

## TODO 发布者注销
def pro_logout(request):
    # try:
        del request.session['user']
        code = 200
    # except Exception:
    #     code = 404
        return JsonResponse({'code':code})


## TODO 标注者注销
def con_logout(request):
    # try:
        del request.session['user']
        code = 200
    # except Exception:
    #     code = 404
        return JsonResponse({'code':code})


## TODO 上传头像
def upload_avatar(request):
    avatar = request.FILES['avatar']
    account_id = request.session['user']['account_id']
    avatar_type = avatar.name.split('.').pop()
    write_data(avatar,account_id+'.'+avatar_type)


def write_data(data, name):
    destination = '..../upload/avatar/'+name
    if os.path.exists(destination):
        os.remove(destination)
    with open(destination,'wb+') as f:
        for chunk in data.chunks():
            f.write(chunk)


## TODO 设置支付密码
def set_payment_password(request):
    res = get_res(request)
    payment_pass = res['payment_password']
    account_id = request.session['user']['account_id']
    W = Wallet.objects.get(account_id=account_id)
    W.payment_password = hash_md5(str(payment_pass))
    W.save()


## TODO 钱包转账提现
def change_wallet(request):
    res = get_res(request)
    cw_type = res['cw_type']
    account_id = request.session['user']['account_id']
    cw_amount = res['cw_amount']
    payment_pass = res['payment_password']
    r = Wallet_record()
    w = Wallet.objects.get(account_id=account_id)
    if hash_md5(str(payment_pass)) == w.payment_password:
        if cw_type == 'recharge':
            w.account_num += cw_amount
            w.save()
        if cw_type == 'withdraw':
            if w.account_num >= cw_amount:
                w.account_num -= cw_amount
                w.save()
            else:
                info = {'code': 404}
                return JsonResponse(info)
    else:
        info = {'code': 404}
        return JsonResponse(info)
    pay_time = datetime.datetime.now()
    r.cw_type = cw_type
    r.cw_amount = cw_amount
    r.AB_id = w.AB_id
    r.pay_time = pay_time
    r.save()
    info = {'code': 200}
    return JsonResponse(info)