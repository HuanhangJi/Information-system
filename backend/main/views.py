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


## TODO 主页
def index(request):
    try:
        content = {'info':'成功打开主页'}
        return render(request,'index/index.html',content)
    except Exception:
        return HttpResponse('打开主页失败')


## TODO 任务市场
def assignments(request):
    try:
        content = {'info':'成功打开任务市场'}
        return render(request,'index/assignments.html',content)
    except Exception:
        return HttpResponse('打开任务市场失败')