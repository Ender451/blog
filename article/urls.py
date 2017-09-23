#encoding: utf-8

from django.conf.urls import url

from . import views

app_name='article'
urlpatterns = [
   url(r'^$', views.articlelist, name='articlelist'),
   url(r'(?P<year>[0-9]{4})/(?P<month>[0-9]){1,2}/$', views.archives, name='archives'),
   url(r'^category/(?P<pk>\d+)/$', views.category, name='category'),
   url(r'(?P<id>\d+)/$', views.detail, name='detail'),
]
