from django.urls import path
from .views import *

urlpatterns = [
    path('project/insert/',insert,name='project_add'), #增加路由
    path('project/delete/',delete,name='project_delete'), #删除路由
    path('project/edit/',edit,name='project_edit'), #编辑路由
    path('project/query/',query,name='project_query'), #查询路由
]


