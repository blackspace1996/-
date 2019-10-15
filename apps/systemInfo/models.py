# _*_coding:utf-8_*_
from django.db import models
from apps.log.views import logInfoset
from apps.users.models import UserProfile
from apps.unity.models import UnityInfo
# Create your models here.


class SysNews(models.Model):
    title = models.CharField(max_length=20, verbose_name=u"动态标题")
    description = models.CharField(max_length=2000, verbose_name=u"动态内容")
    createTime = models.DateTimeField(verbose_name=u"发布时间", auto_now_add=True)
    updateTime = models.DateTimeField(verbose_name=u"修改时间", auto_now=True)
    unity = models.ForeignKey(UnityInfo,on_delete=models.CASCADE,null=True)


    class Meta:
        verbose_name = "系统动态"
        verbose_name_plural = verbose_name
        ordering = ['-createTime']

    def __str__(self):
        return self.title

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
            message ='《'+self.title+'》系统动态',
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
            message ='《'+self.title+'》系统动态',
            objecttable=self.__class__.__name__
        )


class SysRegulations(models.Model):
    regName = models.CharField(max_length=20, verbose_name=u"规章制度")
    regDescription = models.CharField(max_length=2000, verbose_name=u"制度详情")
    createTime = models.DateTimeField(verbose_name=u"发布时间", auto_now_add=True)
    updateTime = models.DateTimeField(verbose_name=u"修改时间", auto_now=True)
    unity = models.ForeignKey(UnityInfo, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "规章制度"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.regName

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
            message ='《'+self.regName+'》规章制度',
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
            message='《' + self.regName + '》规章制度',
            objecttable=self.__class__.__name__
        )



