from django.urls import path
from . import views

urlpatterns = [
    path('', views.jdzz),  # 欢迎页
    path('jdzz/<int:user_id>/', views.jdzz),  # 欢迎页
    path('jdzz_product/<int:user_id>/<int:pIndex>/', views.jdzz_product),  # 任务市场页
    path('jdzz_shangpin/<int:user_id>/<int:task_id>/', views.jdzz_shangpin),  # 商品详情页
    path('jdzz_work1/<int:user_id>/<int:task_id>/', views.work1),  # 文字工作台
    path('jdzz_work2/<int:user_id>/<int:task_id>/', views.work2),  # 图片工作台
    path('jdzz_work1_post/', views.work1_post),  # 接收文字的标注结果
    path('jdzz_work2_post/', views.work2_post),  # 接收图片的标注结果
    # path('testview', views.post1, name='testview'),  #Ajax加载工作台内容
    # path('',index,name='index'), #主页
    # path('products/<int:pIndex>/', products, name='products'),#任务市场
    # path('products/info/<int:project_id>/', product_info, name='product_info')#任务详情
]
