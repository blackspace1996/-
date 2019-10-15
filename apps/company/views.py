from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q

from apps.unity.models import UnityInfo
from .forms import CompanyAddForm, MemberAddForm, EquipmentAddForm, BlockAddForm
from .models import CompanyInfo, MemberInfo, EquipmentInfo, BlockInfo
from apps.rawProduction.models import RawProductionInfo

# Create your views here.


class CompanyInfoView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass == 1:
            companyInfo_list = CompanyInfo.objects.all()
        elif request.user.identityClass == 2:
            companyInfo_list = CompanyInfo.objects.filter(Q(companyID=request.user.company.companyID)|Q(superCompany=request.user.company))
        else:
            return render(request, "function/no_permissions.html", {})
        if request.GET.get('order') is not None:
            order = int(request.GET.get('order'))
        else:
            order = 2

        if order == 1:
            companyInfo_list = companyInfo_list.order_by('joiningDate')

        elif order == 2:
            companyInfo_list = companyInfo_list.order_by('-joiningDate')

        elif order == 3:
            companyInfo_list = companyInfo_list.order_by('updateTime')

        else:
            companyInfo_list = companyInfo_list.order_by('-updateTime')

        paginator = Paginator(companyInfo_list, 10)
        page = request.GET.get('page')
        try:
            customer = paginator.page(page)
        except PageNotAnInteger:
            customer = paginator.page(1)
        except EmptyPage:
            customer = paginator.page(paginator.num_pages)

        return render(request, "function/companyManagement/companyInfo.html", {'companyInfo_list': customer, 'order': order})

    def post(self, request):
        pass


class CompanyInfoAddView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        unity_list = UnityInfo.objects.all()
        if request.user.identityClass == 1:
            company_list = CompanyInfo.objects.all()
            return render(request, "function/companyManagement/companyInfoAdd.html", {"company_list": company_list, "unity_list": unity_list})
        elif request.user.identityClass == 2:
            company_list = CompanyInfo.objects.filter(companyID=request.user.company.companyID)
            return render(request, "function/companyManagement/companyInfoAdd.html", {"company_list": company_list, "unity_list": unity_list})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if request.user.identityClass == 2 or request.user.identityClass == 1:
            addForm = CompanyAddForm(request.POST)
            if addForm.is_valid():
                companyName = request.POST.get('companyName')
                companyRegisterNumber = request.POST.get('companyRegisterNumber')
                telephone = request.POST.get('telephone')
                legalPersonName = request.POST.get('legalPersonName')
                legalPersonPhone = request.POST.get('legalPersonPhone')
                amountOfProStoreHouse = request.POST.get('amountOfProStoreHouse')
                amountOfItemStoreHouse = request.POST.get('amountOfItemStoreHouse')
                joiningDate = request.POST.get('joiningDate')
                super_company = request.POST.get('super_company')
                unityID = request.POST.get('unityID')
                companyInfo = CompanyInfo()
                companyInfo.companyName = companyName
                companyInfo.companyRegisterNumber = companyRegisterNumber
                companyInfo.telephone = telephone
                companyInfo.legalPersonName = legalPersonName
                companyInfo.legalPersonPhone = legalPersonPhone
                companyInfo.amountOfProStoreHouse = amountOfProStoreHouse
                companyInfo.amountOfItemStoreHouse = amountOfItemStoreHouse
                companyInfo.joiningDate = joiningDate
                companyInfo.unityID = UnityInfo.objects.get(unityID=unityID)
                if request.user.identityClass == 1:
                    if super_company:
                        companyInfo.superCompany = CompanyInfo.objects.get(companyID=super_company)
                elif request.user.identityClass == 2:
                    companyInfo.superCompany = request.user.company

                companyInfo.Save(request)

                return redirect(reverse("companyInfo"))
            else:
                company_list = CompanyInfo.objects.all()
                unity_list = UnityInfo.objects.all()
                error = addForm.errors
                return render(request, "function/companyManagement/companyInfoAdd.html",
                              {"error": error, 'company_list': company_list, "unity_list": unity_list})
        else:
            return render(request, "function/no_permissions.html")


class CompanyInfoUpdateView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        company_id = int(request.GET.get('id'))
        if request.user.identityClass == 1:
            companyInfo_update = CompanyInfo.objects.get(companyID=company_id)
            return render(request, "function/companyManagement/companyInfoUpdate.html", {"raw_companyInfo": companyInfo_update})
        elif request.user.identityClass == 2 and company_id == request.user.company.companyID:
            companyInfo_update = CompanyInfo.objects.get(companyID=company_id)
            return render(request, "function/companyManagement/companyInfoUpdate.html", {"raw_companyInfo": companyInfo_update})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        companyID = int(request.POST.get('update_id'))
        if request.user.identityClass == 1 or (request.user.identityClass == 2 and companyID == request.user.company.companyID):
            addForm = CompanyAddForm(request.POST)
            if addForm.is_valid():
                companyInfo_update = CompanyInfo.objects.get(companyID=companyID)
                companyInfo_update.companyName = request.POST.get('companyName')
                companyInfo_update.companyRegisterNumber = request.POST.get('companyRegisterNumber')
                companyInfo_update.telephone = request.POST.get('telephone')
                companyInfo_update.legalPersonName = request.POST.get('legalPersonName')
                companyInfo_update.legalPersonPhone = request.POST.get('legalPersonPhone')
                companyInfo_update.amountOfProStoreHouse = request.POST.get('amountOfProStoreHouse')
                companyInfo_update.amountOfItemStoreHouse = request.POST.get('amountOfItemStoreHouse')
                companyInfo_update.joiningDate = request.POST.get('joiningDate')
                companyInfo_update.Save(request)

                raw_companyInfo = CompanyInfo.objects.get(companyID=companyID)
                return render(request, "function/companyManagement/companyInfoUpdate.html", {"raw_companyInfo": raw_companyInfo, "success": 1})
            else:
                companyID = int(request.POST.get('update_id'))
                raw_companyInfo = CompanyInfo.objects.get(companyID=companyID)
                error = addForm.errors
                return render(request, "function/companyManagement/companyInfoUpdate.html", {"raw_companyInfo": raw_companyInfo, "error": error})
        else:
            return render(request, "function/no_permissions.html", {})


class CompanyInfoDeleteView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        delete_id = int(request.GET.get('id'))
        if request.user.identityClass == 1:
            CompanyInfo.objects.get(companyID=delete_id).Delete(request)
            return redirect(reverse('companyInfo'))
        # 父公司可以删除子公司信息
        elif request.user.identityClass == 2:
            if CompanyInfo.objects.get(companyID=delete_id).superCompany.companyID == request.user.company.companyID:
                CompanyInfo.objects.get(companyID=delete_id).Delete(request)
                return redirect(reverse('companyInfo'))
        else:
            return render(request, "function/no_permissions.html", {})

    def post(self, request):
        pass


class CompanyInfoDetailsView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        company_id = int(request.GET.get('id'))
        if request.user.identityClass == 1:
            currentInfo = CompanyInfo.objects.get(companyID=company_id)
            return render(request, "function/companyManagement/companyInfoDetails.html", {"currentInfo": currentInfo})
        elif request.user.identityClass == 2:
            # 检查是否是上级公司查看
            if CompanyInfo.objects.get(companyID=company_id).superCompany:
                if CompanyInfo.objects.get(companyID=company_id).superCompany.companyID == request.user.company.companyID:
                    currentInfo = CompanyInfo.objects.get(companyID=company_id)
                    return render(request, "function/companyManagement/companyInfoDetails.html",
                                  {"currentInfo": currentInfo})
                else:
                    return render(request, "function/no_permissions.html", {})
            # 检查是不是自己看自己
            elif company_id == request.user.company.companyID:
                currentInfo = CompanyInfo.objects.get(companyID=company_id)
                return render(request, "function/companyManagement/companyInfoDetails.html",
                              {"currentInfo": currentInfo})
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    def post(self, request):
        pass


class MemberInfoView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        # 系统管理员查看所有公司成员信息
        if request.user.identityClass == 1:
            companyInfo_list = CompanyInfo.objects.all()
            company_current = request.GET.get("company_current")
            if not company_current:
                if companyInfo_list:
                    company_current = companyInfo_list[0].companyID
            else:
                company_current = int(company_current)
            member_list = MemberInfo.objects.filter(companyName=company_current)
            if request.GET.get('order') is not None:
                order = int(request.GET.get('order'))
            else:
                order = 2

            if order == 1:
                member_list = member_list.order_by('hireDate')

            elif order == 2:
                member_list = member_list.order_by('-hireDate')

            paginator = Paginator(member_list, 10)
            page = request.GET.get('page')
            try:
                customer = paginator.page(page)
            except PageNotAnInteger:
                customer = paginator.page(1)
            except EmptyPage:
                customer = paginator.page(paginator.num_pages)

            return render(request, "function/companyManagement/memberInfo.html", {'member_list': customer, 'order': order, 'member_list_get': 1, 'companyInfo_list': companyInfo_list, "selected_id": company_current, "company_current": company_current})
        # 系统操作员查看自己及子公司员工信息
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
                member_list = MemberInfo.objects.filter(companyName=company_current)
                if request.GET.get('order') is not None:
                    order = int(request.GET.get('order'))
                else:
                    order = 2

                if order == 1:
                    member_list = member_list.order_by('hireDate')

                elif order == 2:
                    member_list = member_list.order_by('-hireDate')

                paginator = Paginator(member_list, 10)
                page = request.GET.get('page')
                try:
                    customer = paginator.page(page)
                except PageNotAnInteger:
                    customer = paginator.page(1)
                except EmptyPage:
                    customer = paginator.page(paginator.num_pages)

                return render(request, "function/companyManagement/memberInfo.html", {'member_list': customer, 'order': order, 'member_list_get': 1, 'companyInfo_list': companyInfo_list, "selected_id": company_current, "company_current": company_current})
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    def post(self, request):
        pass


class MemberInfoAddView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass == 2 :
            return render(request, "function/companyManagement/memberInfoAdd.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if request.user.identityClass == 2:
                addForm = MemberAddForm(request.POST)
                if addForm.is_valid():
                    memberName = request.POST.get("memberName")
                    position = request.POST.get("position")
                    telephone = request.POST.get("telephone")
                    hireDate = request.POST.get("hireDate")
                    memberInfo = MemberInfo()
                    memberInfo.memberName = memberName
                    memberInfo.position = position
                    memberInfo.telephone = telephone
                    memberInfo.hireDate = hireDate
                    memberInfo.companyName = request.user.company
                    memberInfo.Save(request)

                    return redirect(reverse("memberInfo"))
                else:
                    error = addForm.errors
                    return render(request, "function/companyManagement/memberInfoAdd.html", {"error": error})
        else:
            return render(request, "function/no_permissions.html", {})


class MemberInfoDeleteView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        delete_id = int(request.GET.get('id'))
        if request.user.identityClass == 2:
            if request.user.company.companyID == MemberInfo.objects.get(memberID=delete_id).companyName.companyID:
                MemberInfo.objects.get(memberID=delete_id).Delete(request)
                return redirect(reverse('memberInfo'))
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass


class MemberInfoDetailsView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        member_id = int(request.GET.get('id'))
        if request.user.identityClass == 1:
            currentInfo = MemberInfo.objects.get(memberID=member_id)
            return render(request, "function/companyManagement/memberInfoDetails.html", {"currentInfo": currentInfo})
        # 员工细节信息只有本公司的系统操作员能查看
        elif request.user.identityClass == 2:
            if MemberInfo.objects.get(memberID=member_id).companyName.companyID == request.user.company.companyID:
                currentInfo = MemberInfo.objects.get(memberID=member_id)
                return render(request, "function/companyManagement/memberInfoDetails.html",
                              {"currentInfo": currentInfo})
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    def post(self, request):
        pass


class MemberInfoUpdateView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass == 2:
            update_id = int(request.GET.get('id'))
            if request.user.company.companyID == MemberInfo.objects.get(memberID=update_id).companyName.companyID:
                rawMemberInfo = MemberInfo.objects.get(memberID=update_id)
                return render(request, "function/companyManagement/memberInfoUpdate.html", {"rawMemberInfo": rawMemberInfo})
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if request.user.identityClass == 2:
            update_id = int(request.POST.get('update_id'))
            if request.user.company.companyID == MemberInfo.objects.get(memberID=update_id).companyName.companyID:
                addForm = MemberAddForm(request.POST)
                if addForm.is_valid():
                    memberName = request.POST.get("memberName")
                    position = request.POST.get("position")
                    telephone = request.POST.get("telephone")
                    hireDate = request.POST.get("hireDate")
                    memberInfo = MemberInfo.objects.get(memberID=update_id)
                    memberInfo.memberName = memberName
                    memberInfo.position = position
                    memberInfo.telephone = telephone
                    memberInfo.hireDate = hireDate
                    memberInfo.companyName = request.user.company
                    memberInfo.Save(request)

                    return redirect(reverse("memberInfo"))
                else:
                    error = addForm.errors
                    rawMemberInfo = MemberInfo.objects.get(memberID=update_id)
                    return render(request, "function/companyManagement/memberInfoUpdate.html", {"error": error, "rawMemberInfo": rawMemberInfo})
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})


class EquipmentInfoView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        # 系统管理员查看所有公司设备信息
        if request.user.identityClass == 1:
            companyInfo_list = CompanyInfo.objects.all()
            company_current = request.GET.get("company_current")
            if not company_current:
                if companyInfo_list:
                    company_current = companyInfo_list[0].companyID
            else:
                company_current = int(company_current)
            equipment_list = EquipmentInfo.objects.filter(companyID=company_current)
            paginator = Paginator(equipment_list, 10)
            page = request.GET.get('page')
            try:
                customer = paginator.page(page)
            except PageNotAnInteger:
                customer = paginator.page(1)
            except EmptyPage:
                customer = paginator.page(paginator.num_pages)

            return render(request, "function/companyManagement/equipmentInfo.html", {'equipment_list': customer, 'equipment_list_get': 1, 'companyInfo_list': companyInfo_list, "selected_id": company_current, "company_current": company_current})
        # 系统操作员查看自己及子公司设备信息
        elif request.user.identityClass == 2:
            company_self = request.user.company.companyID
            companyInfo_list = CompanyInfo.objects.filter(Q(companyID=company_self) | Q(superCompany=company_self))
            company_current = request.GET.get("company_current")
            if not company_current:
                if companyInfo_list:
                    company_current = companyInfo_list[0].companyID
            else:
                company_current = int(company_current)
            # 禁止越权访问
            if (company_self == company_current) or (company_self == CompanyInfo.objects.get(companyID=company_current).superCompany.companyID):
                equipment_list = EquipmentInfo.objects.filter(companyID=company_current).order_by("equipmentName")

                paginator = Paginator(equipment_list, 10)
                page = request.GET.get('page')
                try:
                    customer = paginator.page(page)
                except PageNotAnInteger:
                    customer = paginator.page(1)
                except EmptyPage:
                    customer = paginator.page(paginator.num_pages)

                return render(request, "function/companyManagement/equipmentInfo.html", {'equipment_list': customer, 'equipment_list_get': 1, 'companyInfo_list': companyInfo_list, "selected_id": company_current, "company_current": company_current})
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    def post(self, request):
        pass


class EquipmentInfoAddView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass == 2:
            return render(request, "function/companyManagement/equipmentInfoAdd.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if request.user.identityClass == 2:
                addForm = EquipmentAddForm(request.POST)
                if addForm.is_valid():
                    equipmentName = request.POST.get("equipmentName")
                    amount = request.POST.get("amount")
                    description = request.POST.get("description")
                    share = request.POST.get("share")
                    shareCondition = request.POST.get("shareCondition")
                    equipmentInfo = EquipmentInfo()
                    equipmentInfo.equipmentName = equipmentName
                    equipmentInfo.companyID = request.user.company
                    equipmentInfo.amount = amount
                    equipmentInfo.description = description
                    if share == '1':
                        equipmentInfo.share = True
                        equipmentInfo.shareCondition = shareCondition
                    else:
                        equipmentInfo.share = False
                        equipmentInfo.shareCondition = ''
                    equipmentInfo.Save(request)

                    return redirect(reverse("equipmentInfo"))
                else:
                    error = addForm.errors
                    return render(request, "function/companyManagement/equipmentInfoAdd.html", {"error": error})
        else:
            return render(request, "function/no_permissions.html", {})


class EquipmentInfoDeleteView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        delete_id = int(request.GET.get('id'))
        if request.user.identityClass == 2:
            if request.user.company.companyID == EquipmentInfo.objects.get(id=delete_id).companyID.companyID:
                EquipmentInfo.objects.get(id=delete_id).Delete(request)
                return redirect(reverse('equipmentInfo'))
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass


class EquipmentInfoDetailsView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        equipment_id = int(request.GET.get('id'))
        if request.user.identityClass == 1:
            currentInfo = EquipmentInfo.objects.get(id=equipment_id)
            return render(request, "function/companyManagement/equipmentInfoDetails.html", {"currentInfo": currentInfo})
        # 本公司设备细节信息只有本公司的系统操作员能查看
        elif request.user.identityClass == 2:
            if EquipmentInfo.objects.get(id=equipment_id).companyID.companyID == request.user.company.companyID:
                currentInfo = EquipmentInfo.objects.get(id=equipment_id)
                return render(request, "function/companyManagement/equipmentInfoDetails.html",
                              {"currentInfo": currentInfo})
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    def post(self, request):
        pass


class EquipmentInfoUpdateView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass == 2:
            update_id = int(request.GET.get('id'))
            if request.user.company.companyID == EquipmentInfo.objects.get(id=update_id).companyID.companyID:
                rawEquipmentInfo = EquipmentInfo.objects.get(id=update_id)
                return render(request, "function/companyManagement/equipmentInfoUpdate.html", {"rawEquipmentInfo": rawEquipmentInfo})
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if request.user.identityClass == 2:
            update_id = int(request.POST.get('update_id'))
            if request.user.company.companyID == EquipmentInfo.objects.get(id=update_id).companyID.companyID:
                addForm = EquipmentAddForm(request.POST)
                if addForm.is_valid():
                    equipmentName = request.POST.get("equipmentName")
                    amount = request.POST.get("amount")
                    description = request.POST.get("description")
                    share = request.POST.get("share")
                    shareCondition = request.POST.get("shareCondition")
                    equipmentInfo = EquipmentInfo.objects.get(id=update_id)
                    equipmentInfo.equipmentName = equipmentName
                    equipmentInfo.companyID = request.user.company
                    equipmentInfo.amount = amount
                    equipmentInfo.description = description
                    if share == '1':
                        equipmentInfo.share = True
                        equipmentInfo.shareCondition = shareCondition
                    else:
                        equipmentInfo.share = False
                        equipmentInfo.shareCondition = ''
                    equipmentInfo.Save(request)

                    return redirect(reverse("equipmentInfo"))
                else:
                    error = addForm.errors
                    rawEquipmentInfo = EquipmentInfo.objects.get(id=update_id)
                    return render(request, "function/companyManagement/equipmentInfoUpdate.html", {"error": error, "rawEquipmentInfo": rawEquipmentInfo})
        else:
            return render(request, "function/no_permissions.html", {})


class BlockInfoView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        # 系统管理员查看所有公司地块信息
        if request.user.identityClass == 1:
            companyInfo_list = CompanyInfo.objects.all()
            company_current = request.GET.get("company_current")
            if not company_current:
                if companyInfo_list:
                    company_current = companyInfo_list[0].companyID
            else:
                company_current = int(company_current)
            block_list = BlockInfo.objects.filter(companyID=company_current)
            paginator = Paginator(block_list, 10)
            page = request.GET.get('page')
            try:
                customer = paginator.page(page)
            except PageNotAnInteger:
                customer = paginator.page(1)
            except EmptyPage:
                customer = paginator.page(paginator.num_pages)

            return render(request, "function/companyManagement/blockInfo.html", {'block_list': customer, 'block_list_get': 1, 'companyInfo_list': companyInfo_list, "selected_id": company_current, "company_current": company_current})
        # 系统操作员查看自己及子公司地块信息
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
                block_list = BlockInfo.objects.filter(companyID=company_current).order_by("blockID")

                paginator = Paginator(block_list, 10)
                page = request.GET.get('page')
                try:
                    customer = paginator.page(page)
                except PageNotAnInteger:
                    customer = paginator.page(1)
                except EmptyPage:
                    customer = paginator.page(paginator.num_pages)

                return render(request, "function/companyManagement/blockInfo.html", {'block_list': customer, 'block_list_get': 1, 'companyInfo_list': companyInfo_list, "selected_id": company_current, "company_current": company_current})
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    def post(self, request):
        pass


class BlockInfoAddView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass == 2:
            rawProduction_list = RawProductionInfo.objects.filter(company=request.user.company.companyID)
            return render(request, "function/companyManagement/blockInfoAdd.html", {"rawProduction_list": rawProduction_list})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if request.user.identityClass == 2:
            rawProduction_list = RawProductionInfo.objects.filter(company=request.user.company.companyID)
            addForm = BlockAddForm(request.POST)
            if addForm.is_valid():
                blockName = request.POST.get("blockName")
                rawProduction = request.POST.get("rawProduction")
                blockSquare = request.POST.get("blockSquare")
                unit = request.POST.get("unit")
                soilInfo = request.POST.get("soilInfo")
                blockInfo = BlockInfo()
                blockInfo.companyID = request.user.company
                blockInfo.blockName = blockName
                if rawProduction=='无':
                    blockInfo.rawProduction = None
                else:
                    blockInfo.rawProduction = RawProductionInfo.objects.get(id=rawProduction)
                blockInfo.blockSquare = blockSquare
                if unit == '1' or unit == '2':
                    blockInfo.unit = unit
                blockInfo.soilInfo = soilInfo
                blockInfo.Save(request)

                return redirect(reverse("blockInfo"))
            else:
                error = addForm.errors
                return render(request, "function/companyManagement/blockInfoAdd.html", {"error": error,"rawProduction_list": rawProduction_list})
        else:
            return render(request, "function/no_permissions.html", {})


class BlockInfoUpdateView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass == 2:
            update_block_id = int(request.GET.get('id'))
            update_block = BlockInfo.objects.get(blockID=update_block_id)
            if update_block.companyID == request.user.company:
                rawProduction_list = RawProductionInfo.objects.filter(company=request.user.company.companyID)
                return render(request, "function/companyManagement/blockInfOUpdate.html", {"rawProduction_list": rawProduction_list, 'update_block': update_block})
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if request.user.identityClass == 2:
            addForm = BlockAddForm(request.POST)
            update_block_id = int(request.POST.get('update_id'))
            update_block = BlockInfo.objects.get(blockID=update_block_id)
            if update_block.companyID == request.user.company:
                if addForm.is_valid():
                    blockName = request.POST.get("blockName")
                    rawProduction = request.POST.get("rawProduction")
                    blockSquare = request.POST.get("blockSquare")
                    unit = request.POST.get("unit")
                    soilInfo = request.POST.get("soilInfo")
                    update_block.blockName = blockName
                    if not rawProduction:
                        update_block.rawProduction = None
                    else:
                        update_block.rawProduction = RawProductionInfo.objects.get(id=rawProduction)
                    update_block.blockSquare = blockSquare
                    if unit == '1' or unit == '2':
                        update_block.unit = unit
                    update_block.soilInfo = soilInfo
                    update_block.Save(request)
                    return redirect(reverse("blockInfo"))
                else:
                    error = addForm.errors
                    return render(request, "function/companyManagement/blockInfoAdd.html", {"error": error, 'update_block':update_block})
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})


class BlockInfoDeleteView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        delete_id = int(request.GET.get('id'))
        delete_block = BlockInfo.objects.get(blockID=delete_id)
        if request.user.identityClass == 2:
            if request.user.company.companyID == delete_block.companyID.companyID:
                delete_block.Delete(request)
                return redirect(reverse('blockInfo'))
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass


class BlockInfoDetailsView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        block_id = int(request.GET.get('id'))
        if request.user.identityClass == 1:
            currentInfo = BlockInfo.objects.get(blockID=block_id)
            return render(request, "function/companyManagement/blockInfoDetails.html", {"currentInfo": currentInfo})
        # 本公司地块细节信息只有本公司的系统操作员能查看
        elif request.user.identityClass == 2:
            if BlockInfo.objects.get(blockID=block_id).companyID == request.user.company:
                currentInfo = BlockInfo.objects.get(blockID=block_id)
                return render(request, "function/companyManagement/blockInfoDetails.html",
                              {"currentInfo": currentInfo})
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    def post(self, request):
        pass


class EquipmentShareInfoView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        search = request.GET.get('search')
        if request.user.identityClass ==0:
            return render(request,"function/no_permissions.html",{})
        user_unityID = request.user.unityID
        if not search:
            equipment_list = EquipmentInfo.objects.filter(share=True)
            equipment_list=equipment_list.filter(companyID__unityID=user_unityID)
            paginator = Paginator(equipment_list, 10)
            page = request.GET.get('page')
            try:
                customer = paginator.page(page)
            except PageNotAnInteger:
                customer = paginator.page(1)
            except EmptyPage:
                customer = paginator.page(paginator.num_pages)
            return render(request, "function/companyManagement/equipmentShareInfo.html", {"equipment_list": customer})
        else:
            equipment_list = EquipmentInfo.objects.filter(Q(share=True) & Q(equipmentName__icontains=search))
            equipment_list = equipment_list.filter(companyID__unityID=user_unityID)
            paginator = Paginator(equipment_list, 10)
            page = request.GET.get('page')
            try:
                customer = paginator.page(page)
            except PageNotAnInteger:
                customer = paginator.page(1)
            except EmptyPage:
                customer = paginator.page(paginator.num_pages)
            return render(request, "function/companyManagement/equipmentShareInfo.html",
                          {"equipment_list": customer, "searchCondition": search})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass
