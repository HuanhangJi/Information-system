from django.urls import path
from .views import *
urlpatterns = [
    path('',index,name='index'),
    path('login/pro', login_pro,name='login_pro'), #pro登陆路由，
    path('login/con',login_con,name='login_con'), #con登陆路由
    path('register/pro',pro_register,name='pro_register'), #pro注册路由
    path('register/con',con_register,name='con_register') #con注册路由
]
