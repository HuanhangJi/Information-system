from django.urls import path
from .views import *


urlpatterns = [
    path('api/pro_login/', pro_login,name='pro_login'), #pro登陆
    path('api/con_login/', con_login,name='con_login'), #con登陆
    path('api/pro_register/', pro_register,name='pro_register'), #pro注册
    path('api/con_register/', con_register,name='con_register'),#con注册
    path('api/logout/', logout,name='logout'),#注销
    path('api/full_user_id/', full_user_id,name='full_user_id'),#补充id池
    path('api/upload_avatar/',upload_avatar,name='upload_avatar'),#上传头像
    path('api/set_payment_password/',set_payment_password,name='set_payment_password'),#设置支付密码
    path('api/change_wallet/',change_wallet,name='change_wallet')#钱包转账体现
    # path('admin',admin_login,name='admin'),#后台，不做后台另说
    # path('admin/pro/add',pro_add,name='pro_add'),
    # path('admin/pro/del',pro_del,name='pro_del'),
    # path('admin/pro/query',pro_query,name='pro_query'),
]
