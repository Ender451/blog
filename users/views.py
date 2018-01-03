# Create your views here.
import datetime
import json
import os
import time


from django.views.generic import View,FormView
from django.views.generic.base import TemplateResponseMixin

from .models import UserExt
from .forms import RegisterForm,LoginForm,ResetPasswordForm,ResetPasswordConfirmForm,ChangePasswordForm,UserExtBaseForm,UserExtAvatarForm
from .mixins import LoginRequiredMixin

from django.utils import timezone
from django.utils.decorators import method_decorator
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages

from django.db import transaction #事务

from django.conf import settings
from home.models import Visitors


class RegisterView(View):


    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        print('-------------------------------------')
        return self._register(form)


    def _register(self, form):
        if form.is_valid():
            username = form.cleaned_data.get('username', '')
            password = form.cleaned_data.get('password', '')
            email = form.cleaned_data.get('email', '')
            print('======')
            print('username:',username,'password:',password,'email:',email)   
            try:
                with transaction.atomic():
                    user = User.objects.create_user(username=username, password=password, email=email)
                    validkey = UserExt.gen_validkey()
                    user_ext = UserExt.objects.create(user=user, realname='', birthday=datetime.date(1945, 1, 1), \
                                                        nickname=username, avatar='default', telephone='', logintime=timezone.now(), validkey=validkey)
                    content = '欢迎注册[川陀图书馆], 请点击此处进行激活用户: http://blog.guozhongyuan.cn/user/active/?username={username}&validkey={validkey}'.format(username=username, validkey=validkey)
                    send_mail('[川陀图书馆]用户注册', content, settings.EMAIL_HOST_USER, [email])
            except BaseException as e:
                return JsonResponse({'status': 500, 'errors' : ['服务器错误']})
            return JsonResponse({'status': 200})
        else:
            return JsonResponse({'status': 400, 'errors': json.loads(form.errors.as_json()), 'result': ''})




    def get(self,request,*args,**kwargs):
        username = request.GET.get('username','')
        password = request.GET.get('password','')
        email = request.GET.get('email','')
      
        nickname = request.GET.get('nickname','')
        realname = nickname
        print("nickname:",nickname)

        user = User.objects.create_user(username=username,password=password,email=email)  #创建User
        validkey = UserExt.gen_validkey()                                                 #生成一个通过MD5加密的随机字符串作为验证秘钥
                                                                                          #创建与User一一对应的UserExt
        user_ext = UserExt.objects.create(user=user,realname=realname,birthday=datetime.date(1945,1,1),\
                                         nickname=nickname,avatar='default',telephone='',logintime=timezone.now(),validkey=validkey)

        content = '<a href="http://blog.guozhongyuan.cn/user/active/?username={username}&validkey={validkey}"> 点击此处进行激活  </a>'
        send_mail('User Register',content.format(username=username,validkey=validkey),settings.EMAIL_HOST_USER,[email])     #发送验证邮件


        return JsonResponse({'status': 200})




class ActiveView(View):

    def get(self,request,*args,**kwargs):

        username = request.GET.get('username','')
        validkey = request.GET.get('validkey','')
      
        print(username,validkey)
        user = User.objects.get(username=username)

        try:
            if user.userext.status == 0 and user.userext.validkey != '':
                if user.userext.validkey == validkey:   #当验证秘钥吻合，激活用户状态，清空秘钥，激活成功
                   user.userext.status = 1
                   user.userext.validkey = ''
                   user.userext.save()
                   return HttpResponse("激活成功")     
                else:                                   #当验证秘钥失败，返回验证码错误
                   return HttpResponse("验证码不正确")

            return HttpResponse("用户已经激活")         #如果用户状态已经处于激活状态，返回用户已激活

        except ObjectDoesNotExist as e:                 #无法得到正确对应验证信息，返回用户不存在

            pass

        #跳转到页面显示：
        return HttpResponse("用户不存在")



class LoginView2(View):
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.cached_user)
            return JsonResponse({'status' : 200, 'errors' : {}, 'result' : {}})
        else:
            return JsonResponse({'status' : 400, 'errors' : json.loads(form.errors.as_json()), 'result' : {}})



class LoginView(FormView):
    form_class = LoginForm

    def form_valid(self, form):
        login(self.request, form.cached_user)
        print('login ok')
        return JsonResponse({'status' : 200, 'errors' : {}, 'result' : {}})

    def form_invalid(self, form):
        print('login error')
        return JsonResponse({'status' : 400, 'errors' : json.loads(form.errors.as_json()), 'result' : {}})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class ModifyPasswordView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponse('success')
        else:
            return HttpResponse('fail')



class ResetPasswordView(FormView):
    template_name = 'user/reset_password.html'
    form_class = ResetPasswordForm

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = form.cached_user
                validkey = user.userext.gen_validkey()
                user.userext.validkey = validkey
                user.userext.save()
                content = '欢迎来到[川陀图书馆], 请点击此处进行重置用户: http://blog.guozhongyuan.cn/user/reset_password_confirm/?username={username}&validkey={validkey}'.format(username=user.username, validkey=validkey)
                send_mail('[川陀图书馆]用户重置密码', content, settings.EMAIL_HOST_USER, [user.email])
                messages.add_message(self.request, messages.INFO , '重置密码邮件已发送, 请查收邮件进行密码重置')
        except BaseException as e:
            print(e)
            messages.add_message(self.request, messages.ERROR, '重置密码邮件发送失败，请重试')

        return HttpResponseRedirect(reverse('index'))

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form' : form})




class ResetPasswordConfirmView(FormView):
    template_name = 'user/reset_password_confirm.html'
    form_class = ResetPasswordConfirmForm

    def get_initial(self):
        return self.request.GET

    def form_valid(self, form):
        user = form.cached_user
        password = form.cleaned_data.get('password', '')
        user.set_password(password)
        user.save()
        user.userext.validkey = ''
        user.userext.save()
        messages.add_message(self.request, messages.INFO, '重置密码成功，请重新登陆')
        return HttpResponseRedirect(reverse('index'))

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form' : form})


class ChangePasswordView(LoginRequiredMixin, FormView):
    form_class = ChangePasswordForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        password = form.cleaned_data.get('password', '')
        user.set_password(password)
        user.save()
        return JsonResponse({'status' : 200, 'errors' : {}, 'result' : None})

    def form_invalid(self, form):
        return JsonResponse({'status' : 400, 'errors' : json.loads(form.errors.as_json()), 'result' : None})




class UserExtBaseView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'user/user_ext.html'
    form_class = UserExtBaseForm
    form_class_avatar = UserExtAvatarForm

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
                                    'form' : self.form_class(instance=request.user.userext),
                                    'form_avatar' : self.form_class_avatar(instance=request.user.userext),
                                    'nav' : 'avatar'
                                    })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user.userext)
        if form.is_valid():
            model = form.save(commit=False)
            model.save()

        return self.render_to_response({
                                        'form' : form,
                                        'form_avatar' : self.form_class_avatar(instance=request.user.userext),
                                        'nav' : 'base'
                                        })



class UserExtAvatarView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'user/user_ext.html'
    form_class = UserExtBaseForm
    form_class_avatar = UserExtAvatarForm

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
                                    'form' : self.form_class(instance=request.user.userext),
                                    'form_avatar' : self.form_class_avatar(instance=request.user.userext),
                                    'nav' : 'avatar'
                                    })

    def post(self, request, *args, **kwargs):
        form = self.form_class_avatar(data=request.POST, files=request.FILES, instance=request.user.userext)
        if form.is_valid():
            avatar = request.FILES.get('avatar', None)
            if avatar:
                name = '{pk}_{ctime}.{suffix}'.format(pk=request.user.pk, ctime=int(time.time() * 1000), suffix=avatar.name.split('.')[-1])
                path = os.path.join(settings.MEDIA_ROOT, 'avatar', name)
                with open(path, 'wb') as fhandler:
                    for chunk in avatar.chunks():
                        fhandler.write(chunk)

                model = form.save(commit=False)
                model.avatar = name
                model.save()

        return self.render_to_response({
                                        'form' : self.form_class(instance=request.user.userext),
                                        'form_avatar' : form,
                                        'nav' : 'avatar'
                                        })





#test

def test(request):
    sum_num = Visitors.objects.all().count()
    start_num = int(sum_num) - 14
    #访问人数  选取最近14天的数据
    accessdata = Visitors.objects.all().order_by('Visit_day')[start_num:sum_num]
    
    #limit_num =
    context = {
               'accessdata':accessdata
              }   
    return render(request,'user/usertest.html',context)




