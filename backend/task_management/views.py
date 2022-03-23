from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render
import json
from django.db.models import Q
from django.http import *
import numpy as np
import requests
import json
from .models import *
import hashlib


## TODO 增加任务函数
def insert(request):
    try:
        uid = request.GET['uid']
        price = request.GET['price']
        owner = request.GET['owner']
        t = Task()
        t.uid = uid
        t.price = price
        t.owner = owner
        t.save()
        data = {'code':200,'msg':'添加任务成功'}
    except BaseException:
        data = {'code':404,'msg':'添加任务失败'}
    return JsonResponse(data)


## TODO 删除任务函数
def delete(request):
    try:
        uid = request.GET['uid']
        if Task.objects.filter(uid=uid).exist():
            task = Task.objects.get(uid=uid)
            task.delete()
            data = {'code':200,'msg':'删除成功'}
        else:
            data = {'code':402,'msg':'不存在删除对象'}
    except BaseException:
        data = {'code':404,'msg':'删除失败'}
    return JsonResponse(data)


## TODO 编辑任务函数
def edit(request):
    try:
        uid = request.GET['uid']
        price = request.GET['price']
        owner = request.GET['owner']
        if Task.objects.filter(uid=uid).exist():
            t = Task.objects.get(uid=uid)
            t.price = price
            t.owner = owner
            t.save()
            data = {'code': 200, 'msg': '修改成功'}
        else:
            data = {'code':402,'msg':'未找到该任务'}
    except BaseException:
        data = {'code':404,'msg':'修改失败'}
    return JsonResponse(data)


## TODO 查询任务函数
def query(request):
    try:
        uid = request.GET['uid']
        t = Task.objects.get(uid=uid)
        task_info = {'uid':uid,'price':t.price,'owner':t.owner}
        data = {'code': 200, 'msg': '查询成功', 'task_info':task_info}
    except BaseException:
        data = {'code': 404, 'msg': '查询失败','task_info':''}
    return JsonResponse(data)


## TODO 接单
