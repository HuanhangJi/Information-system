from django.shortcuts import render
import os
import sys
sys.path.append(os.path.abspath('..'))
from task_management.models import *
from client_management.models import *
from django.core.paginator import *
from django.db.models import Q
from django.http import *


## TODO 主页
def index(request):
    # try:
        return render(request,'index/index.html')
    # except Exception:
    #     return HttpResponse('打开主页失败')


## TODO 任务市场
def products(request, pIndex=1):
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
        try:
            max_page = page.num_pages
        except Exception:
            content = {'task_list': None, 'info':'暂无数据'}
            return render(request,'index/product.html',content)
        if pIndex < 1:
            pIndex = 1
        if pIndex > max_page:
            pIndex = max_page
        Plist2 = page.page(pIndex)
        plist = page.page_range
        content = {'task_list':Plist2,'plist':plist,'pIndex':pIndex,'max_page':max_page,'mywhere':mywhere}
        return render(request,'index/product.html',content)
    # except Exception:
    #     return HttpResponse(f'打开任务市场失败')

def product_info(request,project_id):
    try:
        p = Project()
        content = p.objects.get(project_id=project_id).to_dict()
    except Exception:
        content = {'info':404}
    return render(request, 'index/shangpin.html', content)
