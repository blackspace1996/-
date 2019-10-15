# _*_ coding:utf-8 _*_
# _*_ coding:utf-8 _*_
from django import forms


class CompanyAddForm(forms.Form):
    companyName = forms.CharField(required=True, max_length=20, error_messages={
        'required': u'请填写 公司名称',
        'max_length': u'单位名称最大长度为20'
    })
    companyRegisterNumber = forms.CharField(required=True, max_length=18, error_messages={
        'required': u'请填写 企业注册码',
        'max_length': u'企业注册码最大长度为18'
    })
    telephone = forms.CharField(required=True, max_length=11, error_messages={
        'required': u'请填写 企业热线',
        'max_length': u'企业热线最大长度为11'
    })
    legalPersonName = forms.CharField(required=True, max_length=10, error_messages={
        'required': u'请填写 企业法人',
        'max_length': u'法人名字最大允许长度为10'
    })
    legalPersonPhone = forms.CharField(required=True, max_length=11, error_messages={
        'required': u'请填写 法人联系方式',
        'max_length': u'法人联系方式最大长度为11'
    })
    amountOfProStoreHouse = forms.IntegerField(required=True, error_messages={
        'required': u'请填写 产品仓库数量',
        'invalid': u'产品仓库数量 请输入一个整数'
    })
    amountOfItemStoreHouse = forms.IntegerField(required=True, error_messages={
        'required': u'请填写 投入品仓库数量',
        'invalid': u'投入品仓库数量 请输入一个整数'
    })
    joiningDate = forms.DateField(required=True, error_messages={
        'required': u'请填写 加入日期',
    })
    unityID = forms.IntegerField(required=True, error_messages={
        'required':u'请选择公司所属联盟'
    })


class MemberAddForm(forms.Form):
    memberName = forms.CharField(required=True, error_messages={
        'required': u'请填写 公司名称',
    })
    position = forms.CharField(required=True, error_messages={
        'required': u'请填写 员工职位'
    })
    telephone = forms.CharField(required=True, error_messages={
        'required': u'请填写 员工联系方式'
    })
    hireDate = forms.DateField(required=True, error_messages={
        'required': u'请填写 受聘时间'
    })


class EquipmentAddForm(forms.Form):
    equipmentName = forms.CharField(required=True, max_length=20, error_messages={
        'required': u'请填写 设备名称',
        'max_length': u'设备名称应当小于20个字符'
    })
    amount = forms.IntegerField(required=True, error_messages={
        'required': u'请填写 设备数量',
        'invalid': u'请填写 一个整数'
    })


class BlockAddForm(forms.Form):
    blockName = forms.CharField(required=True, max_length=20, error_messages={
        'required': u'请填写 地块名称',
        'max_length': u'地块名称应当小于20个字符'
    })
    blockSquare = forms.IntegerField(required=True, error_messages={
        'required': u'请填写 地块面积',
        'invalid': u'请填写 一个整数'
    })
    unit = forms.CharField(required=True, max_length=10, error_messages={
        'required': u'请选择单位'
    })
    soilInfo = forms.CharField(required=True, max_length=200, error_messages={
        'required': u'请填写 土壤信息',
        'max_length': u'土壤信息应当小于200个字符'
    })

