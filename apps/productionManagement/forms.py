# _*_ coding:utf-8 _*_
# _*_ coding:utf-8 _*_
from django import forms


class SowingAddForm(forms.Form):
    sowingName = forms.CharField(required=True, max_length=20, error_messages={
        'required': u'请填写 批次别名',
        'max_length': u'单位名称最大长度为20'
    })


class ConfirmingMeasureForm(forms.Form):
    confirmingMember = forms.CharField(required=True, max_length=20, error_messages={
        'required': u'请填写 确认人',
        'max_length': u'确认人名称最大长度为20'
    })

