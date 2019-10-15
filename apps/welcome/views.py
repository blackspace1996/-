# _*_coding:utf-8_*_
from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from apps.systemInfo.models import SysNews, SysRegulations
from apps.company.models import CompanyInfo
from apps.unity.models import UnityInfo

import project520.settings

# Create your views here.


class Welcome(View):
    def get(self, request):
        # SysNews_list = SysNews.objects.all()[:9]
        # SysRegs_list = SysRegulations.objects.all()[:15]
        # Company_List = CompanyInfo.objects.all()[:4]
        if request.GET.get('unityID'):
            unityID = int(request.GET.get('unityID'))
            unity = UnityInfo.objects.get(unityID=unityID)
            return render(request,"unity/unity.html", {"unity": unity})
        else:
            unity_list = UnityInfo.objects.all()
            return render(request, "index.html", {"unity_list": unity_list})

    def post(self, request):
        pass


class ListView(View):
    def get(self, request):
        Type = request.GET.get("Type")
        unityID=int(request.GET.get("unityID"))
        unity = UnityInfo.objects.get(unityID=unityID)
        if Type == "News":
            SysNews_list = SysNews.objects.filter(unity=unity)
            if request.GET.get('order') is not None:
                order = int(request.GET.get('order'))
            else:
                order = 2

            if order == 1:
                SysNews_list = SysNews_list.order_by('createTime')

            else:
                SysNews_list = SysNews_list.order_by('-createTime')

            paginator = Paginator(SysNews_list, 10)
            page = request.GET.get('page')
            try:
                customer = paginator.page(page)
            except PageNotAnInteger:
                customer = paginator.page(1)
            except EmptyPage:
                customer = paginator.page(paginator.num_pages)
            return render(request, 'welcome/NewsList.html',
                          {'SysNews_list': customer, 'order': order, 'unity':unity})
        elif Type == "Regs":
            unity = UnityInfo.objects.get(unityID=unityID)
            SysRegs_list = SysRegulations.objects.filter(unity=UnityInfo.objects.get(unityID=unityID))
            if request.GET.get('order') is not None:
                order = int(request.GET.get('order'))
            else:
                order = 2

            if order == 1:
                SysRegs_list = SysRegs_list.order_by('createTime')

            else:
                SysRegs_list = SysRegs_list.order_by('-createTime')

            paginator = Paginator(SysRegs_list, 10)
            page = request.GET.get('page')
            try:
                customer = paginator.page(page)
            except PageNotAnInteger:
                customer = paginator.page(1)
            except EmptyPage:
                customer = paginator.page(paginator.num_pages)
            return render(request, 'welcome/RegsList.html',
                          {'SysRegs_list': customer, 'order': order, 'unity':unity})

        else:
            unity = UnityInfo.objects.get(unityID=unityID)
            Company_list = CompanyInfo.objects.filter(unityID=UnityInfo.objects.get(unityID=unityID))
            if request.GET.get('order') is not None:
                order = int(request.GET.get('order'))
            else:
                order = 2

            if order == 1:
                Company_list = Company_list.order_by('joiningDate')

            else:
                Company_list = Company_list.order_by('-joiningDate')

            paginator = Paginator(Company_list, 10)
            page = request.GET.get('page')
            try:
                customer = paginator.page(page)
            except PageNotAnInteger:
                customer = paginator.page(1)
            except EmptyPage:
                customer = paginator.page(paginator.num_pages)
            return render(request, 'welcome/CompanyList.html',
                          {'CompanyList': customer, 'order': order, 'unity':unity})

    def post(self, request):
        pass


class NewsList(View):
    def get(self, request):
        SysNews_list = SysNews.objects.all()
        if request.GET.get('order') is not None:
            order = int(request.GET.get('order'))
        else:
            order = 2

        if order == 1:
            SysNews_list = SysNews_list.order_by('createTime')

        else:
            SysNews_list = SysNews_list.order_by('-createTime')

        paginator = Paginator(SysNews_list, 10)
        page = request.GET.get('page')
        try:
            customer = paginator.page(page)
        except PageNotAnInteger:
            customer = paginator.page(1)
        except EmptyPage:
            customer = paginator.page(paginator.num_pages)
        return render(request, 'welcome/NewsList.html',
                      {'SysNews_list': customer, 'order': order})


class NewsDetail(View):
    def get(self, request):
        news_id = request.GET.get('id')
        currentNews = SysNews.objects.get(id=news_id)
        count = -1
        news_list = SysNews.objects.all()
        unityID = int(request.GET.get("unityID"))
        unity = UnityInfo.objects.get(unityID=unityID)
        for news in news_list:
            count = count + 1
            if news == currentNews:
                break
        if count == 0:
            previousFlag = ''
        else:
            previousFlag = SysNews.objects.all()[count-1].id

        if count == (len(SysNews.objects.all())-1):
            nextFlag = ''
        else:
            nextFlag = SysNews.objects.all()[count+1].id

        return render(request, "welcome/NewsDetail.html", {"currentNews": currentNews,
                                                           'previousFlag': previousFlag,
                                                           'nextFlag': nextFlag,
                                                           'unity': unity})

    def post(self, request):
        pass


class RegsList(View):
    def get(self, request):
        SysRegs_list = SysRegulations.objects.all()
        if request.GET.get('order') is not None:
            order = int(request.GET.get('order'))
        else:
            order = 2

        if order == 1:
            SysRegs_list = SysRegs_list.order_by('createTime')

        else:
            SysRegs_list = SysRegs_list.order_by('-createTime')

        paginator = Paginator(SysRegs_list, 10)
        page = request.GET.get('page')
        try:
            customer = paginator.page(page)
        except PageNotAnInteger:
            customer = paginator.page(1)
        except EmptyPage:
            customer = paginator.page(paginator.num_pages)
        return render(request, 'welcome/RegsList.html',
                      {'SysRegs_list': customer, 'order': order})

    def post(self, request):
        pass


class RegsDetail(View):
    def get(self, request):
        regs_id = request.GET.get('id')
        currentRegs = SysRegulations.objects.get(id=regs_id)
        count = -1
        regs_list = SysRegulations.objects.all()
        unityID = int(request.GET.get("unityID"))
        unity = UnityInfo.objects.get(unityID=unityID)
        for regs in regs_list:
            count = count + 1
            if regs == currentRegs:
                break
        if count == 0:
            previousFlag = ''
        else:
            previousFlag = SysRegulations.objects.all()[count-1].id

        if count == (len(SysRegulations.objects.all())-1):
            nextFlag = ''
        else:
            nextFlag = SysRegulations.objects.all()[count+1].id

        return render(request, "welcome/RegsDetail.html", {"currentRegs": currentRegs,
                                                           "previousFlag": previousFlag,
                                                           "nextFlag": nextFlag,
                                                           "unity": unity})

    def post(self, request):
        pass


class CompanyList(View):
    def get(self, request):
        Company_list = CompanyInfo.objects.all()
        if request.GET.get('order') is not None:
            order = int(request.GET.get('order'))
        else:
            order = 2

        if order == 1:
            Company_list = Company_list.order_by('joiningDate')

        else:
            Company_list = Company_list.order_by('-joiningDate')

        paginator = Paginator(Company_list, 10)
        page = request.GET.get('page')
        try:
            customer = paginator.page(page)
        except PageNotAnInteger:
            customer = paginator.page(1)
        except EmptyPage:
            customer = paginator.page(paginator.num_pages)
        return render(request, 'welcome/CompanyList.html',
                      {'CompanyList': customer, 'order': order})
