from django.db import models

from apps.rawProduction.models import RawProductionInfo, RawProductionManagement
from apps.company.models import BlockInfo, MemberInfo
from apps.users.models import UserProfile
from apps.productionManagement.models import SowInfo
from apps.log.views import logInfoset
# Create your models here.


class StoreInfo(models.Model):
    batch = models.ForeignKey("productionManagement.HarvestInfo", on_delete=models.CASCADE, verbose_name=u"批次")
    storeTips = models.CharField(max_length=999, verbose_name=u"入库备注", null=True)
    storeTime = models.DateField(auto_now_add=True, verbose_name=u"入库时间")
    amount = models.FloatField(verbose_name=u"入库总数量")
    unit = models.CharField(max_length=20, verbose_name=u"数量单位")
    storeHouse = models.CharField(max_length=20, verbose_name=u"存储仓库")
    restAmount = models.FloatField(verbose_name=u"剩余数量")
    storeMember = models.ForeignKey("company.MemberInfo", on_delete=models.DO_NOTHING, verbose_name=u"负责员工")
    recorder = models.ForeignKey("users.UserProfile", on_delete=models.DO_NOTHING, verbose_name=u"记录人")
    isNormal = models.BooleanField(default="True", verbose_name=u"是否正常")
    hashWords = models.CharField(max_length=256, verbose_name=u"hash文字")
    storingPeriod = models.IntegerField(default=0, verbose_name=u"存储时间")

    class Meta:
        verbose_name = "入库信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.batch.harvestBatch.sowingName

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
            message = self.batch.harvestBatch.sowingName+'入库信息',
            objecttable=self.__class__.__name__
        )

