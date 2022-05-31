import math

from django.shortcuts import render
import os
import sys
sys.path.append(os.path.abspath('..'))
from task_management.models import *
from client_management.models import *
from django.core.paginator import *
from django.db.models import Q
from django.http import *
from django.shortcuts import redirect
import json
import os

os.chdir(os.path.abspath(os.path.join(os.getcwd(),'..')))

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

def judge_diff(star):
    stars = int(star)
    if stars<= 1.5:
        score = "很简单"
    elif stars <= 2.5:
        score = "比较简单"
    elif stars <= 3.5:
        score = "中等"
    elif stars <= 4.5:
        score = "比较困难"
    else:
        score = "很困难"
    return score

def judge_time(star):
    stars = int(star)
    if stars<= 1.5:
        score = "10分钟"
    elif stars <= 2.5:
        score = "20分钟"
    elif stars <= 3.5:
        score = "30分钟"
    elif stars <= 4.5:
        score = "45分钟"
    else:
        score = "60分钟"
    return score


def get_avatar(user_id):
    pics = os.listdir('./static/avatar')
    flag = 0
    pid = ''
    for pic in pics:
        if pic.split('.')[0] == str(user_id):
            flag = 1
            pid = pic
            break
    return {'flag':flag,'pid':pid}

def show_avatar(user_id):
    dic = get_avatar(user_id)
    if dic['flag'] == 1:
        context = {'user_id': user_id, 'img_url': f'/static/avatar/{dic["pid"]}'}
    else:
        context = {'user_id': user_id, 'img_url': '/static/avatar/default/default_avatar.jpeg'}
    return context


def jdzz(request, user_id='0'):
    # user_id为0表示未登录
    # 根据user_id从数据库调img_url(用户头像的图片)
    dic = get_avatar(user_id)
    if dic['flag'] == 1:
        context = {'user_id': user_id, 'img_url': f'/static/avatar/{dic["pid"]}'}
    else:
        context = {'user_id': user_id, 'img_url': '/static/avatar/default/default_avatar.jpeg'}
    return render(request, "index/index.html", context)



# 任务市场
def jdzz_product(request, user_id=0, pIndex=1):
    # 根据user_id从数据库调img_url
    context = show_avatar(user_id)
    # 从数据库调任务信息
# try:
    kw = request.GET.get('keyword',None)
    Plist = Project.objects.exclude(project_status=5)
    mywhere = []
    if kw:
        mywhere.append(f'keyword={kw}')
        Plist = Plist.filter(Q(title__contains=kw)|Q(content__contains=kw))
    Plist = Plist.order_by("project_id")
    n = len(Plist)
    if n > 200:
        n = 200
    pIndex = int(pIndex)
    limit = 5
    page = Paginator(Plist,limit)
    max_page = page.num_pages
    if pIndex < 1:
        pIndex = 1
    if pIndex > max_page:
        pIndex = max_page
    Plist2 = page.page(pIndex)
    plist = page.page_range
    content = {'task_list':Plist2,'plist':plist,'pIndex':pIndex,'number':n,'mywhere':mywhere,'limit':limit}
    for i in content['task_list']:
        print(i.project_id)
    print({**context, **content})
    return render(request, "index/product.html", {**context, **content})


def jdzz_shangpin(request, project_id, user_id=0):
    # 根据user_id从数据库调img_url
    context = show_avatar(user_id)
    # 根据task_id从数据库调取task_info
    p = Project.objects.get(project_id=project_id)
    info = p.to_dict()
    h = Producer.objects.get(account_id=info['account_id'])
    task_info = {'task_id': project_id, 'biaoti': info['project_name'], 'fabuzhe': h.nickname,
                 'renwuhao': project_id,
                 'leixing': info['project_type'], 'nandu': judge_diff(info['project_star']),
                 'shijian': info['due_time'], 'star1': info['project_star'],
                 'exp': judge_score(info['project_star']),
                 'jingbi': info['payment_per_task']*0.8*100, 'time_guji': judge_time(info['project_star']), 'miaoshu': info['description']}
    return render(request, "index/shangpin.html", {**context, **task_info})


def work1(request, user_id, task_id, page=1):
    #检查
    ta = Task_association.objects.filter(Q(task_id=task_id),Q(account_id=user_id))
    if not ta.exists():
        return JsonResponse({'info':'无该任务记录'})
    # 根据user_id从数据库调img_url
    context = show_avatar(user_id)
    page_try = request.GET.get('page')
    # 根据task_id和page从数据库调task_info
    if page_try:
        page = int(page_try)
        if page == 1:
            content = '嗷嗷嗷111' * 100
            jindu = '50'
        elif page == 2:
            content = '嗷嗷嗷222' * 100
            jindu = '50'
        elif page == 3:
            content = '嗷嗷嗷333' * 100
            jindu = '70'
        elif page == 4:
            content = '嗷嗷嗷444' * 100
            jindu = '90'
        else:
            content = '任务结束'
            jindu = '100'
        return JsonResponse({'data': {'content': content, 'jindu': jindu, 'new_page': page}})
    else:
        project_id = task_id.split('_')[0]
        task_num = task_id.split('_')[1]
        content = 'AAAAAAAAAA' * 100
        choice_dict = {'choice_1':'开心','choice_2':'生气','choice_3':'难过','choice_4':'其他'}
        path = f'/static/sample_document/{project_id}/{task_num}.txt'
        task_info = {'page_max':100,'task_id': task_id, 'page': page, 'renwuhao':task_id , 'miaoshu': '请判断以下文字中的情绪', 'jindu': '40','content': content,'yaoqiu':'AA就选AA'*20}
        return render(request, "index/work_1.html", {**context, **task_info,**choice_dict})

def work2(request,user_id,task_id,page = 1):
    context = show_avatar(user_id)
    page_try = request.GET.get('page')
    print()
    # 根据task_id和page从数据库调task_info
    ta = Task_association.objects.filter(Q(task_id=task_id), Q(account_id=user_id))
    if not ta.exists():
        return JsonResponse({'info': 'no ta info!'})
    context = show_avatar(user_id)
    project_id = task_id.split('_')[0]
    task_num = task_id.split('_')[1]
    path = f'./static/sample_document/{project_id}'
    pic_list = []
    for item in os.listdir(path):
        try:
            id = item.split('.')[0].split("_")[1]
            if id == task_num:
                pic_list.append(item)
        except:
            pass
    n = len(pic_list)
    p = Project.objects.get(project_id=project_id)
    start = int(p.item_per_task) * (int(task_num) - 1) + 1
    print(f'page_try:{page_try}')
    if page_try:
        jindu = math.floor(float(int(page_try) / n) * 100)
        if jindu > 100:
            jindu = 100
        number = start + int(page_try) - 1
        if number < start:
            number = start
        if number > start + n - 1:
            number = start + n - 1
        img = f'/static/sample_document/{project_id}/{number}_{task_num}.jpg'
        print({'data':{'task_img':img,'jindu':jindu,'new_page':int(page_try),'target': '奥特曼之眼'}})
        return JsonResponse({'data':{'task_img':img,'jindu':jindu,'new_page':int(page_try),'target': '奥特曼之眼'}})
    else:
        img = f'/static/sample_document/{project_id}/{start}_{task_num}.jpg'
        task_info = {'task_id': task_id, 'page': page, 'renwuhao': task_id, 'target': '奥特曼之眼', 'jindu': 0,
                     'task_img': img,'page_max':n+1}
        return render(request, "index/work_2.html",{**context,**task_info})

def work3(request, user_id, task_id, page=1):
    #检查
    ta = Task_association.objects.filter(Q(task_id=task_id),Q(account_id=user_id))
    if not ta.exists():
        return JsonResponse({'info':'无该任务记录'})
    # 根据user_id从数据库调img_url
    context = show_avatar(user_id)
    page_try = request.GET.get('page')
    # 根据task_id和page从数据库调task_info
    if page_try:
        page = int(page_try)
        if page == 1:
            content = '/static/img/1.png'
            jindu = '50'
        elif page == 2:
            content = '/static/img/2.png'
            jindu = '50'
        elif page == 3:
            content = '/static/img/3.png'
            jindu = '70'
        elif page == 4:
            content = '/static/img/4.png'
            jindu = '90'
        else:
            content = '任务结束'
            jindu = '100'
        return JsonResponse({'data': {'content': content, 'jindu': jindu, 'new_page': page}})
    else:
        project_id = task_id.split('_')[0]
        task_num = task_id.split('_')[1]
        content = '/static/img/logo.svg'
        jindu = 0
        choice_dict = {'choice_1':'猫','choice_2':'狗','choice_3':'鸡','choice_4':'钝角'}
        path = f'/static/sample_document/{project_id}/{task_num}.txt'
        task_info = {'task_id': task_id, 'page': page, 'renwuhao':task_id , 'miaoshu': '请为以下图片正确分类', 'jindu': jindu,'content': content,'yaoqiu':'AA就选AA'*20}
        return render(request, "index/work_1.html", {**context, **task_info,**choice_dict})


def work1_post(request):
    data = json.loads(request.body, strict=False)
    choice = data["choice"]
    user_id = data["user_id"]
    task_id = data["task_id"]
    page = data["page"]
    print(choice)
    # if page = page_max:
    #     .....
    return JsonResponse({})


def work2_post(request):
    data = json.loads(request.body, strict=False)
    result = data["result"]
    user_id = data["user_id"]
    task_id = data["task_id"]
    page = data["page"]
    store_data(user_id,task_id,page,result)
    return JsonResponse({})

def work3_post(request):
    data = json.loads(request.body, strict=False)
    choice = data["choice"]
    user_id = data["user_id"]
    task_id = data["task_id"]
    page = data["page"]
    print(choice)
    # if page = page_max:
    #     .....
    return JsonResponse({})


def get_task(request,account_id,project_id):
    if int(account_id) == 0:
        return redirect('http://127.0.0.1:8001')
    try:
        Consumer.objects.get(account_id=account_id)
    except:
        return JsonResponse({'code':402,'msg':'接收者错误'})
    tasks = Task.objects.filter(Q(project_id=project_id),(Q(task_status=0)))
    Project.objects.get(project_id=project_id).project_status = 1
    task_num = tasks.count()
    if task_num >= 1:
        task = tasks.first()
        task.task_status = 1
        id = task.task_id
        task.save()
        ta = Task_association()
        ta.account_id = account_id
        ta.project_id = project_id
        ta.task_id = id
        ta.save()
        return JsonResponse({'code': 200,'task_id':id})
    else:
        return JsonResponse({'code':404,'msg':'网络繁忙'})


def store_data(user_id, task_id, page, result):
    path = f'./static/data/account_{user_id}_task_{task_id}'
    print()
    print(f'page:{page}')
    if not os.path.exists(path):
        os.mkdir(path)
    if os.listdir(path) == []:
        data = {}
        data[str(page)] = result
        with open(f'{path}/data.json','w') as f:
            json.dump(data,f)
    else:
        with open(f'{path}/data.json','r') as f:
            data = json.load(f)
            data[str(page)] = result
        print(f'data:{data}')
        with open(f'{path}/data.json','w') as f:
            json.dump(data,f)
    print()

def commit_task(request, user_id, task_id, page):
    path = f'./static/data/account_{user_id}_task_{task_id}/data.json'
    miss = []
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)
            keys = data.keys()
            for i in range(1, page + 1):
                if str(i) not in keys:
                    miss.append(str(i))
        if miss == []:
            t = Task.objects.get(task_id=task_id)
            t.task_status = 2
            t.save()
            return JsonResponse({'code': 200})
        else:
            miss_data = ' '.join(miss)
            print(miss_data)
            return JsonResponse({'code': 403, 'miss_data': miss_data})
    else:
        return JsonResponse({'code': 404})

