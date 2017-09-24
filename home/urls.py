#encoding: utf-8

from django.conf.urls import url

from . import views


urlpatterns = [
   #url(r'^$', views.index, name='index'),
   url(r'^$', views.IndexView.as_view(), name='index'), #基于类的 通用视图

]
