# _*_ coding:utf-8 _*_
from django import forms


class CompanyTaskAddForm(forms.Form):
    taskName = forms.CharField(required=True, max_length=20, error_messages={
        'required': u'请填写 任务名称',
        'max_length': u'任务名称最大长度为20'
    })
    taskDescription = forms.CharField(required=True, max_length=999, error_messages={
        'required': u'请填写 任务描述',
        'max_length': u'任务描述最大长度为999'
    })
    deadline = forms.DateField(required=True, error_messages={
        'required': u'请填写 截止日期'
    })


class PersonTaskAddForm(forms.Form):
    taskName = forms.CharField(required=True, max_length=20, error_messages={
        'required': u'请填写 任务名称',
        'max_length': u'任务名称最大长度为20'
    })

    receiver = forms.CharField(required=True , max_length=20, error_messages={
        'required': u'请选择 接受人/负责人'
    })

    taskDescription = forms.CharField(required=True, max_length=999, error_messages={
        'required': u'请填写 任务描述',
        'max_length': u'任务描述最大长度为999'
    })
    deadline = forms.DateField(required=True, error_messages={
        'required': u'请填写 截止日期'
    })