from django.http import *
from .models import *
import os
import sys
sys.path.append(os.path.abspath('..'))
from client_management.models import *
from django.shortcuts import render
import json
from django.db.models import Q


## 补充ID池
def full_project_id(request):
    for ids in range(10000000,10005000):
        id = project_id_pool()
        id.project_id = ids
        id.save()
    return HttpResponse('成功添加')


## 判断分数
def judge_score(payment):
    payment = int(payment)
    if payment < 50:
        score = 100
    elif payment <100:
        score = 300
    else:
        score = 500
    return score


## TODO 增加任务函数
def project_add(request):
    # try:
        publisher_id = request.GET['publisher_id']
        project_name = request.GET['project_name']
        project_type = request.GET['project_type']
        description = request.GET['description']
        due_time = request.GET['due_time']
        pay_per_task = request.GET['pay_per_task']
        task_num = request.GET['task_num']
        sample_document = request.GET['sample_document']
        p = Project()
        id = project_id_pool().objects.first()
        project_id = id.project_id
        p.project_id = project_id
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
        p.sample_document = sample_document
        p.save()
        for i in range(1,task_num+1):
            t = Task()
            t.project_id = project_id
            t.task_id = project_id+'_'+str(i)
            t.score = judge_score(pay_per_task)
            t.original_data = sample_document
            t.due_time = due_time
            t.task_status = 0
        data = {'code':200,'msg':'添加任务成功'}
    # except BaseException:
    #     data = {'code':404,'msg':'添加任务失败'}
        return JsonResponse(data)


## TODO 删除任务函数
def project_delete(request):
    # try:
        project_id = request.GET['project_id']
        if Project.objects.filter(project_id=project_id).exist():
            Project.objects.get(project_id=project_id).delete()
            Task.objects.filter(project_id=project_id).delete()
            data = {'code':200,'msg':'删除成功'}
        else:
            data = {'code':402,'msg':'不存在删除对象'}
    # except BaseException:
    #     data = {'code':404,'msg':'删除失败'}
        return JsonResponse(data)


## TODO 编辑任务函数
def project_edit(request):
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
def project_query(request):
    # try:
        keyword = request.GET['keyword']
        t = Project.objects.get(project_id=keyword)
        info = t.to_dict()
        data = {'code': 200, 'msg': '查询成功', 'task_info':info}
    # except BaseException:
    #     data = {'code': 404, 'msg': '查询失败','task_info':''}
        return JsonResponse(data)



