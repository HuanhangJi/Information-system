from django.urls import path
from .views import *


urlpatterns = [
    path('login/pro', pro_login,name='pro_login'), #pro登陆路由
    path('login/con',con_login,name='con_login'), #con登陆路由
    path('register/pro',pro_register,name='pro_register'), #pro注册路由
    path('register/con',con_register,name='con_register'),#con注册路由
    # path('admin',admin_login,name='admin'),#后台，不做后台另说
    # path('admin/pro/add',pro_add,name='pro_add'),
    # path('admin/pro/del',pro_del,name='pro_del'),
    # path('admin/pro/query',pro_query,name='pro_query'),
    # path('admin/pro/edit',pro_edit,name='pro_edit'),
]
