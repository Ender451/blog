#encoding: utf-8

from django.conf.urls import url

from .views import RegisterView,ActiveView


urlpatterns = [
   #url(r'^$', views.index, name='index'),
   url(r'^register/', RegisterView.as_view(), name='register'), #基于类的 注册用户  
   url(r'^active/', ActiveView.as_view(),name='active'),        #         激活用户
]
