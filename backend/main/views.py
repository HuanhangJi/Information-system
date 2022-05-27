from django.shortcuts import render
import os
import sys
sys.path.append(os.path.abspath('..'))
from task_management.models import *
from client_management.models import *
from django.core.paginator import *
from django.db.models import Q
from django.http import *
import json
import os

os.chdir(os.path.abspath(os.path.join(os.getcwd(),'..')))

# ## TODO 主页
# def index(request):
#     # try:
#         return render(request,'index/index.html')
#     # except Exception:
#     #     return HttpResponse('打开主页失败')
#
#
# ## TODO 任务市场
# def products(request, pIndex=1):
#     # try:
#         kw = request.GET.get('keyword',None)
#         Plist = Project.objects
#         mywhere = []
#         if kw:
#             mywhere.append(f'keyword={kw}')
#             Plist = Plist.filter(Q(title__contains=kw)|Q(content__contains=kw))
#         Plist = Plist.order_by("project_id")
#         pIndex = int(pIndex)
#         page = Paginator(Plist,5)
#         try:
#             max_page = page.num_pages
#         except Exception:
#             content = {'task_list': None, 'info':'暂无数据'}
#             return render(request,'index/product.html',content)
#         if pIndex < 1:
#             pIndex = 1
#         if pIndex > max_page:
#             pIndex = max_page
#         Plist2 = page.page(pIndex)
#         plist = page.page_range
#         content = {'task_list':Plist2,'plist':plist,'pIndex':pIndex,'max_page':max_page,'mywhere':mywhere}
#         return render(request,'index/product.html',content)
#     # except Exception:
#     #     return HttpResponse(f'打开任务市场失败')
#
# def product_info(request,project_id):
#     try:
#         p = Project()
#         content = p.objects.get(project_id=project_id).to_dict()
#     except Exception:
#         content = {'info':404}
#     return render(request, 'index/shangpin.html', content)

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
        context = {'user_id': user_id, 'img_url': '/static/avatar/avatar/default/default_avatar.jpeg'}
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
    Plist = Project.objects
    mywhere = []
    if kw:
        mywhere.append(f'keyword={kw}')
        Plist = Plist.filter(Q(title__contains=kw)|Q(content__contains=kw))
    Plist = Plist.order_by("project_id")
    pIndex = int(pIndex)
    page = Paginator(Plist,5)
    max_page = page.num_pages
    if pIndex < 1:
        pIndex = 1
    if pIndex > max_page:
        pIndex = max_page
    Plist2 = page.page(pIndex)
    plist = page.page_range
    content = {'task_list':Plist2,'plist':plist,'pIndex':pIndex,'max_page':max_page,'mywhere':mywhere}
    print(content['task_list'])
    infos = []
    for i in content['task_list']:
        info = i.to_dict()
        shangpin_info = {'name': f'{info["project_name"]}', 'star':f'{info["project_star"]}', 'url': f'/jdzz_shangpin/\
{user_id}/{info["project_id"]}'}
        infos.append(shangpin_info)
        print(shangpin_info['url'])
    print({**context, **{'info':infos}})
    return render(request, "index/product.html", {**context, **{'info':infos}})


def jdzz_shangpin(request, project_id, user_id=0):
    # 根据user_id从数据库调img_url
    context = show_avatar(user_id)
    # 根据task_id从数据库调取task_info
    p = Project.objects.get(project_id=project_id)
    info = p.to_dict()
    h = Producer.objects.get(account_id=info['account_id'])
    h
    if info['project_type'] == 'image_block':
        type_ = '图片标注'
    elif info['project_type'] == 'text_type':
        type_ = '文本标注'
    else:
        return JsonResponse({'code':404})
    task_info = {'task_id': project_id, 'biaoti': info['project_name'], 'fabuzhe': h.nickname,
                 'renwuhao': project_id,
                 'leixing': type_, 'nandu': judge_diff(info['project_star']),
                 'shijian': info['due_time'], 'star1': info['project_star'],
                 'exp': judge_score(info['project_star']),
                 'jingbi': info['payment_per_task']*0.8*100, 'time_guji': judge_time(info['project_star']), 'miaoshu': info['description']}
    return render(request, "index/shangpin.html", {**context, **task_info})


def work1(request, task_id, page=1, user_id=0):
    # 根据user_id从数据库调img_url
    print(user_id)
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
        task_info = {'task_id': task_id, 'page': page, 'renwuhao':task_id , 'miaoshu': '请判断以下文字中的情绪', 'jindu': '40'}
        return render(request, "index/work_1.html", {**context, **task_info})


def work2(request, task_id, page=1, user_id=0):
    context = {'user_id': user_id, 'img_url': '/static/img/6159252dd42a2834f52175724d59cfe014cebf3e.png', 'page_max': 5}
    page_try = request.GET.get('page')
    # 根据task_id和page从数据库调task_info
    if page_try:
        page = int(page_try)
        if page == 1:
            target = '奥特曼之眼1'
            task_img = '/static/img/built.jpeg'
            jindu = '50'
        elif page == 2:
            target = '崔浩然'
            task_img = '/static/img/chr.jpg'
            jindu = '50'
        elif page == 3:
            target = '奥特曼之眼3'
            task_img = '/static/img/3.png'
            jindu = '70'
        elif page == 4:
            target = '奥特曼之眼4'
            task_img = '/static/img/4.png'
            jindu = '90'
        else:
            target = '奥特曼之眼5'
            task_img = '/static/img/5.png'
            jindu = '100'
        return JsonResponse({'data': {'task_img': task_img, 'jindu': jindu, 'new_page': page, 'target': target}})
    else:
        task_info = {'task_id': task_id, 'page': page, 'renwuhao': task_id, 'target': '奥特曼之眼', 'jindu': '10',
                     'task_img': '/static/img/built.jpeg'}
        return render(request, "index/work_2.html", {**context, **task_info})


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
    page = ["page"]
    print(result)
    # if page = page_max:
    #     .....
    return JsonResponse({})

def get_task(request,account_id,project_id):
    tasks = Task.objects.filter(Q(project_id=project_id),(Q(task_status=0)))
    Project.objects.get(project_id=project_id).project_status = 1
    task_num = tasks.count()
    if task_num >=1:
        task = tasks.first()
        task.task_status = 1
        task.save()
        ta = Task_association()
        ta.account_id = account_id
        ta.project_id = project_id
        ta.save()
        return JsonResponse({'code': 200})
    else:
        return JsonResponse({'code':404})

