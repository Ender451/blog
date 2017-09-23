from django.db import models

# Create your models here.

class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    article= models.ForeignKey('article.Article')
 
    def __str__(self):
        return self.text[:20]


    
