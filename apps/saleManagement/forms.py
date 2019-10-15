# _*_ coding:utf-8 _*_
from django import forms


class SaleInfoAddForm(forms.Form):
    saleName = forms.CharField(required=True, max_length=20, error_messages={
        'required': u'请填写 销售名称',
        'max_length': u'名称最大长度为20'
    })
    buyer = forms.CharField(required=True, max_length=100, error_messages={
        'required': u'请填写 购买方',
        'max_length': u'购买方名称最大长度为100'
    })
    amount = forms.FloatField(required=True, error_messages={
        'invalid': u'数量请输入有效数字',
        'required': u'请输入售出数量'
    })
    saleTime = forms.DateField(required=True, error_messages={
        'required': u'请选择售出时间'
    })

