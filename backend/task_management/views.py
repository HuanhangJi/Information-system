import pylab as p
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


def full_project_id(request):
    for ids in range(10000000,10005000):
        id = project_id_pool()
        id.project_id = ids
        id.save()
    return HttpResponse('成功添加')


## TODO 增加任务函数
def insert(request):
    # try:
        publisher_id = request.GET['publisher_id']
        project_name = request.GET['project_name']
        project_type = request.GET['project_type']
        description = request.GET['description']
        due_time = request.GET['due_time']
        pay_per_task = request.GET['pay_per_task']
        task_num = request.GET['task_num']
        p = Project()
        id = project_id_pool().objects.first()
        p.project_id = id.project_id
        id.delete()
        p.publisher_id = publisher_id
        p.project_type = project_type
        p.completed_task_num = 0
        p.task_num = task_num
        p.project_status = 0
        p.payment_per_task = pay_per_task
        p.due_time = due_time
        p.description = description
        p.project_name = project_name
        p.save()
        data = {'code':200,'msg':'添加任务成功'}
    # except BaseException:
    #     data = {'code':404,'msg':'添加任务失败'}
        return JsonResponse(data)


## TODO 删除任务函数
def delete(request):
    # try:
        project_id = request.GET['project_id']
        if Project.objects.filter(project_id=project_id).exist():
            project = Project.objects.get(project_id=project_id)
            project.delete()
            data = {'code':200,'msg':'删除成功'}
        else:
            data = {'code':402,'msg':'不存在删除对象'}
    # except BaseException:
    #     data = {'code':404,'msg':'删除失败'}
        return JsonResponse(data)


## TODO 编辑任务函数
def edit(request):
    # try:
        project_id = request.GET['project_id']
        project_name = request.GET['project_name']
        description = request.GET['description']
        due_time = request.GET['due_time']
        pay_per_task = request.GET['pay_per_task']
        task_num = request.GET['task_num']
        if Project.objects.filter(project_id=project_id).exist():
            p = Project.objects.get(project_id=project_id)
            p.project_name = project_name
            p.description = description
            p.due_time = due_time
            p.payment_per_task = pay_per_task
            p.task_num = task_num
            p.save()
            data = {'code': 200, 'msg': '修改成功'}
        else:
            data = {'code':404,'msg':'未找到该任务'}
    # except BaseException:
    #     data = {'code':404,'msg':'修改失败'}
        return JsonResponse(data)


## TODO 查询任务函数
def query(request):
    # try:
        keyword = request.GET['keyword']
        t = Project.objects.get(project_id=keyword)
        info = t.to_dict()
        data = {'code': 200, 'msg': '查询成功', 'task_info':info}
    # except BaseException:
    #     data = {'code': 404, 'msg': '查询失败','task_info':''}
        return JsonResponse(data)



