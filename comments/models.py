from django.db import models

# Create your models here.

class Comment(models.Model):
    name = models.CharField(max_length=100,verbose_name="评论者")
    email = models.EmailField(max_length=255,verbose_name="Email地址")
    url = models.URLField(blank=True)
    text = models.TextField(verbose_name="评论")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="评论时间")

    article= models.ForeignKey('article.Article',blank=True,null=True,verbose_name="所属文章")
    #独立文章 与 一般文章 共用一套评论，所以增加一个外键
    independentarticle= models.ForeignKey('independentarticle.Independentarticle',blank=True,null=True,verbose_name="所属独立文章")

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '所有评论'

 
    def __str__(self):
        return self.text[:20]


    
