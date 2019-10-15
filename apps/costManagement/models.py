from django.db import models

from apps.users.models import UserProfile
from apps.company.models import CompanyInfo
from apps.log.views import logInfoset
# Create your models here.


class CostInfo(models.Model):
    costName = models.CharField(max_length=99, verbose_name=u'花销名称', null=True)
    costCompany = models.ForeignKey("company.CompanyInfo", on_delete=models.DO_NOTHING, verbose_name=u"花销公司")
    costType = models.CharField(max_length=10, choices=(
        ('food', '餐饮'), ('purchase', '采购'), ('waterCharge', '水费'), ('electricCharge', '电费'),
        ('salary', '工资'), ('rest', '其他')), verbose_name=u'花销种类')
    costTips = models.CharField(max_length=999, null=True, verbose_name=u'花销备注')
    costAmount = models.IntegerField(verbose_name=u'花销金额')
    recorder = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, verbose_name=u'记录人')
    costTime = models.DateField(verbose_name=u"花销时间")
    isNormal = models.BooleanField(default=True, verbose_name=u"是否正常")
    hashWords = models.CharField(max_length=256, verbose_name=u"hash")

    class Meta:
        verbose_name = "支出信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.costName

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
            message = self.costName,
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
            message = self.costName,
            objecttable=self.__class__.__name__
        )

class IncomeInfo(models.Model):
    incomeName = models.CharField(max_length=99, verbose_name=u'收入名称', null=True)
    incomeCompany = models.ForeignKey("company.CompanyInfo", on_delete=models.DO_NOTHING, verbose_name=u"收入公司")
    incomeType = models.CharField(max_length=10, choices=(
        ('sale', '销售'), ('subsidy', '补贴'), ('rest', '其他')), verbose_name=u'收入种类')
    incomeTips = models.CharField(max_length=999, null=True, verbose_name=u'收入备注')
    incomeAmount = models.IntegerField(verbose_name=u'收入金额')
    incomeTime = models.DateField(verbose_name=u"收入时间")
    recorder = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, verbose_name=u'记录人')
    isNormal = models.BooleanField(default=True, verbose_name=u"是否正常")
    hashWords = models.CharField(max_length=256, verbose_name=u"hash")

    class Meta:
        verbose_name = "收入信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.incomeName

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
            message = self.incomeName,
            objecttable=self.__class__.__name__
        )

