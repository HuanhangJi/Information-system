from django.urls import path
from .views import *

urlpatterns = [
    path('project/add/',project_add,name='project_add'), #增加路由
    path('project/delete/',project_delete,name='project_delete'), #删除路由
    path('project/edit/',project_edit,name='project_edit'), #编辑路由
    path('project/query/',project_query,name='project_query'), #查询路由
]


