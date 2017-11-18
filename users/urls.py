#encoding: utf-8

from django.conf.urls import url

from .views import RegisterView,ActiveView,\
                   LoginView,LogoutView,\
                   ResetPasswordView,ResetPasswordConfirmView, \
                   ModifyPasswordView,ChangePasswordView,\
                   UserExtBaseView,UserExtAvatarView
                                             #导入 views.py 中的 类
 
from . import views                          #引入 views.py 中的 函数

app_name = 'users'
urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.test, name='test'),                         #测试页面
    url(r'^register/', RegisterView.as_view(), name='register'), #基于类的 注册用户  
    url(r'^active/', ActiveView.as_view(),name='active'),        #         激活用户
    url(r'^login/', LoginView.as_view(), name="login"),
    url(r'^logout/', LogoutView.as_view(), name="logout"),
    url(r'^modify_password/', ModifyPasswordView.as_view(), name="modify_password"),
    url(r'^reset_password/', ResetPasswordView.as_view(), name="reset_password"),
    url(r'^reset_password_confirm/', ResetPasswordConfirmView.as_view(), name="reset_password_confirm"),
    url(r'^change_password/', ChangePasswordView.as_view(), name="change_password"),
    url(r'^user_ext_base/', UserExtBaseView.as_view(), name="user_ext_base"),
    url(r'^user_ext_avatar/', UserExtAvatarView.as_view(), name="user_ext_avatar"),
]
