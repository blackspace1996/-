# _*_coding:utf-8_*_
from django.db import models
from apps.company.models import CompanyInfo
from apps.log.views import logInfoset
# Create your models here.


class RawProductionInfo(models.Model):
    rawProductionName = models.CharField(max_length=10, verbose_name=u"源产品名称")
    description = models.CharField(max_length=500, null=True, verbose_name=u"备注")
    company = models.ForeignKey(CompanyInfo, on_delete=models.DO_NOTHING, verbose_name=u"所属公司")
    createTime = models.DateTimeField(verbose_name=u"发布时间", auto_now_add=True)
    updateTime = models.DateTimeField(verbose_name=u"修改时间", auto_now=True)

    class Meta:
        verbose_name = "源产品信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.rawProductionName

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
            message =self.rawProductionName+'源产品信息',
            objecttable=self.__class__.__name__
        )

class RawProductionManagement(models.Model):
    rawProductionName = models.ForeignKey(RawProductionInfo, on_delete=models.CASCADE, verbose_name=u"品种")
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, verbose_name=u'隶属公司', null=True)
    qualityControlMeasure = models.CharField(max_length=20, verbose_name=u"措施简称", default='')
    measureDescription = models.CharField(max_length=500, verbose_name=u'措施详情', default='')
    orderNumber = models.IntegerField(default=0, verbose_name=u'序号')
    createTime = models.DateTimeField(verbose_name=u"发布时间", auto_now_add=True)
    updateTime = models.DateTimeField(verbose_name=u"修改时间", auto_now=True)
    flag = models.BooleanField(verbose_name=u"是否追溯", default=False)

    class Meta:
        verbose_name = "源产品质量管理措施"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s' % (self.rawProductionName, self.qualityControlMeasure)

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
            message =self.rawProductionName.rawProductionName+'源产品质量管理措施',
            objecttable=self.__class__.__name__
        )