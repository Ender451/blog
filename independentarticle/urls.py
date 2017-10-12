#encoding: utf-8

from django.conf.urls import url

from . import views

app_name='independentarticle'
urlpatterns = [
   url(r'(?P<id>\d+)/$', views.detail, name='detail'),      # 文章详情
]
