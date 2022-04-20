from django.urls import path
from .views import *

urlpatterns = [
    path('project/add/',project_add,name='project_add'), #增加任务
    path('project/delete/',project_delete,name='project_delete'), #删除任务
    path('project/edit/',project_edit,name='project_edit'), #编辑任务
    path('project/query/',project_query,name='project_query'), #查询任务
]


