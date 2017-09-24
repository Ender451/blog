#coding:utf-8
#自定义模板标签
from django import template
from ..models import Article , Category ,Tag
from django.db.models.aggregates import Count
register = template.Library()

#文章列表 模板标签
@register.simple_tag
def get_recent_articles(num=5):
    return Article.objects.all().order_by('-create_time')[:num]


#归档 模板标签
@register.simple_tag
def archives():
    return Article.objects.dates('create_time','month',order='DESC')

#分类 模板标签
@register.simple_tag
def get_categories():
    return Category.objects.all()

#标签 模板标签
@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0)



