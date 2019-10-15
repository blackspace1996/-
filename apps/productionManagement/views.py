from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password

from apps.company.models import CompanyInfo, MemberInfo, BlockInfo
from apps.rawProduction.models import RawProductionInfo, RawProductionManagement
from .models import SowInfo, MeasureConfirmingInfo, HarvestInfo
from .forms import SowingAddForm, ConfirmingMeasureForm
# Create your views here.


class SowingInfoView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        # 系统管理员查看所有公司收获信息
        if request.user.identityClass==0:
            return render(request, "function/no_permissions.html", {})
        elif request.user.identityClass == 1:
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
            if rawProduction_current:
                sowingInfo_list = SowInfo.objects.filter(Q(sowingCompany=company_current) & Q(sowingProduction=rawProduction_current))
                for sowingInfo in sowingInfo_list:
                    words = str(sowingInfo.sowingName) + str(sowingInfo.sowingTips) + str(
                        sowingInfo.sowingBlock.blockID) + str(
                        sowingInfo.sowingMember.memberID) + str(sowingInfo.sowingProduction.id) + str(
                        sowingInfo.recorder.holder)
                    if check_password(words, sowingInfo.hashWords):
                        sowingInfo.isNormal = True
                        sowingInfo.save()
                    else:
                        sowingInfo.isNormal = False
                        sowingInfo.save()
                paginator = Paginator(sowingInfo_list, 10)
                page = request.GET.get('page')
                try:
                    customer = paginator.page(page)
                except PageNotAnInteger:
                    customer = paginator.page(1)
                except EmptyPage:
                    customer = paginator.page(paginator.num_pages)
            else:
                customer = ''
            return render(request, "function/producingManagement/sowingInfo.html",
                          {'sowingInfo_list': customer, 'sowingInfo_list_get': 1, 'companyInfo_list': companyInfo_list,
                           "selected_id": company_current, "company_current": company_current,
                           "rawProductionInfo_list": rawProductionInfo_list,
                           "rawProduction_current_id": rawProduction_current})
        else :
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
                sowingInfo_list = SowInfo.objects.filter(Q(sowingCompany=request.user.company) & Q(sowingProduction=rawProduction_current))
                for sowingInfo in sowingInfo_list:
                    words = str(sowingInfo.sowingName) + str(sowingInfo.sowingTips) + str(
                        sowingInfo.sowingBlock.blockID) + str(
                        sowingInfo.sowingMember.memberID) + str(sowingInfo.sowingProduction.id) + str(
                        sowingInfo.recorder.holder)
                    if check_password(words, sowingInfo.hashWords):
                        sowingInfo.isNormal = True
                        sowingInfo.save()
                    else:
                        sowingInfo.isNormal = False
                        sowingInfo.save()
                paginator = Paginator(sowingInfo_list, 10)
                page = request.GET.get('page')
                try:
                    customer = paginator.page(page)
                except PageNotAnInteger:
                    customer = paginator.page(1)
                except EmptyPage:
                    customer = paginator.page(paginator.num_pages)
            else:
                customer = ''
            return render(request, "function/producingManagement/sowingInfo.html",
                          {'sowingInfo_list': customer, 'sowingInfo_list_get': 1,
                           "rawProductionInfo_list": rawProductionInfo_list,
                           "rawProduction_current_id": rawProduction_current})


    def post(self, request):
        pass


class SowingInfoAddView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass == 1:
            return render(request, "function/no_permissions.html", {})
        else:
            rawProduction_list = RawProductionInfo.objects.filter(company=request.user.company.companyID)
            block_list = BlockInfo.objects.filter(companyID=request.user.company)
            member_list = MemberInfo.objects.filter(companyName=request.user.company)
            return render(request, "function/producingManagement/sowingInfoAdd.html",
                          {"rawProduction_list": rawProduction_list,
                           "block_list": block_list, "member_list": member_list})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if request.user.identityClass == 1:
            return render(request, "function/no_permissions.html", {})
        else:
            addForm = SowingAddForm(request.POST)
            if addForm.is_valid():
                sowingName = request.POST.get("sowingName")
                sowingTips = request.POST.get("sowingTips")
                sowingProduction = int(request.POST.get("sowingProduction"))
                sowingBlock = int(request.POST.get("sowingBlock"))
                sowingMember = int(request.POST.get("sowingMember"))
                sowInfo = SowInfo()
                sowInfo.sowingName = sowingName
                sowInfo.sowingTips = sowingTips
                sowInfo.sowingCompany = request.user.company
                current_rawProduction = RawProductionInfo.objects.get(id=sowingProduction)
                current_block = BlockInfo.objects.get(blockID=sowingBlock)
                current_member = MemberInfo.objects.get(memberID=sowingMember)
                if request.user.company == current_rawProduction.company:
                    sowInfo.sowingProduction = current_rawProduction
                # 同时修改对应地块种植的产品
                if request.user.company == current_block.companyID:
                    sowInfo.sowingBlock = current_block
                    current_block.rawProduction = current_rawProduction
                    current_block.Save(request)
                if request.user.company == current_member.companyName:
                    sowInfo.sowingMember = current_member
                sowInfo.recorder = request.user
                # 加密环节
                words = str(sowingName) + str(sowingTips) + str(sowingBlock) + str(sowingMember) + str(
                    sowingProduction) + str(request.user.holder)
                sowInfo.hashWords = make_password(words, 'cmy', 'pbkdf2_sha256')
                sowInfo.Save(request)
                # 建立所有对应的质量环节
                measures_list = RawProductionManagement.objects.filter(rawProductionName=current_rawProduction)
                for measure in measures_list:
                    measure_new = MeasureConfirmingInfo()
                    measure_new.company = request.user.company
                    measure_new.rawProduction = current_rawProduction
                    measure_new.measure = measure
                    measure_new.sowingBatch = sowInfo
                    measure_new.isConfirming = False
                    measure_new.Save(request)
                return redirect(reverse("sowingInfo"))
            else:
                error = addForm.errors
                return render(request, "function/companyManagement/blockInfoAdd.html", {"error": error})


class SowingInfoDetailsView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        sowingInfo_id = int(request.GET.get('id'))
        if request.user.identityClass == 1:
            currentInfo = SowInfo.objects.get(id=sowingInfo_id)
            return render(request, "function/producingManagement/sowingInfoDetails.html", {"currentInfo": currentInfo})
        # 本公司播种细节信息只有本公司的系统操作员能查看
        elif request.user.identityClass == 2:
            if SowInfo.objects.get(id=sowingInfo_id).sowingCompany == request.user.company:
                currentInfo = SowInfo.objects.get(id=sowingInfo_id)
                return render(request, "function/producingManagement/sowingInfoDetails.html",
                              {"currentInfo": currentInfo})
            else:
                return render(request, "function/no_permissions.html", {})
        # 本公司播种细节信息只有本公司的操作员能查看
        else:
            if SowInfo.objects.get(id=sowingInfo_id).sowingCompany == request.user.company:
                currentInfo = SowInfo.objects.get(id=sowingInfo_id)
                return render(request, "function/producingManagement/sowingInfoDetails.html",
                              {"currentInfo": currentInfo})
            else:
                return render(request, "function/no_permissions.html", {})

    def post(self, request):
        pass


class SowingInfoDeleteView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        delete_id = int(request.GET.get('id'))
        delete_info = SowInfo.objects.get(id=delete_id)
        if request.user.identityClass == 2:
            if request.user.company.companyID == delete_info.sowingCompany.companyID:
                delete_info.Delete(request)
                return redirect(reverse('sowingInfo'))
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass


class MeasuresConfirmingView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        current_id = int(request.GET.get("id"))
        current_batch = SowInfo.objects.get(id=current_id)
        measure_list = MeasureConfirmingInfo.objects.filter(sowingBatch=current_batch).order_by("measure__orderNumber")
        current_measure = -1
        completeAmount = 0
        harvestFlag = False
        for measure in measure_list:
            if (current_measure == -1) & (not measure.isConfirming):
                current_measure = measure.measure.orderNumber
            # 加密环节
            if measure.isConfirming:
                words = str(measure.confirmingMember) + str(measure.sowingBatch.sowingName) + str(measure.recorder.holder)
                if check_password(words, measure.hashWords):
                    measure.isNormal = True
                else:
                    measure.isNormal = False
                measure.save()
                completeAmount = completeAmount + 1
        if completeAmount == len(measure_list):
            harvestFlag = True
        if request.user.identityClass == 1:
            return render(request, "function/producingManagement/measureConfirming.html",
                          {"measure_list": measure_list, "current_measure": current_measure,
                           "harvestFlag": harvestFlag, "current_batch": current_batch})
        else:
            if current_batch.sowingCompany == request.user.company:
                return render(request, "function/producingManagement/measureConfirming.html",
                              {"measure_list": measure_list, "current_measure": current_measure,
                               "harvestFlag": harvestFlag, "current_batch": current_batch})
            else:
                return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass


class MeasureConfirmingCompleteView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        current_id = request.GET.get("id")
        current_confirming = MeasureConfirmingInfo.objects.get(id=current_id)
        sowingInfo = current_confirming.sowingBatch
        if request.user.identityClass == 1:
            return render(request, "function/producingManagement/measureConfirmingComplete.html",
                          {"current_info": current_confirming, "sowingInfo": sowingInfo})
        else:
            if current_confirming.company == request.user.company:
                return render(request, "function/producingManagement/measureConfirmingComplete.html",
                              {"current_info": current_confirming,  "sowingInfo": sowingInfo})
            else:
                return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        current_id = request.POST.get("id")
        current_confirming = MeasureConfirmingInfo.objects.get(id=current_id)
        if current_confirming.isConfirming:
            return render(request, "function/no_permissions.html", {})
        sowingInfo = current_confirming.sowingBatch
        addForm = ConfirmingMeasureForm(request.POST)
        if request.user.identityClass == 1:
            if addForm.is_valid():
                confirmingMember = request.POST.get("confirmingMember")
                confirmingTips = request.POST.get("confirmingTips")
                confirmingTime = request.POST.get("confirmingTime")
                current_confirming.isConfirming = True
                current_confirming.confirmingTime = confirmingTime
                current_confirming.confirmingMember = confirmingMember
                current_confirming.confirmingTips = confirmingTips
                current_confirming.recorder = request.user

                # 加密环节
                words = str(confirmingMember) + str(current_confirming.sowingBatch.sowingName) + str(request.user.holder)
                current_confirming.hashWords = make_password(words, 'cmy', 'pbkdf2_sha256')
                current_confirming.Save(request)
                return redirect(reverse("sowingInfo"))
            else:
                error = addForm.errors
                return render(request, "function/producingManagement/measureConfirmingComplete.html",
                              {"current_info": current_confirming,  "sowingInfo": sowingInfo, "error": error})
        else:
            if request.user.company == current_confirming.company:
                if addForm.is_valid():
                    confirmingMember = request.POST.get("confirmingMember")
                    confirmingTips = request.POST.get("confirmingTips")
                    confirmingTime = request.POST.get("confirmingTime")
                    current_confirming.isConfirming = True
                    current_confirming.confirmingMember = confirmingMember
                    current_confirming.confirmingTips = confirmingTips
                    current_confirming.recorder = request.user
                    current_confirming.confirmingTime = confirmingTime

                    # 加密环节
                    words = str(confirmingMember) + str(current_confirming.sowingBatch.sowingName) + str(
                        request.user.holder)
                    current_confirming.hashWords = make_password(words, 'cmy', 'pbkdf2_sha256')
                    current_confirming.save()
                    return redirect(reverse("sowingInfo"))
                else:
                    error = addForm.errors
                    return render(request, "function/producingManagement/measureConfirmingComplete.html",
                                  {"current_info": current_confirming, "sowingInfo": sowingInfo, "error": error})


class MeasureConfirmingDetailsView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        currentInfo_id = request.GET.get("id")
        currentInfo = MeasureConfirmingInfo.objects.get(id=currentInfo_id)
        if request.user.identityClass == 1:
            return render(request, "function/producingManagement/measureConfirmingDetails.html",
                          {"currentInfo": currentInfo})
        else:
            if currentInfo.company == request.user.company:
                return render(request, "function/producingManagement/measureConfirmingDetails.html",
                              {"currentInfo": currentInfo})
            else:
                return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass


class HarvestInfoAddView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if not request.user.identityClass == 1:
            current_batch_id = request.GET.get("id")
            current_batch = SowInfo.objects.get(id=current_batch_id)
            confirming_list = MeasureConfirmingInfo.objects.filter(sowingBatch=current_batch)
            confirmAmount = 0
            if current_batch.isHarvest:
                return render(request, "function/no_permissions.html", {})
            for confirming in confirming_list:
                if confirming.isConfirming:
                    confirmAmount = confirmAmount + 1
            if confirmAmount == len(confirming_list):
                member_list = MemberInfo.objects.filter(companyName=request.user.company)
                return render(request, "function/producingManagement/harvestInfoAdd.html",
                              {"current_batch": current_batch, "member_list": member_list})
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if not request.user.identityClass == 1:
            current_batch_id = request.POST.get("batch_id")
            current_batch = SowInfo.objects.get(id=current_batch_id)
            confirming_list = MeasureConfirmingInfo.objects.filter(sowingBatch=current_batch)
            confirmAmount = 0
            if current_batch.isHarvest:
                return render(request, "function/no_permissions.html", {})
            for confirming in confirming_list:
                if confirming.isConfirming:
                    confirmAmount = confirmAmount + 1
            if confirmAmount == len(confirming_list):
                harvestTips = request.POST.get("harvestTips")
                member_id = request.POST.get("harvestMember")
                harvestMember = MemberInfo.objects.get(memberID=member_id)
                harvestInfo = HarvestInfo()
                harvestInfo.harvestBatch = current_batch
                harvestInfo.harvestTips = harvestTips
                harvestInfo.harvestCompany = request.user.company
                harvestInfo.harvestMember = harvestMember
                harvestInfo.recorder = request.user
                # 加密环节
                words = str(current_batch_id) + str(harvestMember.memberName) + str(harvestTips) + str(request.user.holder)
                harvestInfo.hashWords = make_password(words, 'cmy', 'pbkdf2_sha256')
                harvestInfo.isNormal = True
                # 修改收获Flag
                current_batch.isHarvest = True
                current_batch.save()
                harvestInfo.Save(request)
                return redirect(reverse('harvestInfo'))
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})


class HarvestInfoView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        # 系统管理员查看所有公司收获信息
        if request.user.identityClass==0:
            return render(request, "function/no_permissions.html", {})
        elif request.user.identityClass == 1:
            companyInfo_list = CompanyInfo.objects.all()
            company_current = request.GET.get("company_current")
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
                harvestInfo_list = HarvestInfo.objects.filter(Q(harvestCompany=company_current) & Q(harvestBatch__sowingProduction=rawProduction_current))
                for harvestInfo in harvestInfo_list:
                    words = str(harvestInfo.harvestBatch.id) + str(
                        harvestInfo.harvestMember.memberName) + str(harvestInfo.harvestTips) + str(
                        harvestInfo.recorder.holder)
                    if check_password(words, harvestInfo.hashWords):
                        harvestInfo.isNormal = True
                        harvestInfo.save()
                    else:
                        harvestInfo.isNormal = False
                        harvestInfo.save()
                paginator = Paginator(harvestInfo_list, 10)
                page = request.GET.get('page')
                try:
                    customer = paginator.page(page)
                except PageNotAnInteger:
                    customer = paginator.page(1)
                except EmptyPage:
                    customer = paginator.page(paginator.num_pages)

            else:
                customer = ''
            return render(request, "function/producingManagement/harvestInfo.html",
                          {'harvestInfo_list': customer, 'harvestInfo_list_get': 1, 'companyInfo_list': companyInfo_list,
                           "selected_id": company_current, "company_current": company_current,
                           "rawProductionInfo_list": rawProductionInfo_list,
                           "rawProduction_current_id": rawProduction_current})
        else:
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
                harvestInfo_list = HarvestInfo.objects.filter(Q(harvestCompany=request.user.company) & Q(harvestBatch__sowingProduction=rawProduction_current))
                # 加密环节
                for harvestInfo in harvestInfo_list:
                    words = str(harvestInfo.harvestBatch.id) + str(
                        harvestInfo.harvestMember.memberName) + str(harvestInfo.harvestTips) + str(
                        harvestInfo.recorder.holder)

                    if check_password(words, harvestInfo.hashWords):
                        harvestInfo.isNormal = True
                        harvestInfo.save()
                    else:
                        harvestInfo.isNormal = False
                        harvestInfo.save()
                paginator = Paginator(harvestInfo_list, 10)
                page = request.GET.get('page')
                try:
                    customer = paginator.page(page)
                except PageNotAnInteger:
                    customer = paginator.page(1)
                except EmptyPage:
                    customer = paginator.page(paginator.num_pages)
            else:
                customer = ''
            return render(request, "function/producingManagement/harvestInfo.html",
                          {'harvestInfo_list': customer, 'harvestInfo_list_get': 1,
                           "rawProductionInfo_list": rawProductionInfo_list,
                           "rawProduction_current_id": rawProduction_current
                           })


    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass


class HarvestInfoDetailsView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        currentInfo_id = request.GET.get("id")
        currentInfo = HarvestInfo.objects.get(id=currentInfo_id)
        if request.user.identityClass == 1:
            return render(request, "function/producingManagement/harvestInfoDetails.html",
                          {"currentInfo": currentInfo})
        else:
            if currentInfo.harvestCompany == request.user.company:
                return render(request, "function/producingManagement/harvestInfoDetails.html",
                              {"currentInfo": currentInfo})
            else:
                return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass

