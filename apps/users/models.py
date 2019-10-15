# _*_encoding:utf-8_*_
from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.unity.models import UnityInfo

class UserProfile(AbstractUser):
    holder = models.CharField(max_length=10, verbose_name=u'持有者')
    company = models.ForeignKey("company.CompanyInfo", verbose_name=u"隶属公司", on_delete=models.CASCADE, null=True)
    identityClass = models.IntegerField(null=True, choices=(("0", u"维护员"),("1", u"系统管理员"), ("2", u"系统操作员"), ("3", u"操作员")), verbose_name=u"权限等级")
    employeeID = models.CharField(max_length=20, verbose_name=u'员工编号',null=True)
    identityID = models.CharField(max_length=20, verbose_name=u'身份证号',null=True)
    unityID=models.ForeignKey(UnityInfo,on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.holder

    def Save(self, request):
        from apps.log.views import logInfoset
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
            message ='“'+self.username+'”账号',
            objecttable=self.__class__.__name__
        )
