import datetime
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

def refresh_data(project_list):
    pass

# 任务市场
def jdzz_product(request, user_id=0, pIndex=1):
    # 根据user_id从数据库调img_url
    context = show_avatar(user_id)
    # 从数据库调任务信息
# try:
    kw = request.GET.get('sousuo','')
    money = request.GET.get('caidan2', '所有报酬')
    type_ = request.GET.get('caidan1', '所有类型')
    star = request.GET.get('caidan3', '所有星级')
    Plist = Project.objects.exclude(project_status=6)
    now = datetime.datetime.now()
    for item in Plist:
        if now>item.start_time.replace(tzinfo=None):
            item.project_status=1
        if now>item.due_time.replace(tzinfo=None):
            item.project_status=5
            project_id = item.project_id
            account_id = item.project_id
            w = Wallet.objects.get(account_id=account_id)
            p = Prepay.objects.get(project_id=project_id)
            w.account_num += p.prepay_balance
            w.save()
            p.delete()
        item.save()
    Plist = Plist.exclude(project_status=5)
    Plist = Plist.exclude(project_status=0)
    Plist = Plist.exclude(project_status=10)
    if kw != '':
        Plist = Plist.filter(Q(project_name__contains=kw)|Q(description__contains=kw))
    if money != '所有报酬':
        if money == '5币以下':
            Plist = Plist.filter(payment_per_task__lte=5)
        elif money == '5币~20币':
            Plist = Plist.filter(Q(payment_per_task__gt=5),Q(payment_per_task__lte=20))
        elif money == '20币~50币':
            Plist = Plist.filter(Q(payment_per_task__gt=20),Q(payment_per_task__lte=50))
        elif money == '50币以上':
            Plist = Plist.filter(payment_per_task__gt=50)
        else:
            money = '所有报酬'
    if type_ != '所有类型':
        if type_ == '文本类型标注':
            Plist = Plist.filter(project_type='文本类型标注')
        elif type_ == '图片识别标注':
            Plist = Plist.filter(project_type='图片识别标注')
        elif type_ == '图片类型标注':
            Plist = Plist.filter(project_type='图片类型标注')
        else:
            type_ = '所有类型'
    if star != '所有星级':
        try:
            star_ = int(star[0])
            Plist = Plist.filter(project_star__lte=star_)
        except:
            star = '所有星级'
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
    content = {'task_list':Plist2,'plist':plist,'pIndex':pIndex,'number':n,'sousuo':kw,'limit':limit,
                'caidan1':type_,'caidan2':money,'caidan3':star}
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
                 'jingbi': round(info['payment_per_task']*0.8,1), 'time_guji': judge_time(info['project_star']), 'miaoshu': info['description']}
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
    project_id = task_id.split('_')[0]
    task_num = task_id.split('_')[1]
    p = Project.objects.get(project_id=project_id)
    descreption = p.description
    page_max = p.item_per_task
    path = f'./static/sample_document/{project_id}'
    start = (int(task_num) - 1) * int(page_max)
    count = 0
    if page_try:
        page = int(page_try)
        if page >= page_max+1:
            content = '！！！任务结束，点击下方按钮提交！！！'
            jindu = 100
            return JsonResponse({'data': {'content': content, 'jindu': jindu, 'new_page': page}})
        with open(path+'/total.txt','r',encoding='gb18030') as fp:
            for line in fp:
                if count == start+page-1:
                    content = line
                count += 1
            if count < start+page-1:
                content = '！！任务已经结束，请直接跳转到结尾提交任务！！'
                return JsonResponse({'data': {'content': content, 'jindu': 100, 'new_page': page}})
        jindu = math.floor((page-1)/int(page_max)*100)
        return JsonResponse({'data': {'content': content, 'jindu': jindu, 'new_page': page}})
    else:
        with open(path+'/total.txt','r',encoding='gb18030') as fp:
            for line in fp:
                if count == start:
                    content = line
                    break
                count += 1
        with open(f'{path}/text_tags_{project_id}.txt','r',encoding='utf-8') as fp1:
            for line in fp1:
                choices = line.split(';')[0].split(',')
                break
        choices_num = len(choices)
        choice_dict = {}
        for i in range(choices_num):
            choice_dict[f'choice_{i+1}'] = choices[i]
        task_info = {'new_page':page,'page_max':page_max+1,'task_id': task_id, 'page': page, 'renwuhao':task_id , 'miaoshu': descreption,'jindu': 0,'content': f'{content}'[:-1],'yaoqiu':descreption,'choice_num':choices_num}
        return render(request, "index/work_1.html", {**context, **task_info,**choice_dict})

def work2(request,user_id,task_id,page = 1):
    page_try = request.GET.get('page')
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
    if page_try:
        jindu = math.floor(float(int(page_try) / n) * 100)
        if jindu > 100:
            jindu = 100
        number = start + int(page_try) - 1
        if number < start:
            number = start
        if number > start + n - 1:
            number = start + n - 1
        img = ''
        for pic in pic_list:
            if int(pic.split('_')[0]) == number:
                img = f'/static/sample_document/{project_id}/{pic}'
                break
        return JsonResponse({'data':{'task_img':img,'jindu':jindu,'new_page':int(page_try),'target': p.project_target}})
    else:
        img = ''
        for pic in pic_list:
            if int(pic.split('_')[0]) == start:
                img = f'/static/sample_document/{project_id}/{pic}'
                break
        task_info = {'new_page':page,'task_id': task_id, 'page': page, 'renwuhao': task_id, 'target': p.project_target, 'jindu': 0,
                     'task_img': img,'page_max':n+1}
        return render(request, "index/work_2.html",{**context,**task_info})

def work3(request, user_id, task_id, page=1):
    #检查
    ta = Task_association.objects.filter(Q(task_id=task_id),Q(account_id=user_id))
    if not ta.exists():
        return JsonResponse({'info':'no ta info'})
    # 根据user_id从数据库调img_url
    context = show_avatar(user_id)
    page_try = request.GET.get('page')
    # 根据task_id和page从数据库调task_info
    project_id = task_id.split('_')[0]
    task_num = task_id.split('_')[1]
    p = Project.objects.get(project_id=project_id)
    descreption = p.description
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
    if page_try:
        page = int(page_try)
        jindu = math.floor(float((int(page_try))/n)*100)
        if jindu > 100:
            jindu = 100
        number = start + int(page_try) - 1
        if number < start:
            number = start
        elif number > start + n - 1:
            number = start + n - 1
        img = ''
        for pic in pic_list:
            if int(pic.split('_')[0]) == number:
                img = f'/static/sample_document/{project_id}/{pic}'
                break
        return JsonResponse({'data': {'content': img, 'jindu': jindu, 'new_page': page}})
    else:
        with open(f'{path}/text_tags_{project_id}.txt','r',encoding='utf-8') as fp1:
            for line in fp1:
                choices = line.split(';')[0].split(',')
                break
        choices_num = len(choices)
        choice_dict = {}
        for i in range(choices_num):
            choice_dict[f'choice_{i+1}'] = choices[i]
        img = ''
        for pic in pic_list:
            if int(pic.split('_')[0]) == start:
                img = f'/static/sample_document/{project_id}/{pic}'
                break
        jindu = 0
        print(img)
        task_info = {'page_max':n+1,'new_page':page,'task_id': task_id, 'page': page, 'renwuhao':task_id , 'miaoshu': descreption, 'jindu': jindu,'content': img,'yaoqiu':p.project_target,'choice_num':choices_num}
        return render(request, "index/work_3.html", {**context, **task_info,**choice_dict})


def work1_post(request):
    data = json.loads(request.body, strict=False)
    choice = data["choice"]
    user_id = data["user_id"]
    task_id = data["task_id"]
    page = data["page"]
    store_data_1(user_id, task_id, page, choice)
    return JsonResponse({})


def work2_post(request):
    data = json.loads(request.body, strict=False)
    result = data["result"]
    user_id = data["user_id"]
    task_id = data["task_id"]
    page = data["page"]
    store_data_2(user_id,task_id,page,result)
    return JsonResponse({})

def work3_post(request):
    data = json.loads(request.body, strict=False)
    choice = data["choice"]
    user_id = data["user_id"]
    task_id = data["task_id"]
    page = data["page"]
    store_data_3(user_id, task_id, page, choice)
    return JsonResponse({})

def star_level(star,level):
    if int(star) < int(level)+2:
        i = 1
    else:
        i = 0
    return i



def get_task(request,account_id,project_id):
    try:
        c = Consumer.objects.get(account_id=account_id)
    except:
        return JsonResponse({'code':402,'msg':'接收者错误'})
    tasks = Task.objects.filter(Q(project_id=project_id),(Q(task_status=0)))
    p = Project.objects.get(project_id=project_id)
    status = star_level(p.project_star, c.level)
    if not status:
        return JsonResponse({'code':403,'msg':'标注着等级不足，无法领取任务'})
    p.project_status = 1
    p.save()
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

def store_data_1(user_id, task_id, page, choice):
    path = f'./static/data/account_{user_id}_task_{task_id}'
    project_id = task_id.split('_')[0]
    path2 = f'./static/sample_document/{project_id}/text_tags_{project_id}.txt'
    with open(path2,'r',encoding='utf-8') as f:
        for line in f:
            tags = line.split(';')[0].split(',')
            break
    if not os.path.exists(path):
        os.mkdir(path)
    if os.listdir(path) == []:
        data = {}
        data[str(page)] = tags[int(choice[-1])-1]
        with open(f'{path}/data.json','w') as f:
            json.dump(data,f)
    else:
        with open(f'{path}/data.json','r') as f:
            data = json.load(f)
            data[str(page)] = tags[int(choice[-1])-1]
        with open(f'{path}/data.json','w') as f:
            json.dump(data,f)

def store_data_2(user_id, task_id, page, result):
    path = f'./static/data/account_{user_id}_task_{task_id}'
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
        with open(f'{path}/data.json','w') as f:
            json.dump(data,f)


def store_data_3(user_id, task_id, page, choice):
    path = f'./static/data/account_{user_id}_task_{task_id}'
    project_id = task_id.split('_')[0]
    path2 = f'./static/sample_document/{project_id}/text_tags_{project_id}.txt'
    with open(path2,'r') as f:
        for line in f:
            tags = line.split(';')[0].split(',')
            break
    if not os.path.exists(path):
        os.mkdir(path)
    if os.listdir(path) == []:
        data = {}
        data[str(page)] = tags[int(choice[-1])-1]
        with open(f'{path}/data.json','w') as f:
            json.dump(data,f)
    else:
        with open(f'{path}/data.json','r') as f:
            data = json.load(f)
            data[str(page)] = tags[int(choice[-1])-1]
        with open(f'{path}/data.json','w') as f:
            json.dump(data,f)


def commit_task_2(request, user_id, task_id, page):
    path = f'./static/data/account_{user_id}_task_{task_id}/data.json'
    miss = []
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)
            keys = data.keys()
            for i in range(1, page):
                if str(i) not in keys:
                    miss.append(str(i))
        if miss == []:
            t = Task.objects.get(task_id=task_id)
            t.task_status = 2
            t.save()
            msg = '标注全部提交！'
            return JsonResponse({'code': 200,'msg': msg})
        else:
            miss_data = ' '.join(miss)
            msg = f'{miss_data}页的标注数据未标注！'
            return JsonResponse({'code': 403, 'msg': msg})
    else:
        msg = f'无标注数据'
        return JsonResponse({'code': 404, 'msg': msg})


def commit_task_1(request, user_id, task_id, page):
    path = f'./static/data/account_{user_id}_task_{task_id}/data.json'
    miss = []
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)
            keys = data.keys()
            for i in range(1, page):
                if str(i) not in keys:
                    miss.append(str(i))
        if miss == []:
            t = Task.objects.get(task_id=task_id)
            t.task_status = 2
            t.save()
            msg = '标注全部提交！'
            return JsonResponse({'code': 200,'msg': msg})
        else:
            miss_data = ' '.join(miss)
            msg = f'{miss_data}页的标注数据未标注！'
            return JsonResponse({'code': 403, 'msg': msg})
    else:
        msg = f'无标注数据'
        return JsonResponse({'code': 404, 'msg': msg})

