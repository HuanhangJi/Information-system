from django.urls import path
from .views import *

urlpatterns = [
    path('project/add/',project_add,name='project_add'), #增加任务
    path('project/delete/',project_delete,name='project_delete'), #删除任务
    path('project/edit/',project_edit,name='project_edit'), #编辑任务
    path('project/query/',project_query,name='project_query'), #查询任务
    path('api/full_project_id/',full_project_id,name='full_project_id'),
    path('upload_document/<int:project_id>',write_data,name='upload_document'),
    path('project_management/', project_management, name='project_management'),
    path('task_management/', task_management, name='task_management'),
    path('project_management_update/', project_management_update, name='project_management_update'),
    path('acceptance_check/', acceptance_check, name=' text_acceptance_check'),
    path('give_up_task/', give_up_task, name='give_up_task'),
    path('acceptance_show/', acceptance_show, name='acceptance_show'),
    path('error_append/', error_append, name='error_append'),
    path('get_data/', get_data, name='get_data'),
    path('admin_management/', admin_management, name='admin_management'),
    path('acceptance_admin/', acceptance_admin, name='acceptance_admin'),
    path('admin_change/', admin_change, name='admin_change'),
    path('admin_conclusion/', admin_conclusion, name='admin_conclusion'),
    path('rank_info/', get_rank, name='rank_info'),
]


