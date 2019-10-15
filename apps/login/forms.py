# _*_ coding:utf-8 _*_
from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(required=True, error_messages={
        'required': u'用户名不能为空'
    })
    password = forms.CharField(required=True, error_messages={
        'required': u'密码不能为空'
    })

    captcha = CaptchaField(required=True, error_messages={
        'required': u'验证码不能为空',
        'invalid': u'验证码错误'
    })
