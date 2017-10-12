from django.db import models

# Create your models here.

class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    article= models.ForeignKey('article.Article',blank=True,null=True)
    #独立文章 与 一般文章 共用一套评论，所以增加一个外键
    independentarticle= models.ForeignKey('independentarticle.Independentarticle',blank=True,null=True)
 
    def __str__(self):
        return self.text[:20]


    
