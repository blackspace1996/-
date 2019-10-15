from django.shortcuts import render
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import Group, Permission
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from apps.company.models import CompanyInfo
from .forms import UsersAddForm
from apps.users.models import UserProfile
from apps.unity.models import UnityInfo


# Create your views here.


class UserListView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        # 系统管理员可以看到所有账号,系统操作员可以看到自己公司的所有账号,无法看到自己子公司的所有帐号
        global user_list
        if request.GET.get('id') is not None:
            if request.user.identityClass == 0:
                user_list = UserProfile.objects.filter(is_active=1).filter(id=request.user.id).filter(identityClass=1)
            elif request.user.identityClass == 1:
                user_list = UserProfile.objects.filter(is_active=1).filter(unityID=request.user.company.unityID).filter(
                    id=request.user.id)
            elif request.user.identityClass == 2:
                user_list = UserProfile.objects.filter(is_active=1).filter(company=request.user.company).filter(
                    id=request.user.id)
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            if request.user.identityClass == 0:
                user_list = UserProfile.objects.filter(is_active=1).filter(identityClass=1)
            elif request.user.identityClass == 1:
                user_list = UserProfile.objects.filter(is_active=1).filter(unityID=request.user.unityID)
            elif request.user.identityClass == 2:
                user_list = UserProfile.objects.filter(is_active=1).filter(company=request.user.company)
            else:
                return render(request, "function/no_permissions.html", {})

        if request.GET.get('order') is not None:
            order = int(request.GET.get('order'))
        else:
            order = 2

        if order == 1:
            user_list = user_list.order_by('date_joined')

        elif order == 2:
            user_list = user_list.order_by('-date_joined')

        paginator = Paginator(user_list, 10)  # 分页器
        page = request.GET.get('page')
        try:
            customer = paginator.page(page)
        except PageNotAnInteger:
            customer = paginator.page(1)
        except EmptyPage:
            customer = paginator.page(paginator.num_pages)

        return render(request, "function/userManagement/userList.html", {'user_list': customer, 'order': order})

    def post(self, request):
        pass


class DistributeUserView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass == 1:
            company_list = CompanyInfo.objects.filter(unityID=request.user.unityID)
            return render(request, "function/userManagement/distributeUser.html", {"company_list": company_list})
        elif request.user.identityClass == 2:
            company_list = CompanyInfo.objects.filter(unityID=request.user.company.unityID)
            return render(request, "function/userManagement/distributeUser.html", {"company_list": company_list})
        elif request.user.identityClass == 0:
            unity_list = UnityInfo.objects.all()
            return render(request, "function/userManagement/distributeUser.html", {"unity_list": unity_list})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        username = request.POST.get("username")
        identityClass = request.POST.get("identityClass")
        sub_company_list = CompanyInfo.objects.filter(superCompany=request.user.company)
        addForm = UsersAddForm(request.POST)
        if UserProfile.objects.filter(username=username).exists():
            if request.user.identityClass == 1:
                company_list = CompanyInfo.objects.filter(unityID=request.user.unityID)
                return render(request, "function/userManagement/distributeUser.html",
                              {"usernameError": 1, "company_list": company_list})
            elif request.user.identityClass == 2:
                company_list = CompanyInfo.objects.filter(unityID=request.user.company)
                return render(request, "function/userManagement/distributeUser.html",
                              {"usernameError": 1, "company_list": company_list})
            elif request.user.identityClass == 0:
                unity_list = UnityInfo.objects.all()
                return render(request, "function/userManagement/distributeUser.html",
                              {"usernameError": 1, "unity_list": unity_list})
        elif addForm.is_valid():
            password = request.POST.get("password")
            holder = request.POST.get("holder")
            new_user = UserProfile()
            new_user.username = username
            new_user.password = make_password(password)
            new_user.is_staff = 0
            new_user.holder = holder
            if request.user.identityClass==0:
                new_user.unityID=UnityInfo.objects.get(unityID=request.POST.get("company"))
            else:
                new_user.company = CompanyInfo.objects.get(companyID=request.POST.get("company"))
                new_user.unityID=new_user.company.unityID
            new_user.identityClass = identityClass
            new_user.Save(request)
            return redirect(reverse("userList"))
        else:
            error = addForm.errors
            if request.user.identityClass == 1:
                company_list = CompanyInfo.objects.filter(unityID=request.user.unityID)
                return render(request, "function/userManagement/distributeUser.html",
                              {"error": error, "company_list": company_list, "sub_company_list": sub_company_list})
            elif request.user.identityClass == 2:
                company_list = CompanyInfo.objects.filter(unityID=request.user.company)
                return render(request, "function/userManagement/distributeUser.html",
                              {"error": error, "company_list": company_list, "sub_company_list": sub_company_list})
            elif request.user.identityClass == 0:
                unity_list = UnityInfo.objects.all()
                return render(request, "function/userManagement/distributeUser.html",
                              {"error": error, "unity_list": unity_list, "sub_company_list": sub_company_list})


class UserInfoDeleteView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        delete_id = int(request.GET.get('id'))
        if request.user.identityClass == 1 or 0:
            delete_user = UserProfile.objects.get(id=delete_id)
            delete_user.is_active = False
            delete_user.Save(request)
            return redirect(reverse('userList'))
        elif request.user.identityClass == 2:
            if UserProfile.objects.get(id=delete_id).company.companyID == request.user.company.companyID:
                if not UserProfile.objects.get(id=delete_id).id == request.user.id:
                    delete_user = UserProfile.objects.get(id=delete_id)
                    delete_user.is_active = False
                    delete_user.Save(request)
                    return redirect(reverse('userList'))
                else:
                    return render(request, "function/no_permissions.html", {})
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    def post(self, request):
        pass


class UpdatePwd(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
            return render(request, "function/userManagement/updatePwd.html", {})


    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        username_update = request.user.username
        password_raw = request.POST.get("rawPwd")
        password_new = request.POST.get("newPwd")
        user = authenticate(username=username_update, password=password_raw)
        if user:
            user.set_password(password_new)
            user.Save(request)
            return redirect(reverse("logout"))
        else:
            return render(request, "function/userManagement/updatePwd.html", {"error": "error"})


class ResetPwd(View):

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if request.user.identityClass == 2 or 1 or 0:
            password_new = request.POST.get("newPwd")
            id= request.POST.get('user_id')
            user = UserProfile.objects.get(id=id)
            user.set_password(password_new)
            user.Save(request)
            return JsonResponse({"url": "/userManagement/userList/"})
        else:
            return render(request, "function/userManagement/updatePwd.html", {})
