from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
import datetime
import io

import png
import pyqrcode

from project520.settings import Des_example
from apps.company.models import CompanyInfo, MemberInfo, BlockInfo
from apps.productionStore.models import StoreInfo
from apps.rawProduction.models import RawProductionManagement, RawProductionInfo
from apps.productionManagement.models import MeasureConfirmingInfo
from apps.itemStore.models import ItemCostInfo
from .forms import SaleInfoAddForm
from .models import SaleInfo


# Create your views here.


class SaleInfoAddView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if not request.user.identityClass == 1:
            batch_id = request.GET.get("id")
            batch = StoreInfo.objects.get(id=batch_id)
            member_list = MemberInfo.objects.filter(companyName=request.user.company)
            if batch.batch.harvestCompany == request.user.company:
                return render(request, "function/saleManagement/saleInfoAdd.html", {"batch": batch,
                                                                                    "member_list": member_list})
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if not request.user.identityClass == 1:
            current_batch_id = request.POST.get("batch_id")
            current_batch = StoreInfo.objects.get(id=current_batch_id)
            current_member_id = request.POST.get("saleMember")
            current_member = MemberInfo.objects.get(memberID=current_member_id)
            if not current_member.companyName == request.user.company:
                return render(request, "function/no_permissions.html", {})
            addForm = SaleInfoAddForm(request.POST)
            if current_batch.batch.harvestCompany == request.user.company:
                if addForm.is_valid():
                    saleName = request.POST.get("saleName")
                    saleTips = request.POST.get("saleTips")
                    amount = float(request.POST.get("amount"))
                    buyer = request.POST.get("buyer")
                    saleTime = request.POST.get("saleTime")
                    if not amount > 0:
                        member_list = MemberInfo.objects.filter(companyName=request.user.company)
                        return render(request, "function/saleManagement/saleInfoAdd.html",
                                      {"batch": current_batch, "member_list": member_list,
                                       "amountIllegal": 1})
                    if amount > current_batch.restAmount:
                        member_list = MemberInfo.objects.filter(companyName=request.user.company)
                        return render(request, "function/saleManagement/saleInfoAdd.html",
                                      {"batch": current_batch, "member_list": member_list,
                                       "amountIllegal": 2})
                    saleInfoAdd = SaleInfo()
                    saleInfoAdd.saleBatch = current_batch
                    saleInfoAdd.saleName = saleName
                    saleInfoAdd.amount = amount
                    saleInfoAdd.buyer = buyer
                    saleInfoAdd.saleTips = saleTips
                    saleInfoAdd.saleMember = current_member
                    saleInfoAdd.saleTime = saleTime
                    saleInfoAdd.recorder = request.user
                    saleInfoAdd.isNormal = True
                    # 加密环节
                    timeStrap = bytes(datetime.datetime.now().strftime('%Y-%m-%d %H:%I:%S'), encoding='utf-8')
                    timeStrap_hash = Des_example.encrypt(timeStrap)
                    words = str(current_batch_id) + str(saleTips) + str(float(amount)) + str(saleTime) + str(request.user.holder) + str(timeStrap)
                    saleInfoAdd.hashWords = make_password(words, 'cmy', 'pbkdf2_sha256')
                    saleInfoAdd.TimeStrap = timeStrap_hash
                    saleInfoAdd.Save(request)
                    current_batch.restAmount = current_batch.restAmount - amount
                    current_batch.Save(request)
                    return redirect(reverse('storeInfo'))
                else:
                    member_list = MemberInfo.objects.filter(companyName=request.user.company)
                    error = addForm.errors
                    return render(request, "function/saleManagement/saleInfoAdd.html", {"batch": current_batch,
                                                                                        "member_list": member_list,
                                                                                        "error": error})
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})


class SaleInfoView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        order = request.GET.get("order")
        if not order:
            order = 1
        else:
            order = int(order)
        if request.user.identityClass == 0:
            return render(request, "function/no_permissions.html", {})
        elif request.user.identityClass == 1:
            companyInfo_list = CompanyInfo.objects.all()
            company_current = request.GET.get("company_current")
            if not company_current:
                if companyInfo_list:
                    company_current = companyInfo_list[0].companyID
            else:
                company_current = int(company_current)
            saleInfo_list = SaleInfo.objects.filter(saleBatch__batch__harvestCompany=company_current)
            for saleInfo in saleInfo_list:
                timeStrap = Des_example.decrypt(saleInfo.TimeStrap)
                words = str(saleInfo.saleBatch.id) + str(saleInfo.saleTips) + str(float(saleInfo.amount)) + str(
                    saleInfo.saleTime) + str(saleInfo.recorder.holder) + str(timeStrap)
                if check_password(words, saleInfo.hashWords):
                    saleInfo.isNormal = True
                    saleInfo.save()
                else:
                    saleInfo.isNormal = False
                    saleInfo.save()
            if order == 1:
                saleInfo_list = saleInfo_list.order_by("-saleTime")
            else:
                saleInfo_list = saleInfo_list.order_by("saleTime")
            paginator = Paginator(saleInfo_list, 10)
            page = request.GET.get('page')
            try:
                customer = paginator.page(page)
            except PageNotAnInteger:
                customer = paginator.page(1)
            except EmptyPage:
                customer = paginator.page(paginator.num_pages)
            return render(request, "function/saleManagement/saleInfo.html",
                          {'saleInfo_list': customer, 'saleInfo_list_get': 1,
                           'companyInfo_list': companyInfo_list,
                           "selected_id": company_current,
                           "company_current": company_current,
                           "order": order})
        else:
            saleInfo_list = SaleInfo.objects.filter(saleBatch__batch__harvestCompany=request.user.company)
            # 验证环节
            for saleInfo in saleInfo_list:
                timeStrap = Des_example.decrypt(saleInfo.TimeStrap)
                words = str(saleInfo.saleBatch.id) + str(saleInfo.saleTips) + str(float(saleInfo.amount)) + str(
                    saleInfo.saleTime) + str(saleInfo.recorder.holder) + str(timeStrap)
                if check_password(words, saleInfo.hashWords):
                    saleInfo.isNormal = True
                    saleInfo.save()
                else:
                    saleInfo.isNormal = False
                    saleInfo.save()
            if order == 1:
                saleInfo_list = saleInfo_list.order_by("-saleTime")
            else:
                saleInfo_list = saleInfo_list.order_by("saleTime")
            paginator = Paginator(saleInfo_list, 10)
            page = request.GET.get('page')
            try:
                customer = paginator.page(page)
            except PageNotAnInteger:
                customer = paginator.page(1)
            except EmptyPage:
                customer = paginator.page(paginator.num_pages)
            return render(request, "function/saleManagement/saleInfo.html",
                          {'saleInfo_list': customer, 'saleInfo_list_get': 1, 'order': order})
#     def get(self, request):
#         # 设置是否指定批次的flag
#
#         flag = request.GET.get("pointed")
#         order = request.GET.get("order")
#         if not order:
#             order = 1
#         else:
#             order = int(order)
#         if flag:
#             current_batch_id = request.GET.get("id")
#             current_batch = StoreInfo.objects.get(id=current_batch_id)
#             saleInfo_list = SaleInfo.objects.filter(saleBatch=current_batch)
#             if request.user.identityClass == 1:
#                 # 验证环节
#                 for saleInfo in saleInfo_list:
#                     timeStrap = Des_example.decrypt(saleInfo.TimeStrap)
#                     words = str(saleInfo.saleBatch.id) + str(saleInfo.saleTips) + str(float(saleInfo.amount)) + str(saleInfo.saleTime) + str(saleInfo.recorder.holder) + str(timeStrap)
#                     if check_password(words, saleInfo.hashWords):
#                         saleInfo.isNormal = True
#                         saleInfo.save()
#                     else:
#                         saleInfo.isNormal = False
#                         saleInfo.save()
#                 if order == 1:
#                     saleInfo_list = saleInfo_list.order_by("-saleTime")
#                 else:
#                     saleInfo_list = saleInfo_list.order_by("saleTime")
#                 paginator = Paginator(saleInfo_list, 10)
#                 page = request.GET.get('page')
#                 try:
#                     customer = paginator.page(page)
#                 except PageNotAnInteger:
#                     customer = paginator.page(1)
#                 except EmptyPage:
#                     customer = paginator.page(paginator.num_pages)
#                 return render(request, "function/saleManagement/saleInfo.html",
#                               {'saleInfo_list': customer, 'saleInfo_list_get': 1, 'pointed': 1, 'order': order, 'id': current_batch_id})
#             else:
#                 if not current_batch.batch.harvestCompany == request.user.company:
#                     return render(request, "function/no_permissions.html", {})
#                 # 验证环节
#                 for saleInfo in saleInfo_list:
#                     timeStrap = Des_example.decrypt(saleInfo.TimeStrap)
#                     words = str(saleInfo.saleBatch.id) + str(saleInfo.saleTips) + str(float(saleInfo.amount)) + str(saleInfo.saleTime) + str(saleInfo.recorder.holder) + str(timeStrap)
#                     if check_password(words, saleInfo.hashWords):
#                         saleInfo.isNormal = True
#                         saleInfo.save()
#                     else:
#                         saleInfo.isNormal = False
#                         saleInfo.save()
#                 if order == 1:
#                     saleInfo_list = saleInfo_list.order_by("-saleTime")
#                 else:
#                     saleInfo_list = saleInfo_list.order_by("saleTime")
#                 paginator = Paginator(saleInfo_list, 10)
#                 page = request.GET.get('page')
#                 try:
#                     customer = paginator.page(page)
#                 except PageNotAnInteger:
#                     customer = paginator.page(1)
#                 except EmptyPage:
#                     customer = paginator.page(paginator.num_pages)
#                 return render(request, "function/saleManagement/saleInfo.html",
#                               {'saleInfo_list': customer, 'saleInfo_list_get': 1, 'pointed': 1, 'order': order, 'id': current_batch_id})
#         else:
#             # 系统管理员查看所有公司信息
#             if request.user.identityClass == 1:
#                 companyInfo_list = CompanyInfo.objects.all()
#                 company_current = request.GET.get("company_current")
#                 if not company_current:
#                     if companyInfo_list:
#                         company_current = companyInfo_list[0].companyID
#                 else:
#                     company_current = int(company_current)
#                 saleInfo_list = SaleInfo.objects.filter(saleBatch__batch__harvestCompany=company_current)
#                 for saleInfo in saleInfo_list:
#                     timeStrap = Des_example.decrypt(saleInfo.TimeStrap)
#                     words = str(saleInfo.saleBatch.id) + str(saleInfo.saleTips) + str(float(saleInfo.amount)) + str(saleInfo.saleTime) + str(saleInfo.recorder.holder) + str(timeStrap)
#                     if check_password(words, saleInfo.hashWords):
#                         saleInfo.isNormal = True
#                         saleInfo.save()
#                     else:
#                         saleInfo.isNormal = False
#                         saleInfo.save()
#                 if order == 1:
#                     saleInfo_list = saleInfo_list.order_by("-saleTime")
#                 else:
#                     saleInfo_list = saleInfo_list.order_by("saleTime")
#                 paginator = Paginator(saleInfo_list, 10)
#                 page = request.GET.get('page')
#                 try:
#                     customer = paginator.page(page)
#                 except PageNotAnInteger:
#                     customer = paginator.page(1)
#                 except EmptyPage:
#                     customer = paginator.page(paginator.num_pages)
#                 return render(request, "function/saleManagement/saleInfo.html",
#                               {'saleInfo_list': customer, 'saleInfo_list_get': 1,
#                                'companyInfo_list': companyInfo_list,
#                                "selected_id": company_current,
#                                "company_current": company_current,
#                                "order": order})
#             else:
#                 saleInfo_list = SaleInfo.objects.filter(saleBatch__batch__harvestCompany=request.user.company)
#                 # 验证环节
#                 for saleInfo in saleInfo_list:
#                     timeStrap = Des_example.decrypt(saleInfo.TimeStrap)
#                     words = str(saleInfo.saleBatch.id) + str(saleInfo.saleTips) + str(float(saleInfo.amount)) + str(saleInfo.saleTime) + str(saleInfo.recorder.holder) + str(timeStrap)
#                     if check_password(words, saleInfo.hashWords):
#                         saleInfo.isNormal = True
#                         saleInfo.save()
#                     else:
#                         saleInfo.isNormal = False
#                         saleInfo.save()
#                 if order == 1:
#                     saleInfo_list = saleInfo_list.order_by("-saleTime")
#                 else:
#                     saleInfo_list = saleInfo_list.order_by("saleTime")
#                 paginator = Paginator(saleInfo_list, 10)
#                 page = request.GET.get('page')
#                 try:
#                     customer = paginator.page(page)
#                 except PageNotAnInteger:
#                     customer = paginator.page(1)
#                 except EmptyPage:
#                     customer = paginator.page(paginator.num_pages)
#                 return render(request, "function/saleManagement/saleInfo.html",
#                               {'saleInfo_list': customer, 'saleInfo_list_get': 1, 'pointed': 1, 'order': order})
#
#     @method_decorator(login_required(login_url='/login/'))
#     def post(self, request):
#         pass
#
#
class SaleInfoDetailsView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        flag = request.GET.get("pointed")
        currentInfo_id = request.GET.get("id")
        currentInfo = SaleInfo.objects.get(id=currentInfo_id)
        if flag:
            if request.user.identityClass == 1:
                return render(request, "function/saleManagement/saleInfoDetails.html", {
                    "currentInfo": currentInfo, "pointed": 1})
            else:
                if request.user.company == currentInfo.saleBatch.batch.harvestCompany:
                    return render(request, "function/saleManagement/saleInfoDetails.html",
                                  {"currentInfo": currentInfo, "pointed": 1})
                else:
                    return render(request, "function/no_permissions.html", {})
        else:
            if request.user.identityClass == 1:
                return render(request, "function/saleManagement/saleInfoDetails.html", {
                    "currentInfo": currentInfo})
            else:
                if request.user.company == currentInfo.saleBatch.batch.harvestCompany:
                    return render(request, "function/saleManagement/saleInfoDetails.html",
                                  {"currentInfo": currentInfo})
                else:
                    return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass


class RetrospectInfoView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass == 2:
            rawProduction_list = RawProductionInfo.objects.filter(company=request.user.company)

            current_rawProduction = request.GET.get("current_rawProduction")
            if not current_rawProduction:
                if rawProduction_list:
                    current_rawProduction = rawProduction_list[0]
                else:
                    current_rawProduction = ''
            else:
                current_rawProduction = RawProductionInfo.objects.get(id=current_rawProduction)

            measure_list = RawProductionManagement.objects.filter(Q(company=request.user.company) &
                                                                  Q(rawProductionName=current_rawProduction))
            return render(request, "function/saleManagement/retrospectInfo.html",
                          {'measure_list': measure_list, 'current_rawProduction': current_rawProduction,
                           'rawProduction_list': rawProduction_list})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if request.user.identityClass == 2:
            rawProduction_list = RawProductionInfo.objects.filter(company=request.user.company)
            current_rawProduction = request.POST.get("current_rawProduction")
            current_rawProduction = RawProductionInfo.objects.get(id=current_rawProduction)
            measure_list = RawProductionManagement.objects.filter(Q(company=request.user.company) &
                                                                  Q(rawProductionName=current_rawProduction))
            all_measure = RawProductionManagement.objects.filter(
                Q(company=request.user.company) & Q(rawProductionName=current_rawProduction))
            count = 1
            for measure in all_measure:
                measure.flag = False
                measure.save()
                flag = request.POST.get("option_"+str(count))
                count = count + 1
                if flag:
                    if request.user.company == measure.company:
                        measure.flag = True
                        measure.save()
            return render(request, "function/saleManagement/retrospectInfo.html", {
                "current_rawProduction": current_rawProduction,
                'rawProduction_list': rawProduction_list,
                'measure_list': measure_list})
        else:
            return render(request, "function/no_permissions.html", {})


class QrCodeView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        information_id = request.GET.get("id")
        information = SaleInfo.objects.get(id=information_id)
        sowing_Info = information.saleBatch.batch.harvestBatch
        harvest_Info = information.saleBatch.batch
        measure_list = RawProductionManagement.objects.filter(Q(company=harvest_Info.harvestCompany) &
                                                              Q(rawProductionName=sowing_Info.sowingProduction))
        item_list = ItemCostInfo.objects.filter(costBatch=sowing_Info)

        item_words = ''
        for item in item_list:
            item_words = item_words + '投入品名称：' + str(item.item.itemName) + ' 使用时间：' + str(item.date) + "\n"

        measure_words = ''
        for measure in measure_list:
            if measure.flag:
                measure_info = MeasureConfirmingInfo.objects.get(Q(measure=measure) & Q(sowingBatch=sowing_Info))
                measure_words = measure_words + measure_info.measure.qualityControlMeasure + u"时间:" + str(measure_info.confirmingTime) + u"负责人：" + str(measure_info.recorder.holder) + "\n"

        sowing_words = u"播种时间：" + str(sowing_Info.sowingTime) + u" 负责人：" + str(sowing_Info.sowingMember.memberName) + "\n"
        harvest_words = u"收获时间：" + str(harvest_Info.harvestTime) + u" 负责人：" + str(harvest_Info.harvestMember.memberName) + "\n"

        final_words = sowing_words + measure_words + item_words + harvest_words

        qr_code = pyqrcode.create(final_words, encoding='utf-8')
        buffer = io.BytesIO()
        qr_code.png(buffer, scale=5)
        img_stream = buffer.getvalue()

        return HttpResponse(img_stream, content_type="image/png")

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass
