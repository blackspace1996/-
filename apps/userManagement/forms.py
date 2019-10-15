# _*_ coding:utf-8 _*_
# _*_ coding:utf-8 _*_
from django import forms


class UsersAddForm(forms.Form):
    username = forms.CharField(required=True, error_messages={
        'required': u'用户名不能为空',
    })
    password = forms.CharField(required=True, min_length=8, error_messages={
        'required': u'密码不能为空',
        'min_length': u'密码最小长度为8'
    })
    holder = forms.CharField(required=True, max_length=10, error_messages={
        'required': u'账号持有者不能为空',
        'max_length': u'持有者名称长度不能超过10个字符'
    })
    company = forms.CharField(required=True, error_messages={
        'required': u'请指定本账号所隶属的公司'
    })


