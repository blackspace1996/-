# _*_ coding:utf-8 _*_
# _*_ coding:utf-8 _*_
from django import forms


class ItemAddForm(forms.Form):
    itemName = forms.CharField(required=True, max_length=20, error_messages={
        'required': u'请填写 投入品名称',
        'max_length': u'投入品名称最大长度为20'
    })




