from django.views import View
from apps.log.models import OperateLog
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def logInfoset(objectID,user,action,ipaddress,message,objecttable):
    logInfo = OperateLog()
    logInfo.user = user
    logInfo.action=action
    logInfo.ipaddress=ipaddress
    logInfo.objectID=objectID
    logInfo.message=message
    logInfo.objecttable=objecttable
    logInfo.save()







class logInfo(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self,request):
        if request.user.identityClass == 0:
            logInfo_list = OperateLog.objects.all()
        else:
            return render(request,"function/no_permissions.html",{})

        if request.GET.get('order') is not None:
            order = int(request.GET.get('order'))
        else:
            order = 2

        if order == 1:
            logInfo_list = logInfo_list.order_by('actiontime')

        else:
            logInfo_list = logInfo_list.order_by('-actiontime')

        paginator = Paginator(logInfo_list, 10)  # 分页器
        page = request.GET.get('page')
        try:
           logInfo_list = paginator.page(page)
        except PageNotAnInteger:
            logInfo_list = paginator.page(1)
        except EmptyPage:
            logInfo_list = paginator.page(paginator.num_pages)

        return render(request,"function/logManagement/logInfo.html",{'logInfo_list':logInfo_list,'order':order})










