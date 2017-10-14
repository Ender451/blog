from django.contrib import admin
from comments.models import Comment
# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    #列表展示的字段信息
    list_display = ('name','email','text','create_time','article','independentarticle',)
    #搜索索引
    search_fields = ('name','text',)




admin.site.register(Comment,CommentAdmin)


