#encoding: utf-8

from django.conf.urls import url

from .views import RegisterView,ActiveView   #导入 views.py 中的 类
from . import views                          #引入 views.py 中的 函数

urlpatterns = [
   #url(r'^$', views.index, name='index'),
   url(r'^$', views.test, name='test'),                         #测试页面
   url(r'^register/', RegisterView.as_view(), name='register'), #基于类的 注册用户  
   url(r'^active/', ActiveView.as_view(),name='active'),        #         激活用户
]
