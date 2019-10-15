from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta

from .models import CostInfo, IncomeInfo
from .forms import CostAddForm, IncomeAddForm
# Create your views here.


class CostManagementInfoView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if not (request.user.identityClass == 1 or request.user.identityClass == 0):
            Type = request.GET.get("Type")
            Time = request.GET.get("Time")
            order = request.GET.get("order")
            amount = 0
            if not Type:
                Type = "cost"
            if not Time:
                Time = "all"
            if not order:
                order = 1
            else:
                order = int(order)

            if Type == "cost":
                if Time == "all":
                    if order == 1:
                        cost_list = CostInfo.objects.filter(costCompany=request.user.company).order_by("costTime")
                    else:
                        cost_list = CostInfo.objects.filter(costCompany=request.user.company).order_by("-costTime")

                    for cost in cost_list:
                        words = str(cost.costTime) + str(cost.costType) + str(cost.recorder.holder) + str(cost.costAmount)
                        if check_password(words, cost.hashWords):
                            cost.isNormal = True
                            cost.save()
                        else:
                            cost.isNormal = False
                            cost.save()
                        amount = amount + cost.costAmount

                    paginator = Paginator(cost_list, 10)
                    page = request.GET.get('page')
                    try:
                        customer = paginator.page(page)
                    except PageNotAnInteger:
                        customer = paginator.page(1)
                    except EmptyPage:
                        customer = paginator.page(paginator.num_pages)
                    return render(request, "function/costManagement/costManagementInfo.html",
                                  {'cost_list': customer, 'order': order, 'Type': Type, 'Time': Time, 'amount': amount})

                elif Time == "week":
                    today = datetime.now()
                    # 当前天 显示当前日期是本周第几天
                    day_num = today.isoweekday()
                    # 计算当前日期所在周一
                    monday = (today - timedelta(days=day_num))
                    if order == 1:
                        # 查询一周内的数据
                        cost_list = CostInfo.objects.filter(
                            Q(costCompany=request.user.company) & Q(
                                costTime__range=(monday, today))).order_by("costTime")
                    else:
                        cost_list = CostInfo.objects.filter(
                            Q(costCompany=request.user.company) & Q(
                                costTime__range=(monday, today))).order_by("-costTime")

                    for cost in cost_list:
                        words = str(cost.costTime) + str(cost.costType) + str(cost.recorder.holder) + str(cost.costAmount)
                        if check_password(words, cost.hashWords):
                            cost.isNormal = True
                            cost.save()

                        else:
                            cost.isNormal = False
                            cost.save()
                        amount = amount + cost.costAmount

                    paginator = Paginator(cost_list, 10)
                    page = request.GET.get('page')
                    try:
                        customer = paginator.page(page)
                    except PageNotAnInteger:
                        customer = paginator.page(1)
                    except EmptyPage:
                        customer = paginator.page(paginator.num_pages)
                    return render(request, "function/costManagement/costManagementInfo.html",
                                  {'cost_list': customer, 'order': order, 'Type': Type, 'Time': Time, 'amount': amount})

                elif Time == "month":
                    today = datetime.today()
                    if order == 1:
                        # 查询一月内的数据
                        cost_list = CostInfo.objects.filter(
                            Q(costCompany=request.user.company) & Q(
                                costTime__month=today.month)).order_by("costTime")
                    else:
                        cost_list = CostInfo.objects.filter(
                            Q(costCompany=request.user.company) & Q(
                                costTime__month=today.month)).order_by("-costTime")

                    for cost in cost_list:
                        words = str(cost.costTime) + str(cost.costType) + str(cost.recorder.holder) + str(cost.costAmount)
                        if check_password(words, cost.hashWords):
                            cost.isNormal = True
                            cost.save()
                        else:
                            cost.isNormal = False
                            cost.save()
                        amount = amount + cost.costAmount

                    paginator = Paginator(cost_list, 10)
                    page = request.GET.get('page')
                    try:
                        customer = paginator.page(page)
                    except PageNotAnInteger:
                        customer = paginator.page(1)
                    except EmptyPage:
                        customer = paginator.page(paginator.num_pages)
                    return render(request, "function/costManagement/costManagementInfo.html",
                                  {'cost_list': customer, 'order': order, 'Type': Type, 'Time': Time, 'amount': amount})

                elif Time == "year":
                    today = datetime.today()
                    if order == 1:
                        # 查询一年内的数据
                        cost_list = CostInfo.objects.filter(
                            Q(costCompany=request.user.company) & Q(
                                costTime__year=today.year)).order_by("costTime")
                    else:
                        cost_list = CostInfo.objects.filter(
                            Q(costCompany=request.user.company) & Q(
                                costTime__year=today.year)).order_by("-costTime")

                    for cost in cost_list:
                        words = str(cost.costTime) + str(cost.costType) + str(cost.recorder.holder) + str(cost.costAmount)
                        if check_password(words, cost.hashWords):
                            cost.isNormal = True
                            cost.save()
                        else:
                            cost.isNormal = False
                            cost.save()
                        amount = amount + cost.costAmount

                    paginator = Paginator(cost_list, 10)
                    page = request.GET.get('page')
                    try:
                        customer = paginator.page(page)
                    except PageNotAnInteger:
                        customer = paginator.page(1)
                    except EmptyPage:
                        customer = paginator.page(paginator.num_pages)
                    return render(request, "function/costManagement/costManagementInfo.html",
                                  {'cost_list': customer, 'order': order, 'Type': Type, 'Time': Time, 'amount': amount})

            elif Type == 'income':
                if Time == "all":
                    if order == 1:
                        income_list = IncomeInfo.objects.filter(incomeCompany=request.user.company).order_by("incomeTime")
                    else:
                        income_list = IncomeInfo.objects.filter(incomeCompany=request.user.company).order_by("-incomeTime")

                    for income in income_list:
                        words = str(income.incomeTime) + str(income.incomeType) + str(income.recorder.holder) + str(income.incomeAmount)
                        if check_password(words, income.hashWords):
                            income.isNormal = True
                            income.save()
                        else:
                            income.isNormal = False
                            income.save()
                        amount = amount + income.incomeAmount

                    paginator = Paginator(income_list, 10)
                    page = request.GET.get('page')
                    try:
                        customer = paginator.page(page)
                    except PageNotAnInteger:
                        customer = paginator.page(1)
                    except EmptyPage:
                        customer = paginator.page(paginator.num_pages)
                    return render(request, "function/costManagement/costManagementInfo.html",
                                  {'income_list': customer, 'order': order, 'Type': Type, 'Time': Time, 'amount': amount})

                elif Time == "week":
                    today = datetime.now()
                    # 当前天 显示当前日期是本周第几天
                    day_num = today.isoweekday()
                    # 计算当前日期所在周一
                    monday = (today - timedelta(days=day_num))
                    if order == 1:
                        # 查询一周内的数据
                        income_list = IncomeInfo.objects.filter(
                            Q(incomeCompany=request.user.company) & Q(
                                incomeTime__range=(monday, today))).order_by("incomeTime")
                    else:
                        income_list = IncomeInfo.objects.filter(
                            Q(incomeCompany=request.user.company) & Q(
                                incomeTime__range=(monday, today))).order_by("-incomeTime")

                    for income in income_list:
                        words = str(income.incomeTime) + str(income.incomeType) + str(income.recorder.holder) + str(income.incomeAmount)
                        if check_password(words, income.hashWords):
                            income.isNormal = True
                            income.save()
                        else:
                            income.isNormal = False
                            income.save()
                        amount = amount + income.incomeAmount

                    paginator = Paginator(income_list, 10)
                    page = request.GET.get('page')
                    try:
                        customer = paginator.page(page)
                    except PageNotAnInteger:
                        customer = paginator.page(1)
                    except EmptyPage:
                        customer = paginator.page(paginator.num_pages)
                    return render(request, "function/costManagement/costManagementInfo.html",
                                  {'income_list': customer, 'order': order, 'Type': Type, 'Time': Time, 'amount': amount})

                elif Time == "month":
                    today = datetime.today()
                    if order == 1:
                        # 查询一月内的数据
                        income_list = IncomeInfo.objects.filter(
                            Q(incomeCompany=request.user.company) & Q(
                                incomeTime__month=today.month)).order_by("incomeTime")
                    else:
                        income_list = IncomeInfo.objects.filter(
                            Q(incomeCompany=request.user.company) & Q(
                                incomeTime__month=today.month)).order_by("-incomeTime")

                    for income in income_list:
                        words = str(income.incomeTime) + str(income.incomeType) + str(income.recorder.holder) + str(income.incomeAmount)
                        if check_password(words, income.hashWords):
                            income.isNormal = True
                            income.save()
                        else:
                            income.isNormal = False
                            income.save()
                        amount = amount + income.incomeAmount

                    paginator = Paginator(income_list, 10)
                    page = request.GET.get('page')
                    try:
                        customer = paginator.page(page)
                    except PageNotAnInteger:
                        customer = paginator.page(1)
                    except EmptyPage:
                        customer = paginator.page(paginator.num_pages)
                    return render(request, "function/costManagement/costManagementInfo.html",
                                  {'income_list': customer, 'order': order, 'Type': Type, 'Time': Time, 'amount': amount})

                elif Time == "year":
                    today = datetime.today()
                    if order == 1:
                        # 查询一年内的数据
                        income_list = IncomeInfo.objects.filter(
                            Q(incomeCompany=request.user.company) & Q(
                                incomeTime__year=today.year)).order_by("incomeTime")
                    else:
                        income_list = IncomeInfo.objects.filter(
                            Q(incomeCompany=request.user.company) & Q(
                                incomeTime__year=today.year)).order_by("-incomeTime")

                    for income in income_list:
                        words = str(income.incomeTime) + str(income.incomeType) + str(income.recorder.holder) + str(income.incomeAmount)
                        if check_password(words, income.hashWords):
                            income.isNormal = True
                            income.save()
                        else:
                            income.isNormal = False
                            income.save()
                        amount = amount + income.incomeAmount

                    paginator = Paginator(income_list, 10)
                    page = request.GET.get('page')
                    try:
                        customer = paginator.page(page)
                    except PageNotAnInteger:
                        customer = paginator.page(1)
                    except EmptyPage:
                        customer = paginator.page(paginator.num_pages)
                    return render(request, "function/costManagement/costManagementInfo.html",
                                  {'income_list': customer, 'order': order, 'Type': Type, 'Time': Time, 'amount': amount})

        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass


class CostManagementInfoAddView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if not request.user.identityClass == 1:
            Type = request.GET.get("Type")
            if not Type:
                Type = "cost"
            return render(request, "function/costManagement/costManagementInfoAdd.html", {"Type": Type})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if not request.user.identityClass == 1:
            Type = request.POST.get("Type")
            if Type == "cost":
                costName = request.POST.get("costName")
                costTips = request.POST.get("costTips")
                costAmount = request.POST.get("costAmount")
                costTime = request.POST.get("costTime")
                costType = request.POST.get("costType")
                addForm = CostAddForm(request.POST)
                if addForm.is_valid():
                    costInfo = CostInfo()
                    costInfo.costName = costName
                    costInfo.costTips = costTips
                    costInfo.costAmount = costAmount
                    costInfo.costTime = costTime
                    costInfo.costType = costType
                    costInfo.isNormal = True
                    costInfo.recorder = request.user
                    costInfo.costCompany = request.user.company
                    # 加密环节
                    words = str(costTime) + str(costType) + str(request.user.holder) + str(costAmount)
                    costInfo.hashWords = make_password(words, 'cmy', 'pbkdf2_sha256')
                    costInfo.Save(request)
                    return redirect(reverse("costManagementInfo"))
                else:
                    error = addForm.errors
                    return render(request, "function/costManagement/costManagementInfoAdd.html", {"Type": Type, "error": error})

            elif Type == "income":
                incomeName = request.POST.get("incomeName")
                incomeTips = request.POST.get("incomeTips")
                incomeAmount = request.POST.get("incomeAmount")
                incomeTime = request.POST.get("incomeTime")
                incomeType = request.POST.get("incomeType")
                addForm = IncomeAddForm(request.POST)
                if addForm.is_valid():
                    incomeInfo = IncomeInfo()
                    incomeInfo.incomeName = incomeName
                    incomeInfo.incomeTips = incomeTips
                    incomeInfo.incomeAmount = incomeAmount
                    incomeInfo.incomeTime = incomeTime
                    incomeInfo.incomeType = incomeType
                    incomeInfo.isNormal = True
                    incomeInfo.recorder = request.user
                    incomeInfo.incomeCompany = request.user.company
                    # 加密环节
                    words = str(incomeTime) + str(incomeType) + str(request.user.holder) + str(incomeAmount)
                    incomeInfo.hashWords = make_password(words, 'cmy', 'pbkdf2_sha256')
                    incomeInfo.Save(request)
                    return redirect(reverse("costManagementInfo"))
                else:
                    error = addForm.errors
                    return render(request, "function/costManagement/costManagementInfoAdd.html", {"Type": Type, "error": error})
        else:
            return render(request, "function/no_permissions.html", {})


class CostManagementInfoDetailsView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass == 1:
            return render(request, "function/no_permissions.html", {})
        else:
            Type = request.GET.get("Type")
            id = int(request.GET.get("id"))
            if Type == "cost":
                currentInfo = CostInfo.objects.get(id=id)
                if currentInfo.costCompany == request.user.company:
                    return render(request, "function/costManagement/costManagementInfoDetails.html",
                                  {"currentInfo": currentInfo, "Type": Type})
                else:
                    return render(request, "function/no_permissions.html", {})
            else:
                currentInfo = IncomeInfo.objects.get(id=id)
                if currentInfo.incomeCompany == request.user.company:
                    return render(request, "function/costManagement/costManagementInfoDetails.html",
                                  {"currentInfo": currentInfo, "Type": Type})
                else:
                    return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass
