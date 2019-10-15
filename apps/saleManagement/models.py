from django.db import models

from apps.productionStore.models import StoreInfo
from apps.users.models import UserProfile
from apps.company.models import MemberInfo, CompanyInfo
from apps.rawProduction.models import RawProductionManagement
from apps.log.views import logInfoset
# Create your models here.


class SaleInfo(models.Model):
    saleName = models.CharField(max_length=20, verbose_name=u'销售名称')
    saleBatch = models.ForeignKey("productionStore.StoreInfo", on_delete=models.CASCADE, verbose_name=u"销售批次")
    buyer = models.CharField(max_length=100, verbose_name=u"购买方")
    amount = models.FloatField(default=0, verbose_name=u"售出数量")
    saleTips = models.CharField(max_length=999, null=True, verbose_name=u"销售备注")
    saleMember = models.ForeignKey("company.MemberInfo", on_delete=models.DO_NOTHING, verbose_name=u"负责人")
    saleTime = models.DateField(verbose_name=u"售出时间")
    recorder = models.ForeignKey("users.UserProfile", on_delete=models.DO_NOTHING, verbose_name=u"记录人")
    isNormal = models.BooleanField(default=True, verbose_name=u"数据状态是否正常")
    hashWords = models.CharField(max_length=256, verbose_name=u"hash数据")
    TimeStrap = models.BinaryField(verbose_name=u'时间戳', default='')

    class Meta:
        verbose_name = "销售信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.saleBatch.batch.harvestBatch.sowingName

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
            message =self.saleName+'销售信息',
            objecttable=self.__class__.__name__
        )

