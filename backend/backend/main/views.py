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


def jdzz(request, user_id=0):
    # user_id为0表示未登录
    print(user_id)
    # 根据user_id从数据库调img_url(用户头像的图片)
    context = {'user_id': user_id, 'img_url': '/static/img/6159252dd42a2834f52175724d59cfe014cebf3e.png'}
    return render(request, "index/index.html", context)


# 任务市场
def jdzz_product(request, user_id=0, page=1):
    # 根据user_id从数据库调img_url
    context = {'user_id': user_id, 'img_url': '/static/img/6159252dd42a2834f52175724d59cfe014cebf3e.png'}
    # 从数据库调任务信息
    shangpin_info = {'name1': '文本任务1', 'star1':2.5, 'url1': '/jdzz_shangpin/' + str(user_id) + '/50/',
                     'name2': "文本标注11111"}
    return render(request, "index/product.html", {**context, **shangpin_info})


def jdzz_shangpin(request, task_id, user_id=0):
    # 根据user_id从数据库调img_url
    context = {'user_id': user_id, 'img_url': '/static/img/6159252dd42a2834f52175724d59cfe014cebf3e.png'}
    # 根据task_id从数据库调取task_info
    task_info = {'task_id': task_id, 'biaoti': '微博评论情绪标注', 'fabuzhe': 123, 'renwuhao': task_id,
                 'leixing': '文本', 'nandu': '简单', 'shijian': "2022-03-29 16:14:37", 'star1': 2,
                 'exp': 150, 'jingbi': 150, 'time_guji': '2小时', 'miaoshu': '这是一个文本标注任务' * 100}
    return render(request, "index/shangpin.html", {**context, **task_info})


def work1(request, task_id, page=1, user_id=0):
    context = {'user_id': user_id, 'img_url': '/static/img/6159252dd42a2834f52175724d59cfe014cebf3e.png', 'page_max': 5}
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
        task_info = {'task_id': task_id, 'page': page, 'renwuhao': '8521', 'miaoshu': '请判断以下文字中的情绪', 'jindu': '40'}
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
        task_info = {'task_id': task_id, 'page': page, 'renwuhao': '8522', 'target': '奥特曼之眼', 'jindu': '10',
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