#encoding: utf-8

from django.conf.urls import url

from . import views

app_name='article'
urlpatterns = [
   #url(r'^$', views.articlelist, name='articlelist'),                                  # 已使用分页-不能使用
   url(r'^$', views.ArticlelistView.as_view(), name='articlelist'),                     #ok 与home index 一致  改为 基于类的 通用视图
   url(r'(?P<year>[0-9]{4})/(?P<month>[0-9]){1,2}/$', views.archives, name='archives'),
   #url(r'^category/(?P<pk>\d+)/$', views.category, name='category'),                   # 已使用分页-不能使用
   url(r'^category/(?P<pk>\d+)/$', views.CategoryView.as_view(), name='category'),      # 改为 基于类的 通用视图 catrgory 文章列表
   url(r'^tag/(?P<pk>\d+)/$', views.TagView.as_view(), name='tagurl'),                  # 改为 基于类的 通用视图 tag      文章列表
   url(r'(?P<id>\d+)/$', views.detail, name='detail'),                                  # 文章详情
   #url(r'(?P<id>\d+)/$', views.ArticleDetailView.as_view(), name='detail'),            # xx error
]
