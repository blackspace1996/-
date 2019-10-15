# _*_coding:utf-8_*_
from django.shortcuts import render
from django.contrib import auth
from django.views.generic.base import View
from django.shortcuts import render_to_response
# Create your views here.


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return render(request, "login.html")


def page_not_found(request, exception):
    # 全局404处理函数
    response = render_to_response('function/404.html')
    response.status_code = 404
    return response


def page_error(request):
    # 全局500处理函数
    response = render_to_response('function/500.html')
    response.status_code = 4500
    return response

