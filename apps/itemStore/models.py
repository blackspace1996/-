# _*_coding:utf-8_*_
from django.db import models
from apps.log.views import logInfoset
# Create your models here.


class ItemInfo(models.Model):
    company = models.ForeignKey("company.CompanyInfo", on_delete=models.CASCADE, verbose_name=u"所属公司编号")
    itemName = models.CharField(max_length=20, verbose_name=u"投入品名称")
    itemDescription = models.CharField(max_length=999, verbose_name=u"投入品描述", null=True)

    class Meta:
        verbose_name = "投入品种类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.itemName

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
            message = self.itemName,
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
            message = self.itemName,
            objecttable=self.__class__.__name__
        )


class ItemCostInfo(models.Model):
    item = models.ForeignKey('ItemInfo', on_delete=models.DO_NOTHING, verbose_name=u"种类")
    costDescription = models.CharField(max_length=999, verbose_name=u"描述", null=True)
    costBatch = models.ForeignKey('productionManagement.SowInfo', on_delete=models.CASCADE, verbose_name=u"使用批次")
    member = models.ForeignKey('company.MemberInfo', on_delete=models.DO_NOTHING, verbose_name=u'负责员工')
    recorder = models.ForeignKey('users.UserProfile', on_delete=models.DO_NOTHING, verbose_name=u'记录人员')
    date = models.DateField(verbose_name=u"使用时间", null=True)
    isNormal = models.BooleanField(default=True, verbose_name=u"状态")
    hashWords = models.CharField(max_length=256, verbose_name=u"hash")
    timeStrap = models.BinaryField(null=True, verbose_name=u"时间戳")

    class Meta:
        verbose_name = "投入品交易"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.item.itemName

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
            message =self.item.itemName+'投入品信息',
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
            message =self.item.itemName+'投入品信息',
            objecttable=self.__class__.__name__
        )