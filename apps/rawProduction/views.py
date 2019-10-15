from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q


from apps.company.models import CompanyInfo
from .models import RawProductionInfo, RawProductionManagement
from .forms import RawProductionInfoAddForm, RawProductionMeasureInfoAddForm
# Create your views here.


class RawProductionInfoView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        # 系统管理员查看所有公司品种信息
        if request.user.identityClass == 1:
            companyInfo_list = CompanyInfo.objects.all()
            company_current = request.GET.get("company_current")
            if not company_current:
                if companyInfo_list:
                    company_current = companyInfo_list[0].companyID
            else:
                company_current = int(company_current)
            rawProduction_list = RawProductionInfo.objects.filter(company=company_current)
            paginator = Paginator(rawProduction_list, 10)
            page = request.GET.get('page')
            try:
                customer = paginator.page(page)
            except PageNotAnInteger:
                customer = paginator.page(1)
            except EmptyPage:
                customer = paginator.page(paginator.num_pages)

            return render(request, "function/rawProductionManagement/rawProductionInfo.html", {'rawProduction_list': customer, 'rawProduction_list_get': 1, 'companyInfo_list': companyInfo_list, "selected_id": company_current, "company_current": company_current})
        # 系统操作员查看自己及子公司品种信息
        elif request.user.identityClass == 2:
            company_self = request.user.company.companyID
            companyInfo_list = CompanyInfo.objects.filter(Q(companyID=company_self) | Q(superCompany=company_self))
            company_current = request.GET.get("company_current")
            if not company_current:
                if companyInfo_list:
                    company_current = companyInfo_list[0].companyID
            else:
                company_current = int(company_current)
            if (company_self == company_current) or (
                        company_self == CompanyInfo.objects.get(companyID=company_current).superCompany.companyID):
                rawProduction_list = RawProductionInfo.objects.filter(company=company_current).order_by("createTime")

                paginator = Paginator(rawProduction_list, 10)
                page = request.GET.get('page')
                try:
                    customer = paginator.page(page)
                except PageNotAnInteger:
                    customer = paginator.page(1)
                except EmptyPage:
                    customer = paginator.page(paginator.num_pages)

                return render(request, "function/rawProductionManagement/rawProductionInfo.html", {'rawProduction_list': customer, 'rawProduction_list_get': 1, 'companyInfo_list': companyInfo_list, "selected_id": company_current, "company_current": company_current})
            else:
                return render(request, "function/no_permissions.html", {})
        elif request.user.identityClass == 3:
            # 操作员拥有查看本公司品种的权限
            rawProduction_list = RawProductionInfo.objects.filter(company=request.user.company).order_by("createTime")
            paginator = Paginator(rawProduction_list, 10)
            page = request.GET.get('page')
            try:
                customer = paginator.page(page)
            except PageNotAnInteger:
                customer = paginator.page(1)
            except EmptyPage:
                customer = paginator.page(paginator.num_pages)

            return render(request, "function/rawProductionManagement/rawProductionInfo.html",
                          {'rawProduction_list': customer, 'rawProduction_list_get': 1})
        else:
            return render(request,"function/no_permissions.html",{})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass


class RawProductionInfoAddView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass == 2:
            return render(request, 'function/rawProductionManagement/rawProductionInfoAdd.html', {})
        else:
            return render(request, 'function/no_permissions.html', {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if request.user.identityClass == 2:
            addForm = RawProductionInfoAddForm(request.POST)
            if addForm.is_valid():
                rawProductionName = request.POST.get("rawProductionName")
                description = request.POST.get("description")
                rawProductionInfo = RawProductionInfo()
                rawProductionInfo.rawProductionName = rawProductionName
                rawProductionInfo.company = request.user.company
                rawProductionInfo.description = description
                rawProductionInfo.Save(request)
                return redirect(reverse("rawProductionInfo"))
            else:
                error = addForm.errors
                return render(request, "function/rawProductionManagement/rawProductionInfoAdd.html", {"error": error})

        else:
            return render(request, 'function/no_permissions.html', {})


class RawProductionInfoDetailsView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        pass

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass


class RawProductionInfoDeleteView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        delete_id = int(request.GET.get('id'))
        delete_info = RawProductionInfo.objects.get(id=delete_id)
        if request.user.identityClass == 2:
            if request.user.company == delete_info.company:
                delete_info.delete()
                return redirect(reverse('rawProductionInfo'))
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass


class RawProductionInfoUpdateView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass == 2:
            update_id = int(request.GET.get("id"))
            update_info = RawProductionInfo.objects.get(id=update_id)
            if update_info.company == request.user.company:
                return render(request, 'function/rawProductionManagement/rawProductionInfoUpdate.html', {'rawInfo': update_info})
            else:
                return render(request, 'function/no_permissions.html', {})
        else:
            return render(request, 'function/no_permissions.html', {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if request.user.identityClass == 2:
            update_id = int(request.POST.get("id"))
            update_info = RawProductionInfo.objects.get(id=update_id)
            if update_info.company == request.user.company:
                addForm = RawProductionInfoAddForm(request.POST)
                if addForm.is_valid():
                    rawProductionName = request.POST.get("rawProductionName")
                    description = request.POST.get("description")
                    rawProductionInfo = update_info
                    rawProductionInfo.rawProductionName = rawProductionName
                    rawProductionInfo.company = request.user.company
                    rawProductionInfo.description = description
                    rawProductionInfo.Save(request)
                    return redirect(reverse("rawProductionInfo"))
                else:
                    error = addForm.errors
                    return render(request, "function/rawProductionManagement/rawProductionInfoUpdate.html", {"error": error, 'rawInfo': update_info})
            else:
                return render(request, 'function/no_permissions.html', {})
        else:
            return render(request, 'function/no_permissions.html', {})


class RawProductionMeasureInfoView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        # 系统管理员查看所有公司质量环节信息
        if request.user.identityClass == 1:
            companyInfo_list = CompanyInfo.objects.all()
            company_current = request.GET.get("company_current")
            rawProduction_current = request.GET.get("rawProduction_current")
            if not company_current:
                if companyInfo_list:
                    company_current = companyInfo_list[0].companyID
            else:
                company_current = int(company_current)

            if not rawProduction_current:
                rawProduction_current_exist = RawProductionInfo.objects.filter(company=company_current)
                if rawProduction_current_exist:
                    rawProduction_current = rawProduction_current_exist[0].id
                else:
                    rawProduction_current = ''
            else:
                rawProduction_current = int(rawProduction_current)

            rawProductionInfo_list = RawProductionInfo.objects.filter(company=company_current)
            # 质量环节的情况
            if rawProduction_current:
                rawProductionMeasure_list = RawProductionManagement.objects.filter(
                    Q(company=company_current) & Q(rawProductionName=rawProduction_current)).order_by("orderNumber")
                paginator = Paginator(rawProductionMeasure_list, 10)
                page = request.GET.get('page')
                try:
                    customer = paginator.page(page)
                except PageNotAnInteger:
                    customer = paginator.page(1)
                except EmptyPage:
                    customer = paginator.page(paginator.num_pages)
            else:
                customer = ''
            return render(request, "function/rawProductionManagement/rawProductionMeasureInfo.html",
                          {'rawProductionMeasure_list': customer, 'companyInfo_list': companyInfo_list,
                           "selected_id": company_current, "company_current_id": company_current,
                           "rawProduction_current_id": rawProduction_current, 'rawProductionInfo_list':rawProductionInfo_list})
        # 系统操作员查看自己及子公司质量环节信息
        elif request.user.identityClass == 2:
            company_self = request.user.company.companyID
            companyInfo_list = CompanyInfo.objects.filter(Q(companyID=company_self) | Q(superCompany=company_self))
            company_current = request.GET.get("company_current")
            rawProduction_current = request.GET.get("rawProduction_current")
            if not company_current:
                if companyInfo_list:
                    company_current = companyInfo_list[0].companyID
            else:
                company_current = int(company_current)

            if not rawProduction_current:
                rawProduction_current_exist = RawProductionInfo.objects.filter(company=company_current)
                if rawProduction_current_exist:
                    rawProduction_current = rawProduction_current_exist[0].id
                else:
                    rawProduction_current = ''
            else:
                rawProduction_current = int(rawProduction_current)

            rawProductionInfo_list = RawProductionInfo.objects.filter(company=company_current)
            # 有品种的情况
            if rawProduction_current:
                rawProductionMeasure_list = RawProductionManagement.objects.filter(
                    Q(company=company_current) & Q(rawProductionName=rawProduction_current)).order_by("orderNumber")
                paginator = Paginator(rawProductionMeasure_list, 10)
                page = request.GET.get('page')
                try:
                    customer = paginator.page(page)
                except PageNotAnInteger:
                    customer = paginator.page(1)
                except EmptyPage:
                    customer = paginator.page(paginator.num_pages)
            else:
                customer = ''
            return render(request, "function/rawProductionManagement/rawProductionMeasureInfo.html",
                          {'rawProductionMeasure_list': customer, 'companyInfo_list': companyInfo_list,
                           "selected_id": company_current, "company_current_id": company_current,
                           "rawProduction_current_id": rawProduction_current, 'rawProductionInfo_list':rawProductionInfo_list})
        elif request.user.identityClass == 3:
            # 操作员拥有查看本公司质量环节的权限
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
            # 有品种的情况
            if rawProduction_current:
                rawProductionMeasure_list = RawProductionManagement.objects.filter(
                    Q(company=request.user.company) & Q(rawProductionName=rawProduction_current)).order_by("orderNumber")
                paginator = Paginator(rawProductionMeasure_list, 10)
                page = request.GET.get('page')
                try:
                    customer = paginator.page(page)
                except PageNotAnInteger:
                    customer = paginator.page(1)
                except EmptyPage:
                    customer = paginator.page(paginator.num_pages)
            else:
                customer = ''
            return render(request, "function/rawProductionManagement/rawProductionMeasureInfo.html",
                          {'rawProductionMeasure_list': customer,
                           "rawProduction_current_id": rawProduction_current,
                           'rawProductionInfo_list': rawProductionInfo_list})
        else:
            return render(request,"function/no_permissions.html",{})


class RawProductionMeasureInfoAddView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass == 2:
            company_self = request.user.company
            rawProduction_list = RawProductionInfo.objects.filter(company=company_self)
            return render(request, "function/rawProductionManagement/rawProductionMeasureInfoAdd.html", {"rawProduction_list":rawProduction_list})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if request.user.identityClass == 2:
            company_self = request.user.company
            rawProduction_list = RawProductionInfo.objects.filter(company=company_self)
            addForm = RawProductionMeasureInfoAddForm(request.POST)
            if addForm.is_valid():
                rawProductionName = request.POST.get("rawProductionName")
                qualityControlMeasure = request.POST.get("qualityControlMeasure")
                measureDescription = request.POST.get("measureDescription")
                rawProductionMeasureInfo = RawProductionManagement()
                rawProductionMeasureInfo.rawProductionName = RawProductionInfo.objects.get(id=rawProductionName)
                rawProductionMeasureInfo.company = request.user.company
                rawProductionMeasureInfo.qualityControlMeasure = qualityControlMeasure
                rawProductionMeasureInfo.measureDescription = measureDescription
                rawProductionMeasureInfo.Save(request)
                return redirect(reverse("rawProductionMeasureInfo"))
            else:
                error = addForm.errors
                return render(request, "function/rawProductionManagement/rawProductionMeasureInfoAdd.html", {"error": error,"rawProduction_list":rawProduction_list})

        else:
            return render(request, 'function/no_permissions.html', {})


class RawProductionMeasureInfoUpdateView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass == 2:
            company_self = request.user.company
            rawProduction_list = RawProductionInfo.objects.filter(company=company_self)
            update_info_id = int(request.GET.get("id"))
            update_info = RawProductionManagement.objects.get(id=update_info_id)
            if update_info.company == request.user.company:
                return render(request, "function/rawProductionManagement/rawProductionMeasureInfoUpdate.html",
                              {"rawProduction_list": rawProduction_list, "update_info": update_info})
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if request.user.identityClass == 2:
            update_info_id = int(request.POST.get("id"))
            update_info = RawProductionManagement.objects.get(id=update_info_id)
            if update_info.company == request.user.company:
                addForm = RawProductionMeasureInfoAddForm(request.POST)
                if addForm.is_valid():
                    rawProductionName = request.POST.get("rawProductionName")
                    qualityControlMeasure = request.POST.get("qualityControlMeasure")
                    measureDescription = request.POST.get("measureDescription")
                    update_info.rawProductionName = RawProductionInfo.objects.get(id=rawProductionName)
                    update_info.qualityControlMeasure = qualityControlMeasure
                    update_info.measureDescription = measureDescription
                    update_info.Save(request)
                    return redirect(reverse("rawProductionMeasureInfo"))
                else:
                    error = addForm.errors
                    return render(request, "function/rawProductionManagement/rawProductionMeasureInfoUpdate.html",
                                  {"error": error, "update_info": update_info})
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, 'function/no_permissions.html', {})


class RawProductionMeasureInfoDetailsView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        current_info_id = request.GET.get("id")
        current_info = RawProductionManagement.objects.get(id=current_info_id)
        if request.user.identityClass == 1:
            return render(request, "function/rawProductionManagement/rawProductionMeasureInfoDetails.html",
                          {"currentInfo": current_info})
        else:
            if current_info.company == request.user.company:
                return render(request, "function/rawProductionManagement/rawProductionMeasureInfoDetails.html",
                              {"currentInfo": current_info})
            else:
                return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass


class RawProductionMeasureSort(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass == 2:
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

            # 有品种的情况
            if rawProduction_current:
                rawProductionMeasure_list = RawProductionManagement.objects.filter(
                    Q(company=request.user.company) & Q(rawProductionName=rawProduction_current)).order_by("orderNumber")

                measureAmount = len(rawProductionMeasure_list)
                paginator = Paginator(rawProductionMeasure_list, 10)
                page = request.GET.get('page')
                try:
                    customer = paginator.page(page)
                except PageNotAnInteger:
                    customer = paginator.page(1)
                except EmptyPage:
                    customer = paginator.page(paginator.num_pages)
            else:
                measureAmount = 0
                customer = ''
            return render(request, "function/rawProductionManagement/rawProductionMeasureSort.html",
                          {'rawProductionMeasure_list': customer,
                           "rawProduction_current_id": rawProduction_current,
                           'rawProductionInfo_list': rawProductionInfo_list,
                           'measureAmount': measureAmount})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if request.user.identityClass == 2:
            measureAmount = int(request.POST.get("measureAmount"))
            for i in range(1, measureAmount+1):
                current_measure_id = int(request.POST.get(str(i)))
                current_measure = RawProductionManagement.objects.get(id=current_measure_id)
                if current_measure.company == request.user.company:
                    current_measure.orderNumber = i
                    current_measure.save()
                else:
                    return render(request, "function/no_permissions.html", {})
            return redirect(reverse('rawProductionMeasureInfo'))
        else:
            return render(request, "function/no_permissions.html", {})


class RawProductionMeasureInfoDeleteView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        delete_id = int(request.GET.get('id'))
        delete_info = RawProductionManagement.objects.get(id=delete_id)
        if request.user.identityClass == 2:
            if request.user.company == delete_info.company:
                delete_info.delete()
                return redirect(reverse('rawProductionMeasureInfo'))
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass


