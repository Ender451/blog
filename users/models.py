from django.db import models

from django.contrib.auth.models import User
# Create your models here.


import os
import hashlib



class UserExt(models.Model):
    user = models.OneToOneField(User,verbose_name="用户名")                              #与User 表 建立一对一关系
    realname = models.CharField(max_length=64,verbose_name="真实姓名")                   # 真实姓名
    birthday = models.DateTimeField(blank=True,verbose_name="生日")                      # 生日
    nickname = models.CharField(max_length=64,blank=True,verbose_name="昵称")            # 昵称
    avatar = models.CharField(max_length=256,blank=True,verbose_name="头像")             # 头像
    telephone = models.CharField(max_length=32,blank=True,verbose_name="电话")           # 电话
    score = models.IntegerField(default=0,verbose_name="积分")                           # 积分
    logintime = models.DateTimeField(verbose_name="登陆时间")                            # 登录时间
    validkey = models.CharField(max_length=256,blank=True,verbose_name="验证key")        # key
    status = models.IntegerField(default=0,verbose_name="账号状态")                      # 状态

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    @classmethod
    def gen_validkey(cls):
        m = hashlib.md5()
        m.update(os.urandom(32))
        #生成一个随机数，并用MD5加密
        return m.hexdigest()

    def __str__(self):
        return self.realname
