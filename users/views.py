from django.shortcuts import render

# Create your views here.

from django.views.generic import View
from django.contrib.auth.models import User

from .models import UserExt

import datetime
from django.utils import timezone
from django.http import JsonResponse,HttpResponse


from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings

class RegisterView(View):


    def post(self,request,*args,**kwargs):
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        email = request.POST.get('email','')
        
        nickname = request.POST.get('nickname','')
        realname = nickname
        print("nickname:",nickname)

        user = User.objects.create_user(username=username,password=password,email=email)
        validkey = UserExt.gen_validkey()
        user_ext = UserExt.objects.create(user=user,realname=realname,birthday=datetime.date(1945,1,1),\
                                         nickname=nickname,avatar='default',telephone='',logintime=timezone.now(),validkey=validkey)

        return JsonResponse({'status': 200})


    def get(self,request,*args,**kwargs):
        username = request.GET.get('username','')
        password = request.GET.get('password','')
        email = request.GET.get('email','')

        user = User.objects.create_user(username=username,password=password,email=email)
        validkey = UserExt.gen_validkey()
        user_ext = UserExt.objects.create(user=user,realname='',birthday=datetime.date(1945,1,1),\
                                         nickname='',avatar='default',telephone='',logintime=timezone.now(),validkey=validkey)

        content = '<a href="http://blog.guozhongyuan.cn/user/active/?username={username}&validkey={validkey}"> 点击此处进行激活  </a>'
        send_mail('User Register',content.format(username=username,validkey=validkey),settings.EMAIL_HOST_USER,[email])



        return JsonResponse({'status': 200})




class ActiveView(View):

    def get(self,request,*args,**kwargs):

        username = request.GET.get('username','')
        validkey = request.GET.get('validkey','')
      
        print(username,validkey)
        user = User.objects.get(username=username)

        try:
            if user.userext.status == 0 and user.userext.validkey != '':
                if user.userext.validkey == validkey:
                   user.userext.status = 1
                   user.userext.validkey = ''
                   user.userext.save()
                   return HttpResponse("激活成功")
                else:
                   return HttpResponse("验证码不正确")

            return HttpResponse("用户已经激活")

        except ObjectDoesNotExist as e:

            pass

        #跳转到页面显示：
        return HttpResponse("用户不存在")



