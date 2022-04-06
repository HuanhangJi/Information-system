from django.shortcuts import render
from django.http import *
from task_management.models import Task
from django.core.paginator import *
from django.db.models import Q

## TODO 主页
def index(request):
    try:
        content = {'info':'成功打开主页'}
        return render(request,'index/index.html',content)
    except Exception:
        return HttpResponse('打开主页失败')


## TODO 任务市场
def assignments(request, pIndex=1):
    try:
        kw = request.GET.get('keyword',None)
        Tlist = Task.objects
        mywhere = []
        if kw:
            mywhere.append(f'keyword={kw}')
            try:#在任务类建立后删除
                Tlist = Task.objects.filter(Q(title__contains=kw)|Q(content__contains=kw))
            except:
                pass
        pIndex = int(pIndex)
        page = Paginator(Tlist,5)
        try:
            max_page = page.num_pages
        except Exception:
            content = {'task_list': None, 'info':'暂无数据'}
            return render(request,'index/product.html',content)
        if pIndex < 1:
            pIndex = 1
        if pIndex > max_page:
            pIndex = max_page
        Tlist2 = page.page(pIndex)
        plist = page.page_range
        content = {'task_list':Tlist2,'plist':plist,'pIndex':pIndex,'max_page':max_page,'mywhere':mywhere,'info':'成功打开任务市场'}
        return render(request,'index/product.html',content)
    except Exception:
        return HttpResponse(f'打开任务市场失败')