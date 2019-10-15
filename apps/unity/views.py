from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from apps.unity.models import UnityInfo
from apps.unity.forms import UnityAddForm
from apps.company.models import CompanyInfo
# Create your views here.


class UnityInfoView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self,request):
        if request.user.identityClass == 0:
            unityInfo_list = UnityInfo.objects.all()
            paginator = Paginator(unityInfo_list, 10)
            page = request.GET.get('page')

            try:
                customer = paginator.page(page)
            except PageNotAnInteger:
                customer = paginator.page(1)
            except EmptyPage:
                customer = paginator.page(paginator.num_pages)

            return render(request, "function/unityManagement/unityInfo.html",
                          {'unityInfo_list': customer})
        else:
            return render(request, "function/no_permissions.html", {})


class UnityInfoAddView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self,request):
        return render(request, "function/unityManagement/unityInfoAdd.html")

    def post(self,request):

        addForm = UnityAddForm(request.POST)
        if request.user.identityClass == 0:
            if addForm.is_valid():
                unityName = request.POST.get('unityName')
                unityProfile = request.POST.get('unityProfile')
                unity = UnityInfo()
                unity.unityName = unityName
                unity.unityProfile=unityProfile
                unity.Save(request)

                return redirect(reverse("unityInfo"))

            else:
                error = addForm.errors
                return render(request, "function/unityManagement/unityInfoAdd.html",
                              {"error": error})
        else:
            return render(request, "function/no_permissions.html", {})


class UnityInfoDeleteView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        delete_id = int(request.GET.get('id'))
        if request.user.identityClass == 0:
            UnityInfo.objects.get(unityID=delete_id).Delete(request)
            return redirect(reverse('unityInfo'))
        else:
            return render(request, "function/no_permissions.html", {})


class UnityInfoUpdateView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self,request):
        unity_id = int(request.GET.get('id'))
        if request.user.identityClass == 0:
            unityInfo_update = UnityInfo.objects.get(unityID=unity_id)
            return render(request, "function/unityManagement/unityInfoUpdate.html",
                          {"raw_unityInfo": unityInfo_update})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        unityID = int(request.POST.get('update_id'))
        if request.user.identityClass == 0:
            addForm = UnityAddForm(request.POST)
            if addForm.is_valid():
                unityInfo_update = UnityInfo.objects.get(unityID=unityID)
                unityInfo_update.unityName = request.POST.get('unityName')
                unityInfo_update.unityProfile=request.POST.get('unityProfile')
                unityInfo_update.Save(request)
                return redirect(reverse("unityInfo"))
            else:
                unityID = int(request.POST.get('update_id'))
                raw_unityInfo = UnityInfo.objects.get(unityID=unityID)
                error = addForm.errors
                return render(request, "function/unityManagement/unityInfoUpdate.html",
                              {"raw_unityInfo": raw_unityInfo, "error": error})
        else:
            return render(request, "function/no_permissions.html", {})


class UnityInfoDetailsView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self,request):
        unity_id = int(request.GET.get('id'))
        if request.user.identityClass == 0:
            companyInfo_list= CompanyInfo.objects.filter(unityID=unity_id)

            return render(request, "function/unityManagement/unityInfoDetails.html", {"companyInfo_list":companyInfo_list})

        else:
            return render(request, "function/no_permissions.html", {})

