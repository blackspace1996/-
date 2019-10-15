from django.db import models

from apps.rawProduction.models import RawProductionInfo, RawProductionManagement
from apps.company.models import BlockInfo, MemberInfo
from apps.users.models import UserProfile
from apps.log.views import logInfoset
# Create your models here.


class SowInfo(models.Model):
    sowingName = models.CharField(max_length=20, verbose_name=u"名称")
    sowingTime = models.DateField(auto_now_add=True, verbose_name=u"播种时间")
    sowingTips = models.CharField(max_length=999, verbose_name=u"播种备注")
    sowingCompany = models.ForeignKey("company.CompanyInfo", on_delete=models.CASCADE,
                                      verbose_name=u"播种公司",)
    sowingProduction = models.ForeignKey("rawProduction.RawProductionInfo", on_delete=models.CASCADE,
                                         verbose_name=u"播种产品")
    sowingBlock = models.ForeignKey("company.BlockInfo", on_delete=models.CASCADE,
                                    verbose_name=u"播种地块")
    sowingMember = models.ForeignKey("company.MemberInfo", on_delete=models.CASCADE,
                                     verbose_name=u"播种人")
    recorder = models.ForeignKey("users.UserProfile", on_delete=models.CASCADE,
                                 verbose_name=u"记录人")
    hashWords = models.CharField(max_length=256, verbose_name=u"记录hash")

    isNormal = models.BooleanField(default="True", verbose_name=u"是否正常")

    isHarvest = models.BooleanField(default="False", verbose_name=u"是否收获")

    class Meta:
        verbose_name = "播种信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sowingName

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
            message = '“'+self.sowingName+'”播种信息',
            objecttable=self.__class__.__name__
        )

    def Save(self, request):
        self.save()
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        logInfoset(
            user=request.user,
            action=2,
            ipaddress=ip,
            objectID=self.id,
            message = '“'+self.sowingName+'”播种信息',
            objecttable=self.__class__.__name__
        )

class MeasureConfirmingInfo(models.Model):
    company = models.ForeignKey("company.CompanyInfo", on_delete=models.CASCADE,
                                verbose_name=u"公司")
    rawProduction = models.ForeignKey("rawProduction.RawProductionInfo", on_delete=models.CASCADE,
                                      verbose_name=u"品种")
    measure = models.ForeignKey("rawProduction.RawProductionManagement", on_delete=models.CASCADE,
                                verbose_name=u"环节")
    sowingBatch = models.ForeignKey("SowInfo", on_delete=models.CASCADE,
                                    verbose_name=u"播种批次")

    isConfirming = models.BooleanField(verbose_name=u"是否确认", default=False)

    confirmingTips = models.CharField(max_length=999, verbose_name=u"确认备注", default='')

    confirmingTime = models.DateField(null=True, verbose_name=u"确认时间")

    confirmingMember = models.CharField(max_length=20, verbose_name=u'确认人', default='')

    recorder = models.ForeignKey("users.UserProfile", on_delete=models.CASCADE,
                                 verbose_name=u"记录者", null=True)

    hashWords = models.CharField(max_length=256, verbose_name=u"记录hash", default='')

    isNormal = models.BooleanField(default="True", verbose_name=u"是否正常")

    class Meta:
        verbose_name = "播种信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.measure.qualityControlMeasure

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
            message = self.company.companyName+'播种信息',
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
            objectID=self.id,
            message = self.company.companyName+'播种信息',
            objecttable=self.__class__.__name__
        )


class HarvestInfo(models.Model):
    harvestBatch = models.ForeignKey("SowInfo", on_delete=models.CASCADE, verbose_name=u"名称", null=True, default='')
    harvestTime = models.DateField(auto_now_add=True, verbose_name=u"收获时间")
    harvestTips = models.CharField(max_length=999, verbose_name=u"收获备注", null=True)
    harvestCompany = models.ForeignKey("company.CompanyInfo", on_delete=models.CASCADE,
                                       verbose_name=u"收获公司")
    harvestMember = models.ForeignKey("company.MemberInfo", on_delete=models.CASCADE,
                                      verbose_name=u"收获人")
    recorder = models.ForeignKey("users.UserProfile", on_delete=models.CASCADE,
                                 verbose_name=u"记录人")
    hashWords = models.CharField(max_length=256, verbose_name=u"记录hash")

    isNormal = models.BooleanField(default="True", verbose_name=u"是否正常")

    isStore = models.BooleanField(default="False", verbose_name=u"是否入库")

    class Meta:
        verbose_name = "确认信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.harvestBatch

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
            message = self.harvestBatch.sowingName+'确认信息',
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
            objectID=self.id,
            message = self.harvestBatch.sowingName+'确认信息',
            objecttable=self.__class__.__name__
        )
