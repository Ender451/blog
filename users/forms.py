#encoding: utf-8

from django import forms

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate


from .models import UserExt

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput,error_messages={'required':'用户名不能为空'})
    password = forms.CharField(widget=forms.PasswordInput,error_messages={'required':'密码不能为空'})
    password2 = forms.CharField(widget=forms.PasswordInput,required=False)
    email = forms.EmailField(error_messages={'required':'邮箱不能为空','invalid':'邮箱格式不正确'})

    def clean_username(self):
        username = self.cleaned_data.get('username','')
        if len(username) < 6 or len(username) > 16:
            raise forms.ValidationError('用户名必须为6位到16位')
        try:
            User.objects.get(username=username)
            raise forms.ValidationError('用户名已经存在')
        except ObjectDoesNotExist as e:
            pass

        return username

    def clean_password(self):
        password = self.cleaned_data.get('password','')
        if len(password) < 6 or len(password) > 32:
            raise forms.ValidationError('密码必须为6到32位')

        return password

    def clean_email(self):
        password = self.cleaned_data.get('password','')
        password2 = self.cleaned_data.get('password2','')

        if password != password2:
            raise forms.ValidationError('两次密码不一致')

        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email','')
        #username = self.cleaned_data.get('username','')
        try:
            User.objects.get(email=email)
            #User.objects.filter(email=email,username=username)
            #print('user:',user)
            raise forms.ValidationError('邮箱已注册1')
        except ObjectDoesNotExist as e:
            #raise forms.ValidationError('邮箱已注册2')
            pass

        return email


class LoginForm(forms.Form):
    username = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cached_user = None

    def clean(self):
        #cleaned_data = super(LoginForm, self).clean() python 2.7
        cleaned_data = super().clean()
        username = cleaned_data.get('username', '')
        password = cleaned_data.get('password', '')

        if username == '' or password == '':
            raise forms.ValidationError("用户或密码不正确")
        else:
            # user = authenticate(username=username, password=password)
            user = None
            try:
                user = User.objects.get(username=username)
            except ObjectDoesNotExist as e:
                try:
                    user = User.objects.get(email=username)
                except ObjectDoesNotExist as e:
                    pass

            if user and user.check_password(password):
                if user.userext.status == 1:
                    self.cached_user = user
                elif user.userext.status == 0:
                    #发送激活邮件
                    raise form.ValidationError("用户未激活，请查收邮件重新激活")
                    pass
            else:
                raise forms.ValidationError("用户或密码不正确")

        return cleaned_data



class ResetPasswordForm(forms.Form):
    username = forms.CharField(required=False)
    email = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cached_user = None

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username', '')
        email = cleaned_data.get('email', '')

        if username == '' or email == '':
            raise forms.ValidationError("用户名或邮箱错误")

        try:
            user = User.objects.get(username=username, email=email)
            if user.userext.status != 1:
                raise forms.ValidationError("用户不可用, 请联系管理员")

            self.cached_user = user
        except ObjectDoesNotExist as e:
            raise forms.ValidationError("用户名或邮箱错误")

        return cleaned_data




class ResetPasswordConfirmForm(forms.Form):
    username = forms.CharField(widget=forms.HiddenInput, required=False)
    validkey = forms.CharField(widget=forms.HiddenInput, required=False)
    password = forms.CharField(widget=forms.PasswordInput, error_messages={'required' : '密码不能为空'})
    password2 = forms.CharField(widget=forms.PasswordInput, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cached_user = None

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username', '')
        validkey = cleaned_data.get('validkey', '')

        if username == '' or validkey == '':
            raise forms.ValidationError("用户名或验证码错误")

        try:
            user = User.objects.get(username=username)
            if user.userext.status != 1:
                raise forms.ValidationError("用户不可用, 请联系管理员")

            # if user.userext.validkey !='' or user.userext.validkey != validkey:
            if user.userext.validkey != validkey:
                raise forms.ValidationError("用户名或验证码错误")

            self.cached_user = user
        except ObjectDoesNotExist as e:
            raise forms.ValidationError("用户名或验证码错误")

        return cleaned_data

    def clean_password(self):
        password = self.cleaned_data.get('password', '')
        if len(password) < 6 or len(password) > 32:
            raise forms.ValidationError('密码必须为6位到32位')
        return password

    def clean_password2(self):
        password = self.cleaned_data.get('password', '')
        password2 = self.cleaned_data.get('password2', '')
        if password != password2:
            raise forms.ValidationError('两次密码不一致')

        return password2




class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, error_messages={'required' : '原密码不能为空'})
    password = forms.CharField(widget=forms.PasswordInput, error_messages={'required' : '密码不能为空'})
    password2 = forms.CharField(widget=forms.PasswordInput, required=False)

    def __init__(self, user, *args, **kwargs):
        #super().__init__(*args, **kwargs)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password', '')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('原密码不正确')
        return old_password


    def clean_password(self):
        password = self.cleaned_data.get('password', '')
        if len(password) < 6 or len(password) > 32:
            raise forms.ValidationError('密码必须为6位到32位')
        return password

    def clean_password2(self):
        password = self.cleaned_data.get('password', '')
        password2 = self.cleaned_data.get('password2', '')
        if password != password2:
            raise forms.ValidationError('两次密码不一致')

        return password2



class UserExtBaseForm(forms.ModelForm):
    sex = forms.ChoiceField(widget=forms.RadioSelect, choices=[(1, '男'), (0, '女')])
    
    class Meta:
        model = UserExt
        fields = ['realname', 'nickname', 'birthday', 'telephone', 'sex']
        labels = {
            'realname' : '真实名称',
            'nickname' : '昵称',
            'birthday' : '出生日期',
            'telephone' : '电话号码',
            'sex' : '性别',
        }
        widgets = {
        }
        error_messages = {
            'realname' : {
                'required' : '真实名称不能为空'
            }
        }
        help_texts = {
            'realname' : '您的真实名称'
        }

    def clean_realname(self):
        realname = self.cleaned_data.get('realname', '')
        if len(realname) > 10:
            raise forms.ValidationError('真实名称不能大于10个字符串')

        return realname




class UserExtAvatarForm(forms.ModelForm):
    avatar = forms.ImageField(label='头像', error_messages={'invalid_image' : '请输入正确头像'})
    class Meta:
        model = UserExt
        fields = ['avatar']


