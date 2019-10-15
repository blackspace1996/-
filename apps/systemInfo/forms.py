# _*_ coding:utf-8 _*_
from django import forms


class NewsAddForm(forms.Form):
    NewsTitle = forms.CharField(required=True, max_length=20,error_messages={
        'required': u'动态标题不能为空',
        'max_length': u'标题最大长度为20'
    })
    NewsDescription = forms.CharField(required=True, max_length=2000, error_messages={
        'required': u'动态内容不能为空',
        'max_length': u'内容最大长度为2000'
    })


class RegsAddForm(forms.Form):
    RegsTitle = forms.CharField(required=True, error_messages={
        'required': u'制度名称不能为空'
    })
    RegsDescription = forms.CharField(required=True, max_length=2000, error_messages={
        'required': u'制度内容不能为空',
        'max_length': u'内容最大长度为2000'
    })
