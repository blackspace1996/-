# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse
# Create your views here.

from .models import SysNews, SysRegulations,UnityInfo
from .forms import NewsAddForm, RegsAddForm


class SystemNewsView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass is not 1:
            return render(request, "function/no_permissions.html")
        SysNews_list = SysNews.objects.all()
        if request.GET.get('order') is not None:
            order = int(request.GET.get('order'))
        else:
            order = 2

        if order == 1:
            SysNews_list = SysNews_list.order_by('createTime')

        elif order == 2:
            SysNews_list = SysNews_list.order_by('-createTime')

        elif order == 3:
            SysNews_list = SysNews_list.order_by('updateTime')

        else:
            SysNews_list = SysNews_list.order_by('-updateTime')

        paginator = Paginator(SysNews_list, 10)
        page = request.GET.get('page')
        try:
            customer = paginator.page(page)
        except PageNotAnInteger:
            customer = paginator.page(1)
        except EmptyPage:
            customer = paginator.page(paginator.num_pages)
        return render(request, 'function/systemManagement/systemNews.html', {'SysNews_list': customer, 'order': order})

    def post(self, request):
        pass


class SystemNewsAddView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass is not 1:
            return render(request, "function/no_permissions.html")
        unity_list = UnityInfo.objects.all()
        return render(request, 'function/systemManagement/systemNewsAdd.html', {'unity_list':unity_list})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        # if request.user.identityClass is not 1:
        #     return render(request, "function/no_permissions.html")
        addForm = NewsAddForm(request.POST)
        unity_list = UnityInfo.objects.all()
        if addForm.is_valid():
            NewsTitle = request.POST.get('NewsTitle')
            NewsDescrption = request.POST.get('NewsDescription')
            unityID= request.POST.get('unityID')
            sysNews = SysNews()
            sysNews.title = NewsTitle
            sysNews.description = NewsDescrption
            sysNews.unity=UnityInfo.objects.get(unityID=unityID)
            sysNews.Save(request)
            return redirect(reverse("systemNews"))
        else:
            error = addForm.errors
            return render(request, "function/systemManagement/systemNewsAdd.html", {"error": error,'unity_list':unity_list})


class SystemNewsUpdateView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass is not 1:
            return render(request, "function/no_permissions.html")
        news_id = request.GET.get('id')
        news_update = SysNews.objects.get(id=news_id)
        unity_list = UnityInfo.objects.all()
        return render(request, "function/systemManagement/systemNewsUpdate.html", {"raw_news": news_update,'unity_list':unity_list})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if request.user.identityClass is not 1:
            return render(request, "function/no_permissions.html")
        addForm = NewsAddForm(request.POST)
        unity_list = UnityInfo.objects.all()
        if addForm.is_valid():
            news_id = int(request.POST.get('update_id'))
            news_update = SysNews.objects.get(id=news_id)
            news_update.title = request.POST.get('NewsTitle')
            news_update.description = request.POST.get('NewsDescription')
            news_update.Save(request)
            raw_news = SysNews.objects.get(id=news_id)
            return render(request, "function/systemManagement/systemNewsUpdate.html", {"raw_news": raw_news, "success":1,'unity_list':unity_list})
        else:
            news_id = int(request.POST.get('update_id'))
            raw_news = SysNews.objects.get(id=news_id)
            error = addForm.errors
            return render(request, "function/systemManagement/systemNewsUpdate.html", {"raw_news": raw_news, "error": error,'unity_list':unity_list})


class SystemNewsDeleteView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass is not 1:
            return render(request, "function/no_permissions.html")
        delete_id = int(request.GET.get('id'))
        SysNews.objects.get(id=delete_id).Delete(request)

        return redirect(reverse('systemNews'))

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass


class SystemNewsDetailsView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass is not 1:
            return render(request, "function/no_permissions.html")
        news_id = request.GET.get('id')
        currentNews = SysNews.objects.get(id=news_id)
        return render(request, "function/systemManagement/systemNewsDetails.html", {"currentNews": currentNews})

    def post(self, request):
        pass


class SystemRegsView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass is not 1:
            return render(request, "function/no_permissions.html")
        SysRegs_list = SysRegulations.objects.all()
        if request.GET.get('order') is not None:
            order = int(request.GET.get('order'))
        else:
            order = 2

        if order == 1:
            SysRegs_list = SysRegs_list.order_by('createTime')

        elif order == 2:
            SysRegs_list = SysRegs_list.order_by('-createTime')

        elif order == 3:
            SysRegs_list = SysRegs_list.order_by('updateTime')

        else:
            SysRegs_list = SysRegs_list.order_by('-updateTime')

        paginator = Paginator(SysRegs_list, 10)
        page = request.GET.get('page')
        try:
            customer = paginator.page(page)
        except PageNotAnInteger:
            customer = paginator.page(1)
        except EmptyPage:
            customer = paginator.page(paginator.num_pages)
        return render(request, 'function/systemManagement/systemRegs.html', {'SysRegs_list': customer, 'order': order})

    def post(self, request):
        pass


class SystemRegsAddView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass is not 1:
            return render(request, "function/no_permissions.html")
        unity_list=UnityInfo.objects.all()
        return render(request, 'function/systemManagement/systemRegsAdd.html', {'unity_list':unity_list})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if request.user.identityClass is not 1:
            return render(request, "function/no_permissions.html")
        addForm = RegsAddForm(request.POST)
        unity_list = UnityInfo.objects.all()
        if addForm.is_valid():
            RegsTitle = request.POST.get('RegsTitle')
            RegsDescrption = request.POST.get('RegsDescription')
            sysRegs = SysRegulations()
            sysRegs.regName = RegsTitle
            sysRegs.regDescription = RegsDescrption
            sysRegs.Save(request)
            return redirect(reverse("systemRegs"))
        else:
            error = addForm.errors
            return render(request, "function/systemManagement/systemRegsAdd.html", {"error": error,'unity_list':unity_list})


class SystemRegsUpdateView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass is not 1:
            return render(request, "function/no_permissions.html")
        regs_id = request.GET.get('id')
        regs_update = SysRegulations.objects.get(id=regs_id)
        unity_list = UnityInfo.objects.all()
        return render(request, "function/systemManagement/systemRegsUpdate.html", {"raw_regs": regs_update,'unity_list':unity_list})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if request.user.identityClass is not 1:
            return render(request, "function/no_permissions.html")
        addForm = RegsAddForm(request.POST)
        unity_list = UnityInfo.objects.all()
        if addForm.is_valid():
            regs_id = int(request.POST.get('update_id'))
            regs_update = SysRegulations.objects.get(id=regs_id)
            regs_update.regName = request.POST.get('RegsTitle')
            regs_update.regDescription = request.POST.get('RegsDescription')
            regs_update.Save(request)
            raw_regs = SysRegulations.objects.get(id=regs_id)
            return render(request, "function/systemManagement/systemRegsUpdate.html", {"raw_regs": raw_regs, "success": 1,'unity_list':unity_list})
        else:
            regs_id = int(request.POST.get('update_id'))
            raw_regs = SysRegulations.objects.get(id=regs_id)
            error = addForm.errors
            return render(request, "function/systemManagement/systemRegsUpdate.html", {"raw_regs": raw_regs, "error": error,'unity_list':unity_list})


class SystemRegsDeleteView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass is not 1:
            return render(request, "function/no_permissions.html")
        delete_id = int(request.GET.get('id'))
        SysRegulations.objects.get(id=delete_id).Delete(request)

        return redirect(reverse('systemRegs'))

    def post(self, request):
        pass


class SystemRegsDetailsView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass is not 1:
            return render(request, "function/no_permissions.html")
        regs_id = request.GET.get('id')
        currentRegs = SysRegulations.objects.get(id=regs_id)
        return render(request, "function/systemManagement/systemRegsDetails.html", {"currentNews": currentRegs})

    def post(self, request):
        pass


class ImageUploadView(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self,request):
        pass

    def post(self,request):
        if request.user.identityClass is not 0:
            response = JsonResponse({
                "error":{
                    "message":"权限不足"
                }
            })
            return response
        image=request.FILES.get('upload')
        imagename=image.name
        f = open('static/img/NewsImage/'+imagename, 'ab')
        for chunk in image.chunks():
            f.write(chunk)
        f.close()
        response = JsonResponse({
                "fileName":imagename,
                "uploaded":1,
                "url": "/static/img/NewsImage/"+imagename,
            })

        return response