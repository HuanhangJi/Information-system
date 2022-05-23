import datetime
from django.http import *
from .models import *
import os
import sys
sys.path.append(os.path.abspath('..'))
from client_management.models import *
from django.db.models import Q
from django.shortcuts import render
import json
import zipfile


## request初始化 FINISH
def get_res(request):
    data = request.body.decode('utf-8')
    res = json.loads(data)
    return res


## TODO 补充ID池
def full_project_id(request):
    for ids in range(10000000,10005000):
        id = project_id_pool()
        id.project_id = ids
        id.save()
    return HttpResponse('成功添加')


## TODO 判断分数
def judge_score(star):
    stars = int(star)
    if stars == 1:
        score = 100
    elif stars == 2:
        score = 300
    elif stars == 3:
        score = 500
    elif stars == 4:
        score = 1000
    else:
        score = 2000
    return score

def judge_level(scores):
    if scores <= 1000:
        return 1
    elif scores <=3000:
        return 2
    elif scores <= 10000:
        return 3
    elif scores <= 20000:
        return 4
    else:
        return 5


## TODO 增加任务函数
def project_add(request):
    # try:
        res = get_res(request)
        publisher_id = res['publisher_id']
        project_name = res['project_name']
        project_type = res['project_type']
        description = res['description']
        due_time = res['due_time']
        pay_per_task = res['pay_per_task']
        task_num = res['task_num']
        sample_document = request.FILES['sample_document']
        sample_type = sample_document.name.split('.').pop()
        project_star = request['project_star']
        p = Project()
        id = project_id_pool.objects.first()
        project_id = id.project_id
        p.project_id = project_id
        id.delete()
        write_data(sample_document, project_id+'.'+sample_type, project_id)
        p.publisher_id = publisher_id
        p.project_type = project_type
        p.task_num = task_num
        p.project_status = 0
        p.payment_per_task = pay_per_task
        p.due_time = due_time
        p.completed_task_num = 0
        p.description = description
        p.project_name = project_name
        p.project_star = project_star
        # p.sample_document = sample_document
        p.save()
        for i in range(1,task_num+1):
            t = Task()
            t.project_id = project_id
            t.task_id = project_id+'_'+str(i)
            t.score = judge_score(project_star)
            # t.original_data = sample_document
            t.due_time = due_time
            t.task_status = 0
        data = {'code':200,'msg':'添加任务成功'}
    # except BaseException:
    #     data = {'code':404,'msg':'添加任务失败'}
        return JsonResponse(data)


## TODO 删除任务函数
def project_delete(request):
    # try:
        res = get_res(request)
        project_id = res['project_id']
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
        res = get_res(request)
        project_id = res['project_id']
        project_name = res['project_name']
        description = res['description']
        due_time = res['due_time']
        # pay_per_task = request.GET['pay_per_task']
        if Project.objects.filter(project_id=project_id).exist():
            p = Project.objects.get(project_id=project_id)
            p.project_name = project_name
            p.description = description
            p.due_time = due_time
            # p.payment_per_task = pay_per_task
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
        res = get_res(request)
        keyword = res['keyword']
        t = Project.objects.get(project_id=keyword)
        info = t.to_dict()
        data = {'code': 200, 'msg': '查询成功', 'task_info':info}
    # except BaseException:
    #     data = {'code': 404, 'msg': '查询失败','task_info':''}
        return JsonResponse(data)


def write_data(data, name, project_id):
    destination = f'..../upload/sample_document/{project_id}/'+ name
    if os.path.exists(destination):
        os.remove(destination)
    with open(destination,'wb+') as f:
        for chunk in data.chunks():
            f.write(chunk)
    r = zipfile.ZipFile(name,'r')
    for file in r.namelist():
        r.extract(file)



## TODO 预付款
def prepay(request):
    res = get_res(request)
    project_id = res('project_id',None)
    prepay_amount = res('prepay_amount',None)
    account_id = request.session['user']['account_id']
    w = Wallet.objects.get(account_id=account_id)
    if w.account_num > prepay_amount:
        w.account_num -= prepay_amount
        w.save()
        p = Prepay()
        p.prepay_amount = prepay_amount
        p.prepay_balance = prepay_amount
        p.project_id = project_id
        p.account_id=account_id
        p.save()
        return JsonResponse({'code': 200})
    else:
        return JsonResponse({'code':404})


## TODO 标注者接收任务
def get_task(request):
    res = get_res(request)
    project_id = res['project_id']
    account_id = res['user']['account_id']
    tasks = Task.objects.filter(Q(project_id=project_id)|Q(task_status=0))
    Project.objects.get(project_id=project_id).project_status = 1
    task_num = tasks.count()
    if task_num >=1:
        task = tasks.first()
        task.task_status = 1
        task.save()
        ta = Task_association()
        ta.task_id = task.task_id
        ta.account_id = account_id
        ta.project_id = project_id
        ta.save()
        return JsonResponse({'code': 200})
    else:
        return JsonResponse({'code':404})


## TODO 标注者取消任务
def give_up_task(request):
    res = get_res(request)
    account_id = request.session['user']['account_id']
    task_id = res['task_id']
    ta = Task_association.objects.filter(Q(account_id=account_id)|Q(task_id=task_id))
    ta.delete()
    t = Task.objects.get(task_id=task_id)
    t.task_status = 0
    t.save()
    return JsonResponse({'code': 200})


## TODO 标注者提交任务
def commit_task(request):
    res = get_res(request)
    processed_data = request.FILES['processed_data']
    task_id = res['task_id']
    type = processed_data.name.split('.').pop()
    project_id = task_id.split('.')[0]
    write_data(processed_data,task_id+'.'+type,project_id)
    t = Task.objects.get(task_id=task_id)
    t.task_status = 2
    t.save()
    return JsonResponse({'code': 200})


## TODO task提交成功后付款与升级
def completed_task(request):
    res = get_res(request)
    task_id = res['task_id']
    project_id = task_id.split('_')[0]
    t = Task.objects.get(task_id=task_id)
    ta = Task_association.objects.get(task_id=task_id)
    account_id = ta.account_id
    c = Consumer.objects.get(account_id=account_id)
    p = Project.objects.get(project_id=project_id)
    pre = Prepay.objects.get(project_id=project_id)
    w = Wallet.objects.get(account_id=account_id)
    r = Reward_record()
    web = Web_account()
    web.task_id = task_id
    t.task_status = 3
    t.save()
    r.reward_amount = p.payment_per_task
    r.ta_id = ta.ta_id
    r.reward_time = datetime.datetime.now()
    r.save()
    pre.prepay_balance -= p.payment_per_task
    pre.save()
    t.completed_task_num += 1
    t.save()
    w.account_num += float(p.payment_per_task)*0.8
    web.PAF_time = datetime.datetime.now()
    web.PAF_amount = float(p.payment_per_task)*0.2
    web.PAF_type = p.project_type
    web.PAF_balance += web.PAF_amount
    web.save()
    w.save()
    c.experience += t.score
    c.level = judge_level(c.experience)
    c.save()
    if p.task_num == p.completed_task_num:
        p.project_status = 2
        p.save()