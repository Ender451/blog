# coding:utf-8
from django.db import models

from django.contrib.auth.models import User
from django.urls import reverse

import markdown
from django.utils.html import strip_tags
# Create your models here.

class Category(models.Model):
    #分类名称
    name = models.CharField(max_length=50,verbose_name="分类名称")

    class Meta:
        verbose_name = '独立文章分类名称'
        verbose_name_plural = '独立文章分类名称'

    def __str__(self):
        return self.name

    def get_article_num(self):
        num= Category.objects.filter(article__category__name=self.name).count()
        return num 


class Tag(models.Model): 
    #名称 
    name = models.CharField(max_length=50,verbose_name="标签名称")
    
    #admin界面中Tag项目显示的名称
    class Meta: 
        verbose_name = '独立文章标签名称'
        verbose_name_plural = '独立文章标签名称'
    
    #admin界面中每个项目显示自己的name
    def __str__(self):
        return self.name

class Independentarticle(models.Model):
    #文章标题
    title = models.CharField(max_length=70,verbose_name="文章标题")
    #文章内容
    body = models.TextField(verbose_name="文章内容",default='')
    #创建时间
    create_time = models.DateTimeField(verbose_name="创建时间")
    #修改时间
    modified_time = models.DateTimeField(verbose_name="修改时间")
    #摘要
    excerpt = models.CharField(max_length=200,blank=True,verbose_name="摘要")
    #分类
    category = models.ForeignKey(Category,verbose_name="分类")
    #标签
    tags = models.ManyToManyField(Tag,blank=True,verbose_name=u"标签")
    #作者
    author = models.ForeignKey(User,verbose_name="作者")
    #浏览量
    views = models.PositiveIntegerField(default=0, verbose_name="浏览量")


    class Meta:
        verbose_name = '独立文章'
        verbose_name_plural = '独立文章'
        #默认排序
        ordering=['-create_time']

    #自动生成摘要
    def save(self,*args,**kwargs):
        if not self.excerpt:
            
            md= markdown.Markdown(
                extensions=[
                           'markdown.extensions.extra',
                           'markdown.extensions.codehilite',
                           ]
                )
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Independentarticle,self).save(*args,**kwargs)


    def __str__(self):
        return self.title



    #定义 get_absolute_url 方法 获取自身的url 
    def get_absolute_url(self):
        # urls.py   中 request 传入的是 id
        # views.py  中 get_object_or_404()函数传入 pk 参数 id
        return reverse('independentarticle:detail',kwargs={'id':self.pk})
        # article --> independentarticle/urls.py app_name=independentarticle
        # detail  --> independentarticle/urls.py name='detail'

    #统计浏览量
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])


