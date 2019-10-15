# _*_ coding:utf-8 _*_
# _*_ coding:utf-8 _*_
from django import forms


class StoreInfoAddForm(forms.Form):
    amount = forms.FloatField(required=True, error_messages={
        'required': u'请填写 入库数量',
        'invalid': u'仅支持如x.xx的小数点后最多两位的数字'
    })
    unit = forms.CharField(required=True, max_length=20, error_messages={
        'required': u'请填写 入库单位',
        'max_length': u'单位名称长度最多不过20位'
    })
    storeHouse = forms.CharField(required=True, max_length=20, error_messages={
        'required': u'请填写 存储仓库',
        'max_length': u'仓库名称长度不超过20'
    })

