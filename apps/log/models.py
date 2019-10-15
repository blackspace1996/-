

# Create your models here.

from django.db import models
from apps.users.models import UserProfile
from django.contrib.contenttypes.models import ContentType


class OperateLog(models.Model):
    objecttable=models.CharField(max_length=30, null=True,verbose_name=u'操作表格')
    objectID = models.IntegerField(null=True,verbose_name=u'操作对象')
    user = models.ForeignKey(UserProfile, verbose_name='操作用户',on_delete=models.SET_NULL,null=True)
    actiontime =models.DateTimeField(auto_now=True,verbose_name=r'操作时间')
    action = models.IntegerField(null=True,choices=((1, u"添加"), (2, u"删除"), (3, u"更改")))
    ipaddress=models.GenericIPAddressField(blank=True,null=True,verbose_name=u'IP地址')
    message = models.CharField(max_length=30, null=True,verbose_name=u'详细信息')




