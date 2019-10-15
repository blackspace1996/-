from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UnityInfo(models.Model):
    unityID = models.AutoField(primary_key=True, verbose_name=u"联盟编号")
    unityName = models.CharField(max_length=20 , verbose_name=u'联盟名称')
    unityProfile = models.CharField(max_length=30, null= True, verbose_name=u'联盟简介')

    class Meta:
        verbose_name = "联盟信息"

    def Save(self, request):
        from apps.log.views import logInfoset
        pk = self.unityID
        self.save()
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        logInfoset(
            user=request.user,
            action=pk is None and 1 or 3,
            ipaddress=ip,
            objectID=self.unityID,
            message='“' + self.unityName + '”联盟信息',
            objecttable=self.__class__.__name__
        )

    def Delete(self, request):
        from apps.log.views import logInfoset
        self.delete()
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        logInfoset(
            user=request.user,
            action=2,
            ipaddress=ip,
            objectID=self.unityID,
            message='“' + self.unityName + '”联盟信息',
            objecttable=self.__class__.__name__
        )


