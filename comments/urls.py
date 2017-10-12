# coding:utf-8
from django.conf.urls import url

from . import views

app_name='comments'
urlpatterns =[
    url(r'^comment/article/(?P<article_pk>[0-9]+)/$',views.article_comment,name='article_comment'),                       #一般文章的评论提交
    url(r'^comment/independentarticle/(?P<article_pk>[0-9]+)/$',views.independentarticle_comment,name='independentarticle_comment'), #独立文章的评论提交
]
