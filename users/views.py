from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UserForm, UserProfileForm
from .models import EmailVerifyRecord, UserProfile
from utils.email_send import send_register_email


class MyBackend(ModelBackend):
    """自定义认证后端：支持邮箱登录 + 激活状态校验"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                # 校验用户是否激活
                if not user.is_active:
                    return None
                return user
        except User.DoesNotExist:
            return None
        return None


def active_user(request, active_code):
    """激活用户：比对链接中的验证码，设置 is_active = True"""
    all_records = EmailVerifyRecord.objects.filter(code=active_code)
    if all_records:
        for record in all_records:
            email = record.email
            try:
                user = User.objects.get(email=email)
                user.is_active = True
                user.save()
            except User.DoesNotExist:
                return HttpResponse('激活失败：用户不存在')
        return redirect('users:login')
    return HttpResponse('链接无效或已过期，请重新注册')


def register_success(request):
    """注册成功页面"""
    return render(request, 'users/register_success.html')


def login_view(request):
    """登录视图"""
    error_msg = None
    if request.method != 'POST':
        form = LoginForm()
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('users:user_profile')
            else:
                # 区分"账号未激活"和"密码错误"
                try:
                    inactive_user = User.objects.get(Q(username=username) | Q(email=username))
                    if inactive_user.check_password(password):
                        error_msg = '账号尚未激活，请检查邮箱并点击激活链接'
                    else:
                        error_msg = '用户名或密码错误，请重试'
                except User.DoesNotExist:
                    error_msg = '用户名或密码错误，请重试'

    context = {'form': form, 'error_msg': error_msg}
    return render(request, 'users/login.html', context)


def register(request):
    """注册视图"""
    if request.method != 'POST':
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get('password'))
            new_user.username = email
            new_user.is_active = False   # 注册后默认未激活
            new_user.save()

            send_register_email(email, 'register')
            return redirect('users:register_success')

    context = {'form': form}
    return render(request, 'users/register.html', context)


def forget_pwd(request):
    """忘记密码：发送重置邮件"""
    if request.method == 'GET':
        form = ForgetPwdForm()
    elif request.method == 'POST':
        form = ForgetPwdForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                send_register_email(email, 'forget')
                return HttpResponse('密码重置邮件已发送，请查收！')
            else:
                return HttpResponse('该邮箱未注册，请先注册！')

    return render(request, 'users/forget_pwd.html', {'form': form})


def forget_pwd_url(request, active_code):
    """通过邮件链接重置密码"""
    if request.method != 'POST':
        form = ModifyPwdForm()
    else:
        form = ModifyPwdForm(request.POST)
        if form.is_valid():
            record = EmailVerifyRecord.objects.get(code=active_code)
            email = record.email
            user = User.objects.get(email=email)
            user.password = make_password(form.cleaned_data.get('password'))
            # 重置密码时自动激活
            user.is_active = True
            user.save()
            return HttpResponse('密码修改成功！<a href="/users/login/">返回登录</a>')
        else:
            return HttpResponse('密码修改失败，请重试')

    return render(request, 'users/reset_pwd.html', {'form': form})


@login_required(login_url='users:login')
def user_profile(request):
    """用户个人中心"""
    user = User.objects.get(username=request.user)
    return render(request, 'users/user_profile.html', {'user': user})


def logout_view(request):
    """登出"""
    logout(request)
    return redirect('users:login')


@login_required(login_url='users:login')
def editor_users(request):
    """编辑用户信息"""
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        try:
            userprofile = user.userprofile
            form = UserForm(request.POST, instance=user)
            user_profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                user_profile_form.save()
                return redirect('users:user_profile')
        except UserProfile.DoesNotExist:
            form = UserForm(request.POST, instance=user)
            user_profile_form = UserProfileForm(request.POST, request.FILES)
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                new_user_profile = user_profile_form.save(commit=False)
                new_user_profile.owner = request.user
                new_user_profile.save()
                return redirect('users:user_profile')
    else:
        try:
            userprofile = user.userprofile
            form = UserForm(instance=user)
            user_profile_form = UserProfileForm(instance=userprofile)
        except UserProfile.DoesNotExist:
            form = UserForm(instance=user)
            user_profile_form = UserProfileForm()

    return render(request, 'users/editor_users.html', locals())
