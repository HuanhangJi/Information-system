from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='index'), #主页路由
    path('assignments', assignments, name='assignments')#任务市场路由
]
