from django.contrib import admin
from users.models import UserExt
# Register your models here.
# 后台管理 登录用户信息

class UserAdmin(admin.ModelAdmin):
    #列表展示的字段信息
    list_display = ('realname','user','nickname','telephone','logintime',)
    #搜索索引  外键不能直接引用 + “__” + 外键具体字段
    search_fields = ('realname',)

admin.site.register(UserExt,UserAdmin)

