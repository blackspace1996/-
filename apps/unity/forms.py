# _*_ coding:utf-8 _*_
# _*_ coding:utf-8 _*_
from django import forms


class UnityAddForm(forms.Form):
    unityName = forms.CharField(required=True, max_length=20, error_messages={
        'required': u'请填写联盟名称',
        'max_length': u'联盟名称最大长度为20'
    })
    unityProfile = forms.CharField(required=True, max_length=30, error_messages={
        'required': u'请填写联盟描述',
        'max_length' : u'联盟简介最大长度为30'
    })
