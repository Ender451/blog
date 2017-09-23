from django.contrib import admin
from article.models import Article,Category,Tag

# Register your models herea.


class ArticleAdmin(admin.ModelAdmin):
    #列表展示的字段信息
    list_display = ('title','category','getTagsName','author','create_time','views',)
    #搜索索引  外键不能直接引用 + “__” + 外键具体字段
    search_fields = ('title','author__username',)


    #多对多关系的字段获取处理    
    def getTagsName(self,obj):
        tag_name=''
        for tag in obj.tags.all():
            tag_name+=tag.name+' '
        return tag_name
    getTagsName.short_description="标签" #getTagName 函数的描述，后台显示时 显示short_description“标签”



admin.site.register(Article,ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)
