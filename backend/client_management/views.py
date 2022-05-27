from django.http import *
from .models import *
import hashlib
from django.shortcuts import *
import os
import datetime
import sys
sys.path.append(os.path.abspath('..'))
os.chdir(os.path.abspath(os.getcwd()))
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
    return res['info']



## 发布者登陆 FINISH
def pro_login(request):
    res = get_res(request)
    pw = hash_md5(res['password'])
    account = str(res['tel'])
    info = ''
    if Producer.objects.filter(tel=account).exists():
        Pro = Producer.objects.get(tel=account)
        if Pro.password == pw:
            code = 200
            info = Pro.to_dict()
            t = Token()
            t.account_id = info['account_id']
            t.save()
            w = Wallet.objects.get(account_id=info['account_id'])
            if w.payment_password != None:
                info['wallet_status'] = 1
            else:
                info['wallet_status'] = 0
        else:
            code = 404
    else:
        code = 404
    data = {'code': code, "userInfo": info}
    print(data)
    return JsonResponse(data)


## 标注者登陆 FINISH
def con_login(request):
    res = get_res(request)
    pw = hash_md5(res['password'])
    account = str(res['tel'])
    info = ''
    if Consumer.objects.filter(tel=account).exists():
        Con = Consumer.objects.get(tel=account)
        if Con.password == pw:
            code = 200
            info = Con.to_dict()
            t = Token()
            t.account_id = info['account_id']
            t.save()
            w = Wallet.objects.get(account_id=info['account_id'])
            if w.payment_password != '':
                info['wallet_status'] = 1
            else:
                info['wallet_status'] = 0
        else:
            code = 404
    else:
        code = 404
    data = {'code': code, "userInfo": info}
    print(data)
    return JsonResponse(data)


## 发布者注册 FINISH
def pro_register(request):
    reg = init(request)
    if reg['status'] == 0:
        if Producer.objects.filter(tel=reg['phone']).exists():
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
            new.status = 1
            new.save()
            code = 200
            msg = ''
        data = {'code': code,'msg':msg}
    else:
        msg = '网络拥堵，请稍后再试'
        data = {'code':404,'msg':msg}
    return JsonResponse(data)


## 标注者注册 FINISH
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
            new.status = 1
            new.level = 1
            new.experience = 0
            new.save()
            code = 200
            msg = ''
        data = {'code': code,"msg":msg}
    else:
        msg = "网络堵塞，请稍后"
        data = {'code':404,"msg":msg}
    return JsonResponse(data)

## TODO 注销
def logout(request):
    # try:
        account_id = get_res(request)['account_id']
        t = Token.objects.filter(account_id=account_id)
        t.delete()
        code = 200
    # except Exception:
    #     code = 404
        return JsonResponse({'code':code})


## TODO 上传头像
def upload_avatar(request, account_id, usertype):
    # try:
        print(os.getcwd())
        avatar = request.FILES['file']
        account_id = str(account_id)
        avatar_type = avatar.name.split('.').pop()
        write_data(avatar,account_id+'.'+avatar_type)
        if usertype == 1:
            p = Producer.objects.get(account_id=account_id)
            p.avatar = f"http://localhost:8000/static/avatar/{account_id}.{avatar_type}"
            p.save()
        if usertype == 2:
            c = Consumer.objects.get(account_id=account_id)
            c.avatar = f"http://localhost:8000/static/avatar/{account_id}.{avatar_type}"
            c.save()
        return JsonResponse({"code": 200,"url":f"http://localhost:8000/static/avatar/{account_id}.{avatar_type}"})
    # except Exception:
    #     return JsonResponse({"code": 404})



def write_data(data, name):
    destination = './static/avatar/'+name
    print(os.getcwd())
    try:
        if os.path.exists(destination):
            os.remove(destination)
        with open(destination,'wb') as f:
            for chunk in data.chunks():
                f.write(chunk)
    except Exception:
        pass


## TODO 设置支付密码
def set_payment_password(pay_password,account_id):
    payment_pass = pay_password
    account_id = account_id
    W = Wallet.objects.get(account_id=account_id)
    W.payment_password = hash_md5(str(payment_pass))
    W.save()


## TODO 钱包转账提现
def withdraw_wallet(request):
    res = get_res(request)
    account_id = res['account_id']
    cw_amount = int(res['cw_amount'])
    payment_pass = res['payment_password']
    r = Wallet_record()
    w = Wallet.objects.get(account_id=account_id)
    if hash_md5(str(payment_pass)) == w.payment_password:
        if w.account_num >= cw_amount:
            w.account_num -= cw_amount
            w.save()
        else:
            info = {'code': 404, 'msg':'钱包金额不足'}
            return JsonResponse(info)
    else:
        info = {'code': 404, 'msg':'网络连接异常'}
        return JsonResponse(info)
    pay_time = str(datetime.datetime.now())
    r.cw_type = 'withdraw'
    r.cw_amount = cw_amount
    r.AB_id = w.AB_id
    r.pay_time = pay_time
    r.save()
    info = {'code': 200}
    return JsonResponse(info)


def recharge_wallet(request):
    res = get_res(request)
    account_id = res['account_id']
    account_num = int(res['account_num'])
    r = Wallet_record()
    w = Wallet.objects.get(account_id=account_id)
    w.account_num += account_num
    w.save()
    pay_time = datetime.datetime.now()
    r.cw_type = 'recharge'
    r.cw_amount = account_num
    r.AB_id = w.AB_id
    r.pay_time = pay_time
    r.save()
    info = {'code': 200}
    return JsonResponse(info)



## TODO 修改用户信息
def user_change(request):
    res = get_res(request)
    account_id = res['account_id']
    usertype = res['usertype']
    type = res['type']
    value = res['value']
    print(type)
    print(value)
    if type == 'pay_password':
        set_payment_password(value,account_id)
    if usertype == 'pointer':
        if type == 'password':
            c = Consumer.objects.get(account_id=account_id)
            c.password = hash_md5(value)
            c.save()
        if type == 'phone':
            c = Consumer.objects.get(account_id=account_id)
            c.tel = value
            c.save()
        if type == 'nickname':
            c = Consumer.objects.get(account_id=account_id)
            c.nickname = value
            c.save()
    if usertype == 'poster':
        if type == 'password':
            p = Producer.objects.filter(account_id=account_id)
            p.password = hash_md5(value)
            p.save()
        if type == 'phone':
            p = Producer.objects.get(account_id=account_id)
            p.tel = value
            p.save()
        if type == 'nickname':
            p = Producer.objects.get(account_id=account_id)
            p.nickname = value
            p.save()
    if usertype == 'pointer':
        c = Consumer.objects.get(account_id=account_id)
        info = c.to_dict()
        w = Wallet.objects.get(account_id=account_id)
        if w.payment_password != '':
            info['wallet_status'] = 1
        else:
            info['wallet_status'] = 0
    if usertype == 'poster':
        p = Producer.objects.get(account_id=account_id)
        info = p.to_dict()
        w = Wallet.objects.get(account_id=account_id)
        if w.payment_password != '':
            info['wallet_status'] = 1
        else:
            info['wallet_status'] = 0
    return JsonResponse(info)

def wallet_info(request):
    res = get_res(request)
    account_id = res['account_id']
    w = Wallet.objects.get(account_id=account_id)
    account_num = w.account_num
    print(account_num)
    return JsonResponse({'account_num':account_num})

