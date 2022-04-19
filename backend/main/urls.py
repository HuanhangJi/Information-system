from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='index'), #主页路由
    path('products/<int:pIndex>/', products, name='products'),#任务市场路由
    path('products/info/<int:project_id>/', product_info, name='product_info')#任务市场路由
]
