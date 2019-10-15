# _*_ coding:utf-8 _*_
# _*_ coding:utf-8 _*_
from django import forms


class IncomeAddForm(forms.Form):
    incomeAmount = forms.IntegerField(required=True, error_messages={
        'required': u'请填写 收入金额',
        'invalid': u'请输入正确格式的收入金额'
    })
    incomeTime = forms.DateField(required=True, error_messages={
        'required': u'请填写 收入时间',
        'invalid': u'请输入正确格式的日期'
    })


class CostAddForm(forms.Form):
    costAmount = forms.IntegerField(required=True, error_messages={
        'required': u'请填写 花销金额',
        'invalid': u'请输入正确格式的花销金额'
    })
    costTime = forms.DateField(required=True, error_messages={
        'required': u'请填写 花销时间',
        'invalid': u'请输入正确格式的日期'
    })
