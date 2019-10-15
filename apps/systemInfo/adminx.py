# _*_ coding:utf-8 _*_
import xadmin

from .models import SysNews
from .models import SysRegulations


class SysNewsAdmin(object):
    list_display = ['title', 'createTime', 'updateTime']
    search_fields = ['title']
    list_filter = ['createTime', 'updateTime']


class SysRegulationsAdmin(object):
    list_display = ['regName', 'createTime', 'updateTime']
    search_fields = ['regName']
    list_filter = ['createTime', 'updateTime']




xadmin.site.register(SysNews, SysNewsAdmin)
xadmin.site.register(SysRegulations, SysRegulationsAdmin)