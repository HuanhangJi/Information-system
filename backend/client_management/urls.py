from django.urls import path
from .views import *


urlpatterns = [
    path('api/pro_login/', pro_login,name='pro_login'), #pro登陆
    path('api/con_login/', con_login,name='con_login'), #con登陆
    path('api/pro_register/', pro_register,name='pro_register'), #pro注册
    path('api/con_register/', con_register,name='con_register'),#con注册
    path('api/logout/', logout,name='pro_logout'),#注销
    path('api/full_user_id/', full_user_id,name='full_user_id'),#补充id池
    path('api/upload_avatar/<int:account_id>/<int:usertype>',upload_avatar,name='upload_avatar'),#上传头像
    path('api/withdraw_wallet/',withdraw_wallet,name='withdraw_wallet'), #钱包转账
    path('api/recharge_wallet/', recharge_wallet, name='recharge_wallet'), #钱包充值
    path('api/change_user_info/',user_change,name='change_user_info'), #用户信息修改
    path('api/get_wallet_info/',wallet_info,name='get_wallet_info'),#用户信息修改
    path('admin_login/',admin_login,name='admin'),#后台，不做后台另说
    # path('admin/pro/del',pro_del,name='pro_del'),
    # path('admin/pro/query',pro_query,name='pro_query'),
]
