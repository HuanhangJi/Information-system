from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='index'), #主页路由
    path('assignments/<int:pIndex>/', assignments, name='assignments')#任务市场路由
]
