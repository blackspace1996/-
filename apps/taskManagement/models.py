from django.db import models
from apps.log.views import logInfoset
from apps.users.models import UserProfile
from apps.company.models import CompanyInfo, MemberInfo,UnityInfo
# Create your models here.


class CompanyTaskInfo(models.Model):
    taskName = models.CharField(max_length=20, verbose_name=u"公司任务名称")
    taskDescription = models.CharField(max_length=999, verbose_name=u"公司任务描述")
    deadline = models.DateField(verbose_name=u"截止日期")
    recorder = models.ForeignKey(UserProfile, null=True, on_delete=models.CASCADE,verbose_name='发布人')
    unityID = models.ForeignKey(UnityInfo,null=True, on_delete=models.CASCADE, verbose_name=u"所属联盟")

    class Meta:
        verbose_name = "公司任务"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.taskName

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
            message ='“'+self.taskName+'”公司任务',
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
            message ='“'+self.taskName+'”公司任务',
            objecttable=self.__class__.__name__
        )


class CompanyTaskReceiveInfo(models.Model):
    task = models.ForeignKey("CompanyTaskInfo", on_delete=models.CASCADE, verbose_name=u'公司任务')
    receiver = models.ForeignKey("company.CompanyInfo", on_delete=models.CASCADE, verbose_name=u'接受公司')
    receivingTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "任务领取信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.task

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
            message ='“'+self.task.taskName+'”任务领取信息',
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
            message ='“'+self.task.taskName+'”任务领取信息',
            objecttable=self.__class__.__name__
        )

class PersonTaskInfo(models.Model):
    taskName = models.CharField(max_length=20, verbose_name=u"私人任务")
    company = models.ForeignKey('company.CompanyInfo', on_delete=models.CASCADE, verbose_name=u'发布公司')
    receiver = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, verbose_name=u"任务负责人")
    taskDescription = models.CharField(max_length=200, verbose_name=u'私人任务描述')
    isRead = models.BooleanField(verbose_name=u'是否已读')
    deadline = models.DateField(verbose_name=u"截止日期")

    class Meta:
        verbose_name = "私人任务"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.taskName

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
            message ='“'+self.taskName+'”私人任务',
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
            message ='“'+self.taskName+'”私人任务',
            objecttable=self.__class__.__name__
        )


