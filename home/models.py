from django.db import models

# Create your models here.

class Visitors(models.Model):
    #Visit_day = models.DateField(auto_now_add=True,editable=True,blank=True,verbose_name="日期")
    Visit_day = models.DateField(verbose_name="日期")
    #Visit_time = models.DateTimeField(auto_now_add=True,verbose_name="访问时间")
    Visitors_number = models.PositiveIntegerField(default=0, verbose_name="访问人数")
    
    class Meta:
        verbose_name = '访客统计'
        verbose_name_plural = '访客量统计'
        #默认排序
        ordering=['-Visit_day']

    def __str__(self):
        return str(self.Visit_day)

    #统计浏览量
    def increase_Visitors_number(self):
        self.Visitors_number += 1
        self.save(update_fields=['Visitors_number'])

