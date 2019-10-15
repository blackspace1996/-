# _*_coding:utf-8_*_
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.db.models import Q

from .forms import LoginForm
from apps.taskManagement.models import PersonTaskInfo
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

# Create your views here.


class LoginView(View):
    def get(self, request):
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        login_form = LoginForm(request.POST)
        return render(request, "login.html", {"login_form": login_form, "hashkey": hashkey, "image_url": image_url})

    def post(self, request):
        # 表单验证,LoginForm里的验证项名字应该和表单中的"name"一致
        login_form = LoginForm(request.POST)
        # 是否符合定义,验证后才会生成结果
        if login_form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            if user and user.is_active is True:
                    login(request, user)
                    re = redirect(reverse('userWelcome'))
                    return re
            else:
                hashkey = CaptchaStore.generate_key()
                image_url = captcha_image_url(hashkey)
                login_form = LoginForm(request.POST)
                return render(request, "login.html", {"userError": "用户名或密码错误", "login_form": login_form, "hashkey": hashkey, "image_url": image_url})

        else:
            error = login_form.errors
            hashkey = CaptchaStore.generate_key()
            image_url = captcha_image_url(hashkey)
            login_form = LoginForm(request.POST)
            return render(request, "login.html",
                          {"error": error, "login_form": login_form, "hashkey": hashkey, "image_url": image_url})


class LogoutView(View):
    def get(self, request):
        logout(request)
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        login_form = LoginForm(request.POST)
        return render(request, "login.html", {"login_form": login_form, "hashkey": hashkey, "image_url": image_url})

    def post(self, request):
        pass


class UserWelcomeView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        time_now = timezone.now()  # 输出time_now即为当然日期和时间
        taskNumber = 0
        if request.user.identityClass == 3:
            task = PersonTaskInfo.objects.filter(Q(receiver=request.user) & Q(isRead=False))
            for single in task:
                taskNumber = taskNumber + 1
        return render(request, 'function/base.html', {'time_now': time_now, 'taskNumber': taskNumber})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass
