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
from project520.settings import Des_example

from apps.company.models import CompanyInfo, MemberInfo
from apps.productionManagement.models import SowInfo
from .models import ItemInfo, ItemCostInfo
from .forms import ItemAddForm
# Create your views here.


class ItemInfoView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        # 系统管理员查看所有公司投入品信息
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
            item_list = ItemInfo.objects.filter(company=company_current)
            paginator = Paginator(item_list, 10)
            page = request.GET.get('page')
            try:
                customer = paginator.page(page)
            except PageNotAnInteger:
                customer = paginator.page(1)
            except EmptyPage:
                customer = paginator.page(paginator.num_pages)

            return render(request, "function/itemManagement/itemInfo.html", {'item_list': customer, 'item_list_get': 1, 'companyInfo_list': companyInfo_list, "selected_id": company_current, "company_current": company_current})
        # 系统操作员查看自己及子公司投入品信息
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
                item_list = ItemInfo.objects.filter(company=company_current).order_by("id")

                paginator = Paginator(item_list, 10)
                page = request.GET.get('page')
                try:
                    customer = paginator.page(page)
                except PageNotAnInteger:
                    customer = paginator.page(1)
                except EmptyPage:
                    customer = paginator.page(paginator.num_pages)

                return render(request, "function/itemManagement/itemInfo.html", {'item_list': customer, 'item_list_get': 1, 'companyInfo_list': companyInfo_list, "selected_id": company_current, "company_current": company_current})
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            company_self = request.user.company.companyID
            item_list = ItemInfo.objects.filter(company=company_self)

            paginator = Paginator(item_list, 10)
            page = request.GET.get('page')
            try:
                customer = paginator.page(page)
            except PageNotAnInteger:
                customer = paginator.page(1)
            except EmptyPage:
                customer = paginator.page(paginator.num_pages)

            return render(request, "function/itemManagement/itemInfo.html", {'item_list': customer, 'item_list_get': 1})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass


class ItemInfoAddView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass == 2:
            return render(request, "function/itemManagement/itemInfoAdd.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if request.user.identityClass == 2:
            addForm = ItemAddForm(request.POST)
            if addForm.is_valid():
                itemName = request.POST.get("itemName")
                itemDescription = request.POST.get("itemDescription")
                itemInfo = ItemInfo()
                itemInfo.company = request.user.company
                itemInfo.itemName = itemName
                itemInfo.itemDescription = itemDescription
                itemInfo.Save(request)
                return redirect(reverse("itemInfo"))
            else:
                error = addForm.errors
                return render(request, "function/itemManagement/itemInfoAdd.html", {"error": error})
        else:
            return render(request, "function/no_permissions.html", {})


class ItemInfoUpdateView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass == 2:
            update_item_id = int(request.GET.get('id'))
            update_item = ItemInfo.objects.get(id=update_item_id)
            if update_item.company == request.user.company:
                return render(request, "function/itemManagement/itemInfoUpdate.html", {'update_item': update_item})
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if request.user.identityClass == 2:
            current_item_id = request.POST.get("update_id")
            current_item = ItemInfo.objects.get(id=current_item_id)
            if current_item.company == request.user.company:
                addForm = ItemAddForm(request.POST)
                if addForm.is_valid():
                    itemName = request.POST.get("itemName")
                    itemDescription = request.POST.get("itemDescription")
                    current_item.company = request.user.company
                    current_item.itemName = itemName
                    current_item.itemDescription = itemDescription
                    current_item.Save(request)
                    return redirect(reverse("itemInfo"))
                else:
                    error = addForm.errors
                    return render(request, "function/itemManagement/itemInfoAdd.html", {"error": error})
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})


class ItemInfoDeleteView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        delete_id = int(request.GET.get('id'))
        delete_item = ItemInfo.objects.get(id=delete_id)
        if request.user.identityClass == 2:
            if request.user.company.companyID == delete_item.company.companyID:
                delete_item.Delete(request)
                return redirect(reverse('itemInfo'))
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass


class ItemCostView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        # 系统管理员查看所有公司投入品信息
        if request.user.identityClass==0:
            return render(request, "function/no_permissions.html", {})
        elif request.user.identityClass == 1:
            itemCost_list = ItemCostInfo.objects.all()
            for itemCost in itemCost_list:
                timeStrap = Des_example.decrypt(itemCost.timeStrap)
                words = str(itemCost.item.itemName) + str(itemCost.member.memberName) + str(
                    itemCost.costBatch.sowingName) + str(itemCost.recorder.holder) + str(itemCost.date) + str(timeStrap)
                if check_password(words, itemCost.hashWords):
                    itemCost.isNormal = True
                    itemCost.save()
                else:
                    itemCost.isNormal = False
                    itemCost.save()

            paginator = Paginator(itemCost_list, 10)
            page = request.GET.get('page')
            try:
                customer = paginator.page(page)
            except PageNotAnInteger:
                customer = paginator.page(1)
            except EmptyPage:
                customer = paginator.page(paginator.num_pages)

            return render(request, "function/itemManagement/itemCostInfo.html", {'itemCost_list': customer, 'itemCost_list_get': 1})
        # 系统操作员查看自己及子公司投入品信息
        else:
            company_self = request.user.company.companyID
            itemCost_list = ItemCostInfo.objects.filter(costBatch__sowingCompany=company_self)

            for itemCost in itemCost_list:
                timeStrap = Des_example.decrypt(itemCost.timeStrap)
                words = str(itemCost.item.itemName) + str(itemCost.member.memberName) + str(
                    itemCost.costBatch.sowingName) + str(itemCost.recorder.holder) + str(itemCost.date) + str(timeStrap)
                if check_password(words, itemCost.hashWords):
                    itemCost.isNormal = True
                    itemCost.save()
                else:
                    itemCost.isNormal = False
                    itemCost.save()

            paginator = Paginator(itemCost_list, 10)
            page = request.GET.get('page')
            try:
                customer = paginator.page(page)
            except PageNotAnInteger:
                customer = paginator.page(1)
            except EmptyPage:
                customer = paginator.page(paginator.num_pages)

            return render(request, "function/itemManagement/itemCostInfo.html", {'itemCost_list': customer, 'itemCost_list_get': 1})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass


class ItemCostAddView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass == 1:
            return render(request, "function/no_permissions.html", {})
        else:
            item_list = ItemInfo.objects.filter(company=request.user.company)
            member_list = MemberInfo.objects.filter(companyName=request.user.company)
            batch_list = SowInfo.objects.filter(Q(sowingCompany=request.user.company) & Q(isHarvest=False))
            return render(request, "function/itemManagement/itemCostInfoAdd.html", {"item_list": item_list, "member_list": member_list, "batch_list": batch_list})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if request.user.identityClass == 1:
            return render(request, "function/no_permissions.html", {})
        else:
            item_id = request.POST.get("item")
            costDescription = request.POST.get("costDescription")
            batch_id = request.POST.get("batch")
            member_id = request.POST.get("member")
            date = request.POST.get("date")

            item = ItemInfo.objects.get(id=item_id)
            batch = SowInfo.objects.get(id=batch_id)
            member = MemberInfo.objects.get(memberID=member_id)

            if not item.company == request.user.company:
                return render(request, "function/no_permissions.html", {})
            if not batch.sowingCompany == request.user.company:
                return render(request, "function/no_permissions.html", {})
            if batch.isHarvest:
                return render(request, "function/no_permissions.html", {})
            if not member.companyName == request.user.company:
                return render(request, "function/no_permissions.html", {})

            itemCost = ItemCostInfo()
            itemCost.item = item
            itemCost.member = member
            itemCost.costDescription = costDescription
            itemCost.costBatch = batch
            itemCost.recorder = request.user
            itemCost.date = date
            # hash验证
            timeStrap = bytes(datetime.now().strftime('%Y-%m-%d %H:%I:%S'), encoding='utf-8')
            timeStrap_hash = Des_example.encrypt(timeStrap)
            words = str(item.itemName) + str(member.memberName) + str(batch.sowingName) + str(request.user.holder) + str(
                date) + str(timeStrap)
            itemCost.hashWords = make_password(words, 'cmy', 'pbkdf2_sha256')
            itemCost.timeStrap = timeStrap_hash
            itemCost.Save(request)
            return redirect(reverse("itemCost"))


class ItemCostDeleteView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        delete_id = int(request.GET.get('id'))
        delete_itemCost = ItemCostInfo.objects.get(id=delete_id)
        if request.user.identityClass == 2:
            if request.user.company.companyID == delete_itemCost.costBatch.sowingCompany.companyID:
                delete_itemCost.Delete(request)
                return redirect(reverse('itemCost'))
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass


class ItemCostDetailsView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        cost_id = request.GET.get("id")
        cost = ItemCostInfo.objects.get(id=cost_id)
        batch_id = cost.costBatch.id
        flag = 0
        if request.GET.get("flag"):
            flag = 1
        if flag:
            if cost.costBatch.sowingCompany == request.user.company:
                return render(request, "function/itemManagement/itemCostInfoDetails.html", {"cost": cost, "flag": 1, "batch_id": batch_id })
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            if cost.costBatch.sowingCompany == request.user.company:
                return render(request, "function/itemManagement/itemCostInfoDetails.html", {"cost": cost})
            else:
                return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass


class ItemCostQueryView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        batch_id = request.GET.get("id")
        batch = SowInfo.objects.get(id=batch_id)
        if batch.sowingCompany == request.user.company:
            itemCost_list = ItemCostInfo.objects.filter(costBatch=batch)
            for itemCost in itemCost_list:
                timeStrap = Des_example.decrypt(itemCost.timeStrap)
                words = str(itemCost.item.itemName) + str(itemCost.member.memberName) + str(
                    itemCost.costBatch.sowingName) + str(itemCost.recorder.holder) + str(itemCost.date) + str(timeStrap)
                if check_password(words, itemCost.hashWords):
                    itemCost.isNormal = True
                    itemCost.save()
                else:
                    itemCost.isNormal = False
                    itemCost.save()

            paginator = Paginator(itemCost_list, 10)
            page = request.GET.get('page')
            try:
                customer = paginator.page(page)
            except PageNotAnInteger:
                customer = paginator.page(1)
            except EmptyPage:
                customer = paginator.page(paginator.num_pages)

            return render(request, "function/itemManagement/itemCostQueryInfo.html", {'itemCost_list': customer, 'itemCost_list_get': 1})

        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass
