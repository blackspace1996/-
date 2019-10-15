# _*_ coding:utf-8 _*_
import xadmin

from .models import CompanyInfo
from .models import MemberInfo
from .models import FinanceInfo
from .models import EquipmentInfo


class CompanyInfoAdmin(object):
    list_display = ['companyName', 'joiningDate', 'telephone']
    search_fields = ['companyName', 'legalPersonName', 'telephone']
    list_filter = ['companyName', 'legalPersonName', 'telephone', 'joiningDate']


class MemberInfoAdmin(object):
    pass


class FinanceInfoAdmin(object):
    pass


class EquipmentInfoAdmin(object):
    pass


xadmin.site.register(CompanyInfo, CompanyInfoAdmin)
xadmin.site.register(MemberInfo, MemberInfoAdmin)
xadmin.site.register(FinanceInfo, FinanceInfoAdmin)
xadmin.site.register(EquipmentInfo, EquipmentInfoAdmin)
