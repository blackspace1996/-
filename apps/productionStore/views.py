from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime

from apps.rawProduction.models import RawProductionInfo
from apps.productionManagement.models import SowInfo, HarvestInfo
from apps.company.models import CompanyInfo, MemberInfo
from .models import StoreInfo
from .forms import StoreInfoAddForm
# Create your views here.


class StoreInfoAddView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if not request.user.identityClass == 1:
            batch_id = request.GET.get("id")
            batch = HarvestInfo.objects.get(id=batch_id)
            member_list = MemberInfo.objects.filter(companyName=request.user.company)
            if batch.harvestCompany == request.user.company:
                return render(request, "function/productionStore/productionStoreAdd.html", {"batch": batch,
                                                                                            "member_list": member_list})
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if not request.user.identityClass == 1:
            current_batch_id = request.POST.get("batch_id")
            current_batch = HarvestInfo.objects.get(id=current_batch_id)
            current_member_id = request.POST.get("storeMember")
            current_member = MemberInfo.objects.get(memberID=current_member_id)
            if not current_member.companyName == request.user.company:
                return render(request, "function/no_permissions.html", {})
            addForm = StoreInfoAddForm(request.POST)
            if current_batch.isStore:
                return render(request, "function/no_permissions.html", {})
            if current_batch.harvestCompany == request.user.company:
                if addForm.is_valid():
                    current_batch.isStore = True
                    current_batch.save()
                    storeTips = request.POST.get("storeTips")
                    amount = request.POST.get("amount")
                    unit = request.POST.get("unit")
                    storeHouse = request.POST.get("storeHouse")
                    storeInfoAdd = StoreInfo()
                    storeInfoAdd.batch = current_batch
                    storeInfoAdd.storeTips = storeTips
                    storeInfoAdd.amount = amount
                    storeInfoAdd.restAmount = amount
                    storeInfoAdd.unit = unit
                    storeInfoAdd.storeMember = current_member
                    storeInfoAdd.storeHouse = storeHouse
                    storeInfoAdd.recorder = request.user
                    storeInfoAdd.isNormal = True
                    # 加密环节
                    words = str(current_batch_id) + str(request.user.holder) + str(storeTips) + str(float(amount)) + str(unit)
                    storeInfoAdd.hashWords = make_password(words, 'cmy', 'pbkdf2_sha256')
                    storeInfoAdd.Save(request)
                    return redirect(reverse('storeInfo'))
                else:
                    batch_id = request.POST.get("batch_id")
                    batch = HarvestInfo.objects.get(id=batch_id)
                    error = addForm.errors
                    if batch.harvestCompany == request.user.company:
                        return render(request, "function/productionStore/productionStoreAdd.html", {"batch": batch,
                                                                                                    "error": error})
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})


class StoreInfoView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        # 系统管理员查看所有公司存储信息
        if request.user.identityClass==0:
            return render(request, "function/no_permissions.html", {})
        elif request.user.identityClass == 1:
            companyInfo_list = CompanyInfo.objects.all()
            company_current = request.GET.get("company_current")
            if request.GET.get('order') is not None:
                order = int(request.GET.get('order'))
            else:
                order = 2
            if not company_current:
                if companyInfo_list:
                    company_current = companyInfo_list[0].companyID
            else:
                company_current = int(company_current)

            rawProduction_current = request.GET.get("rawProduction_current")

            if not rawProduction_current:
                rawProduction_current_exist = RawProductionInfo.objects.filter(company=company_current)
                if rawProduction_current_exist:
                    rawProduction_current = rawProduction_current_exist[0].id
                else:
                    rawProduction_current = ''
            else:
                rawProduction_current = int(rawProduction_current)

            rawProductionInfo_list = RawProductionInfo.objects.filter(company=company_current)

            if rawProduction_current:
                if order == 1:
                    storeInfo_list = StoreInfo.objects.filter(Q(batch__harvestCompany=company_current) & Q(batch__harvestBatch__sowingProduction=rawProduction_current)).order_by("storingPeriod")
                else:
                    storeInfo_list = StoreInfo.objects.filter(Q(batch__harvestCompany=company_current) & Q(batch__harvestBatch__sowingProduction=rawProduction_current)).order_by("-storingPeriod")
                for storeInfo in storeInfo_list:
                    # 计算入库日期
                    today = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
                    storingDay = datetime.strptime(storeInfo.storeTime.strftime('%Y-%m-%d'), '%Y-%m-%d')
                    period = (today - storingDay).days
                    storeInfo.storingPeriod = period
                    storeInfo.save()
                    # 加密
                    words = str(storeInfo.batch.id) + str(storeInfo.recorder.holder) + str(storeInfo.storeTips) + str(storeInfo.amount) + str(storeInfo.unit)
                    if check_password(words, storeInfo.hashWords):
                        storeInfo.isNormal = True
                        storeInfo.save()
                    else:
                        storeInfo.isNormal = False
                        storeInfo.save()
                paginator = Paginator(storeInfo_list, 10)
                page = request.GET.get('page')
                try:
                    customer = paginator.page(page)
                except PageNotAnInteger:
                    customer = paginator.page(1)
                except EmptyPage:
                    customer = paginator.page(paginator.num_pages)
            else:
                customer = ''

            return render(request, "function/productionStore/productionStoreInfo.html",
                          {'storeInfo_list': customer, 'storeInfo_list_get': 1, 'companyInfo_list': companyInfo_list,
                           "selected_id": company_current, "company_current": company_current,
                           "rawProductionInfo_list": rawProductionInfo_list,
                           "rawProduction_current_id": rawProduction_current,
                           "order": order})

        else:
            if request.GET.get('order') is not None:
                order = int(request.GET.get('order'))
            else:
                order = 2
            rawProduction_current = request.GET.get("rawProduction_current")

            if not rawProduction_current:
                rawProduction_current_exist = RawProductionInfo.objects.filter(company=request.user.company)
                if rawProduction_current_exist:
                    rawProduction_current = rawProduction_current_exist[0].id
                else:
                    rawProduction_current = ''
            else:
                rawProduction_current = int(rawProduction_current)

            rawProductionInfo_list = RawProductionInfo.objects.filter(company=request.user.company)

            if rawProduction_current:
                if order == 1:
                    storeInfo_list = StoreInfo.objects.filter(Q(batch__harvestCompany=request.user.company) & Q(batch__harvestBatch__sowingProduction=rawProduction_current)).order_by("storingPeriod")
                else:
                    storeInfo_list = StoreInfo.objects.filter(Q(batch__harvestCompany=request.user.company) & Q(batch__harvestBatch__sowingProduction=rawProduction_current)).order_by("-storingPeriod")
                # 加密环节
                for storeInfo in storeInfo_list:
                    # 计算入库日期
                    today = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
                    storingDay = datetime.strptime(storeInfo.storeTime.strftime('%Y-%m-%d'), '%Y-%m-%d')
                    period = (today-storingDay).days
                    storeInfo.storingPeriod = period
                    storeInfo.save()
                    # 加密
                    words = str(storeInfo.batch.id) + str(storeInfo.recorder.holder) + str(storeInfo.storeTips) + str(
                        storeInfo.amount) + str(storeInfo.unit)
                    if check_password(words, storeInfo.hashWords):
                        storeInfo.isNormal = True
                        storeInfo.save()
                    else:
                        storeInfo.isNormal = False
                        storeInfo.save()
                paginator = Paginator(storeInfo_list, 10)
                page = request.GET.get('page')
                try:
                    customer = paginator.page(page)
                except PageNotAnInteger:
                    customer = paginator.page(1)
                except EmptyPage:
                    customer = paginator.page(paginator.num_pages)
            else:
                customer = ''

            return render(request, "function/productionStore/productionStoreInfo.html",
                          {'storeInfo_list': customer, 'storeInfo_list_get': 1,
                           "rawProductionInfo_list": rawProductionInfo_list,
                           "rawProduction_current_id": rawProduction_current,
                           "order": order})


class StoreInfoDetailsView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        currentInfo_id = request.GET.get("id")
        currentInfo = StoreInfo.objects.get(id=currentInfo_id)
        if request.user.identityClass == 1:
            return render(request, "function/productionStore/productionStoreInfoDetails.html",
                          {"currentInfo": currentInfo})
        else:
            if currentInfo.batch.harvestCompany == request.user.company:
                return render(request, "function/productionStore/productionStoreInfoDetails.html",
                              {"currentInfo": currentInfo})
            else:
                return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass

