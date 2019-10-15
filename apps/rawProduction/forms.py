# _*_ coding:utf-8 _*_
from django import forms


class RawProductionInfoAddForm(forms.Form):
    rawProductionName = forms.CharField(required=True, error_messages={
        'required': u'请填写 品种名称',
    })


class RawProductionMeasureInfoAddForm(forms.Form):
    rawProductionName = forms.CharField(required=True, error_messages={
        'required': u'请选择 品种',
    })
    qualityControlMeasure = forms.CharField(required=True, max_length=20, error_messages={
        'required': u'请填写 措施简称',
        'max_length': u'措施简述最大字符长度为20'
    })
    measureDescription = forms.CharField(required=True, max_length=500, error_messages={
        'required': u'请填写 措施详情',
        'max_length': u'措施详情最大字符长度为500'
    })
