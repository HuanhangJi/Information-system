from django.urls import path
from .views import *


urlpatterns = [
    path('pro/login', pro_login,name='pro_login'), #pro登陆路由
    path('con/login', con_login,name='con_login'), #con登陆路由
    path('pro/register', pro_register,name='pro_register'), #pro注册路由
    path('con/register', con_register,name='con_register'),#con注册路由
    # path('admin',admin_login,name='admin'),#后台，不做后台另说
    # path('admin/pro/add',pro_add,name='pro_add'),
    # path('admin/pro/del',pro_del,name='pro_del'),
    # path('admin/pro/query',pro_query,name='pro_query'),
    path('pro/logout/', pro_logout,name='pro_logout'),#pro注销路由
    path('con/logout/', con_logout,name='con_logout'),#con注销路由
    path('full.user.id/', full_user_id,name='full_user_id'),
    path('test/',test),
]
