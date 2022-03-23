from django.urls import path
from .views import *

urlpatterns = [
    path('insert/',insert,name='insert'), #增加路由
    path('delete/',delete,name='delete'), #删除路由
    path('edit/',edit,name='edit'), #编辑路由
    path('query/',query,name='query'), #查询路由
]


