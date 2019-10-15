# _*_coding:utf-8_*_
from django.db import models
from apps.log.views import logInfoset
from apps.unity.models import UnityInfo
# Create your models here.




class CompanyInfo(models.Model):
    companyID = models.AutoField(primary_key=True, verbose_name=u"单位编号")
    companyName = models.CharField(max_length=20, verbose_name=u"单位名称")
    companyRegisterNumber = models.CharField(max_length=18, verbose_name=u"企业注册号")
    telephone = models.CharField(max_length=11, default='', verbose_name=u"企业热线")
    legalPersonName = models.CharField(max_length=10, verbose_name=u"企业法人")
    legalPersonPhone = models.CharField(max_length=11, verbose_name=u"法人联系方式")
    amountOfProStoreHouse = models.IntegerField(verbose_name=u"产品仓库数量")
    amountOfItemStoreHouse = models.IntegerField(verbose_name=u"投入品仓库数量")
    superCompany = models.ForeignKey("self", null=True, on_delete=models.SET_NULL, verbose_name=u"上级公司")
    joiningDate = models.DateField(verbose_name=u"加入时间")
    updateTime = models.DateTimeField(auto_now=True, verbose_name=u"修改时间")
    unityID = models.ForeignKey(UnityInfo,on_delete=models.CASCADE,null=True, verbose_name=u"联盟编号")

    class Meta:
        verbose_name = "单位信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.companyName

    def Save(self, request):
        pk = self.companyID
        self.save()
        if 'HTTP_X_FORWARDED_FOR' in request.META:
           ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
           ip = request.META['REMOTE_ADDR']
        logInfoset(
            user=request.user,
            action=pk is None and 1 or 3,
            ipaddress=ip,
            objectID=self.companyID,
            message = '“'+self.companyName+'”单位信息',
            objecttable=self.__class__.__name__
        )

    def Delete(self,request):
        self.delete()
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        logInfoset(
            user=request.user,
            action=2,
            ipaddress=ip,
            objectID=self.companyID,
            message='“' + self.companyName + '”单位信息',
            objecttable=self.__class__.__name__
        )



class MemberInfo(models.Model):
    memberID = models.AutoField(primary_key=True, verbose_name=u"工号")
    companyName = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, verbose_name=u"隶属单位")
    memberName = models.CharField(max_length=10, verbose_name=u"员工姓名")
    position = models.CharField(max_length=10, verbose_name=u"员工职位")
    telephone = models.CharField(max_length=11, verbose_name=u"联系方式")
    hireDate = models.DateField(verbose_name=u"聘用时间")
    updateDate = models.DateTimeField(auto_now=True, verbose_name=u"修改时间")

    class Meta:
        verbose_name = "员工信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.memberName

    def Save(self, request):
        pk=self.memberID
        self.save()
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        logInfoset(
            user=request.user,
            action=pk is None and 1 or 3,
            ipaddress=ip,
            objectID=self.memberID,
            message = '“'+self.memberName+'”员工信息',
            objecttable=self.__class__.__name__
        )

    def Delete(self, request):
        self.delete()
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        logInfoset(
            user=request.user,
            action=2,
            ipaddress=ip,
            objectID=self.memberID,
            message='“' + self.memberName + '”员工信息',
            objecttable=self.__class__.__name__
        )



class FinanceInfo(models.Model):
    description = models.CharField(max_length=15, default="", verbose_name=u"收支明细")
    type = models.CharField(max_length=3, choices=[(0, "支出"), (1, "收入")], verbose_name=u"类型")
    companyID = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, verbose_name=u"所属单位编号")
    memberID = models.ForeignKey(MemberInfo, on_delete=models.CASCADE, verbose_name=u"经办人工号")
    amount = models.IntegerField(verbose_name=u"金额")
    unit = models.CharField(max_length=20, choices=[("yuan", u"元"), ("thousand", u"千元"), ("million", u"百万元")], verbose_name=u"单位")
    payer = models.CharField(max_length=20, verbose_name=u"付款方")
    payee = models.CharField(max_length=20, verbose_name=u"收款方")
    dealDate = models.DateField(verbose_name="交易日期")
    createTime = models.DateField(auto_now_add=True, verbose_name=u"创建时间")
    updateTime = models.DateField(auto_now_add=True, verbose_name=u"修改时间")
    hash = models.CharField(max_length=128, null=True, verbose_name="hash值")

    class Meta:
        verbose_name = "收支记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.description

    def Save(self, request):
        pk=self.id
        self.save()
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        logInfoset(
            user=request.user,
            action=pk is None and 1 or 3,
            ipaddress=ip,
            objectID=self.id,
            message = '“'+self.description+'”收支记录',
            objecttable=self.__class__.__name__
        )


class EquipmentInfo(models.Model):
    equipmentName = models.CharField(max_length=20, verbose_name=u"设备名称")
    companyID = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, verbose_name=u"所属公司编号")
    amount = models.IntegerField(verbose_name=u"数量")
    description = models.CharField(max_length=999, verbose_name=u'备注', default="")
    share = models.BooleanField(verbose_name=u"共享与否", default=False)
    shareCondition = models.CharField(max_length=999, verbose_name=u"共享条件", default='')

    class Meta:
        verbose_name = "设备信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.equipmentName

    def Save(self, request):
        pk=self.id
        self.save()
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        logInfoset(
            user=request.user,
            action=pk is None and 1 or 3,
            ipaddress=ip,
            objectID=self.id,
            message='“'+self.equipmentName+'”设备信息',
            objecttable=self.__class__.__name__
        )

    def Delete(self,request):
        self.delete()
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        logInfoset(
            user=request.user,
            action=2,
            ipaddress=ip,
            objectID=self.id,
            message='“' + self.equipmentName + '”设备信息',
            objecttable=self.__class__.__name__
        )

class BlockInfo(models.Model):
    blockID = models.AutoField(primary_key=True, verbose_name=u"地块编号")
    companyID = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, verbose_name=u"所属公司编号")
    blockName = models.CharField(max_length=20, verbose_name=u"地块别名", default="")
    rawProduction = models.ForeignKey("rawProduction.RawProductionInfo", on_delete=models.CASCADE, null=True, verbose_name=u"种植源产品编号")
    blockSquare = models.IntegerField(verbose_name=u"地块面积")
    unit = models.CharField(max_length=10, choices=[("1", "亩"), ("2", "平方米")])
    soilInfo = models.CharField(max_length=200, verbose_name=u"土壤信息")

    class Meta:
        verbose_name = "地块信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.blockID

    def Save(self, request):
        pk=self.blockID
        self.save()
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        logInfoset(
            user=request.user,
            action=pk is None and 1 or 3,
            ipaddress=ip,
            objectID=self.blockID,
            message='“'+self.blockName+'”地块信息',
            objecttable=self.__class__.__name__
        )

    def Delete(self, request):
        self.delete()
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        logInfoset(
            user=request.user,
            action=2,
            ipaddress=ip,
            objectID=self.blockID,
            message='“' + self.blockName + '”地块信息',
            objecttable=self.__class__.__name__
        )