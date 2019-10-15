# _*_encoding:utf-8_*_
from django.shortcuts import render
from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q

from .forms import CompanyTaskAddForm, PersonTaskAddForm
from .models import CompanyTaskInfo, CompanyTaskReceiveInfo
from .models import PersonTaskInfo
from .models import UnityInfo
from apps.users.models import UserProfile


# Create your views here.


class TaskInfo(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass == 1:
            taskInfo_list = CompanyTaskInfo.objects.all()
            if request.GET.get('order') is not None:
                order = int(request.GET.get('order'))
            else:
                order = 2

            if order == 1:
                taskInfo_list = taskInfo_list.order_by('deadline')

            elif order == 2:
                taskInfo_list = taskInfo_list.order_by('-deadline')

            paginator = Paginator(taskInfo_list, 10)
            page = request.GET.get('page')
            try:
                customer = paginator.page(page)
            except PageNotAnInteger:
                customer = paginator.page(1)
            except EmptyPage:
                customer = paginator.page(paginator.num_pages)

            return render(request, "function/taskManagement/taskInfo.html",
                          {'taskInfo_list': customer, 'order': order})
        elif request.user.identityClass == 2:
            taskType = request.GET.get('taskType')
            receiving = request.GET.get('receiving')
            order = request.GET.get('order')
            if not taskType:
                taskType = 'Company'
            if not receiving:
                receiving = 'false'
            if not order:
                order = 2
            else:
                order = int(request.GET.get('order'))

            if taskType == 'Company':
                if receiving == 'false':
                    taskInfo_list = CompanyTaskInfo.objects.filter(unityID=request.user.company.unityID)
                    if order == 1:
                        taskInfo_list = taskInfo_list.order_by('deadline')

                    elif order == 2:
                        taskInfo_list = taskInfo_list.order_by('-deadline')

                    paginator = Paginator(taskInfo_list, 10)
                    page = request.GET.get('page')
                    try:
                        customer = paginator.page(page)
                    except PageNotAnInteger:
                        customer = paginator.page(1)
                    except EmptyPage:
                        customer = paginator.page(paginator.num_pages)

                    return render(request, "function/taskManagement/taskInfo.html",
                                  {'taskInfo_list': customer, 'order': order, 'taskType': 'Company'})
                else:
                    taskInfo_filter_list = CompanyTaskReceiveInfo.objects.filter(receiver=request.user.company)
                    if order == 1:
                        taskInfo_filter_list = taskInfo_filter_list.order_by('receivingTime')

                    elif order == 2:
                        taskInfo_filter_list = taskInfo_filter_list.order_by('-receivingTime')

                    paginator = Paginator(taskInfo_filter_list, 10)
                    page = request.GET.get('page')
                    try:
                        customer = paginator.page(page)
                    except PageNotAnInteger:
                        customer = paginator.page(1)
                    except EmptyPage:
                        customer = paginator.page(paginator.num_pages)

                    return render(request, "function/taskManagement/taskInfo.html",
                                  {'taskInfo_filter_list': customer, 'order': order, 'receiving': 1,
                                   'taskType': taskType})

            else:
                personTask_list = PersonTaskInfo.objects.filter(company=request.user.company)
                if order == 1:
                    personTask_list = personTask_list.order_by('deadline')

                elif order == 2:
                    personTask_list = personTask_list.order_by('-deadline')

                paginator = Paginator(personTask_list, 10)
                page = request.GET.get('page')
                try:
                    customer = paginator.page(page)
                except PageNotAnInteger:
                    customer = paginator.page(1)
                except EmptyPage:
                    customer = paginator.page(paginator.num_pages)
                return render(request, 'function/taskManagement/taskInfo.html',
                              {'taskType': 'Person', 'order': order, 'personTask_list': customer})
        elif request.user.identityClass == 3:
            taskInfo_list = PersonTaskInfo.objects.filter(Q(receiver=request.user) & Q(company=request.user.company))
            if request.GET.get('order') is not None:
                order = int(request.GET.get('order'))
            else:
                order = 2

            if order == 1:
                taskInfo_list = taskInfo_list.order_by('deadline')

            elif order == 2:
                taskInfo_list = taskInfo_list.order_by('-deadline')

            paginator = Paginator(taskInfo_list, 10)
            page = request.GET.get('page')
            try:
                customer = paginator.page(page)
            except PageNotAnInteger:
                customer = paginator.page(1)
            except EmptyPage:
                customer = paginator.page(paginator.num_pages)

            return render(request, "function/taskManagement/taskInfo.html",
                          {'taskInfo_list': customer, 'order': order})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass


class TaskInfoDetails(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        task_id = int(request.GET.get('id'))
        if request.user.identityClass == 1:
            currentInfo = CompanyTaskInfo.objects.get(id=task_id)
            return render(request, "function/taskManagement/taskInfoDetails.html", {"currentInfo": currentInfo})
        elif request.user.identityClass == 2:
            isPerson = request.GET.get('isPerson')
            if not isPerson:
                currentInfo = CompanyTaskInfo.objects.get(id=task_id)
                try:
                    query = CompanyTaskReceiveInfo.objects.get(Q(task=currentInfo) & Q(receiver=request.user.company))
                except CompanyTaskReceiveInfo.DoesNotExist:
                    query = ''

                if query:
                    currentInfo = CompanyTaskInfo.objects.get(id=task_id)
                    return render(request, "function/taskManagement/taskInfoDetails.html",
                                  {"currentInfo": currentInfo, 'exist': '1'})
                else:
                    return render(request, "function/taskManagement/taskInfoDetails.html",
                                  {"currentInfo": currentInfo, 'exist': ''})
            else:
                currentInfo = PersonTaskInfo.objects.get(id=task_id)
                if currentInfo.company == request.user.company:
                    return render(request, "function/taskManagement/taskInfoDetails.html",
                                  {"currentInfo": currentInfo, "isPerson": '1'})
                else:
                    return render(request, "function/no_permissions.html", {})
        else:
            currentInfo = PersonTaskInfo.objects.get(id=task_id)
            if currentInfo.receiver == request.user:
                return render(request, "function/taskManagement/taskInfoDetails.html",
                              {"currentInfo": currentInfo, "isPerson": '1'})
            else:
                return render(request, "function/no_permissions.html", {})

    def post(self, request):
        pass


class TaskInfoUpdate(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        task_id = int(request.GET.get('id'))
        if request.user.identityClass == 1:
            task_update = CompanyTaskInfo.objects.get(id=task_id)
            return render(request, "function/taskManagement/taskInfoUpdate.html", {"raw_taskInfo": task_update})
        elif request.user.identityClass == 2:
            pass
        else:
            pass

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        if request.user.identityClass == 1:
            taskID = int(request.POST.get('update_id'))
            addForm = CompanyTaskAddForm(request.POST)
            if addForm.is_valid():
                taskName = request.POST.get('taskName')
                taskDescription = request.POST.get('taskDescription')
                deadline = request.POST.get('deadline')
                companyTaskInfo = CompanyTaskInfo.objects.get(id=taskID)
                companyTaskInfo.taskName = taskName
                companyTaskInfo.taskDescription = taskDescription
                companyTaskInfo.deadline = deadline
                companyTaskInfo.Save(request)
                return redirect(reverse("taskInfo"))
            else:
                taskID = int(request.POST.get('update_id'))
                raw_taskInfo = CompanyTaskInfo.objects.get(id=taskID)
                error = addForm.errors
                return render(request, "function/taskManagement/taskInfoUpdate.html",
                              {"raw_taskInfo": raw_taskInfo, "error": error})
        elif request.user.identityClass == 2:
            pass
        else:
            return render(request, "function/no_permissions.html", {})


class TaskInfoDelete(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        delete_id = int(request.GET.get('id'))
        if request.user.identityClass == 1:
            CompanyTaskInfo.objects.get(id=delete_id).Delete(request)
            return redirect(reverse('taskInfo'))
        elif request.user.identityClass == 2:
            delete_info = PersonTaskInfo.objects.get(id=delete_id)
            if delete_info.company == request.user.company:
                delete_info.Delete(request)
                return redirect(reverse('taskInfo'))
            else:
                return render(request, "function/no_permissions.html", {})
        else:
            return render(request, "function/no_permissions.html", {})

    def post(self, request):
        pass


class TaskDistributing(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass == 1:
            unity_list = UnityInfo.objects.all()
            return render(request, "function/taskManagement/taskDistributing.html", {'unity_list': unity_list})
        elif request.user.identityClass == 2:
            member_list = UserProfile.objects.filter(
                Q(company=request.user.company) & Q(is_active=1) & Q(identityClass=3))
            return render(request, "function/taskManagement/taskDistributing.html", {'member_list': member_list})
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        # 系统管理员分发公司级别的任务
        if request.user.identityClass == 1:
            addForm = CompanyTaskAddForm(request.POST)
            unity_list = UnityInfo.objects.all()
            if addForm.is_valid():
                taskName = request.POST.get('taskName')
                taskDescription = request.POST.get('taskDescription')
                deadline = request.POST.get('deadline')
                unityID = request.POST.get('unityID')
                companyTaskInfo = CompanyTaskInfo()
                companyTaskInfo.taskName = taskName
                companyTaskInfo.taskDescription = taskDescription
                companyTaskInfo.deadline = deadline
                companyTaskInfo.unityID = UnityInfo.objects.get(unityID=unityID)
                companyTaskInfo.Save(request)
                return redirect(reverse("taskInfo"))
            else:
                error = addForm.errors
                return render(request, "function/taskManagement/taskDistributing.html",
                              {'error': error, 'unity_list': unity_list})

        elif request.user.identityClass == 2:
            addForm = PersonTaskAddForm(request.POST)
            if addForm.is_valid():
                taskName = request.POST.get('taskName')
                receiverID = request.POST.get('receiver')
                taskDescription = request.POST.get('taskDescription')
                deadline = request.POST.get('deadline')
                personTaskInfo = PersonTaskInfo()
                personTaskInfo.taskName = taskName
                receiver = UserProfile.objects.get(id=receiverID)
                if receiver.company == request.user.company:
                    personTaskInfo.receiver = receiver
                personTaskInfo.company = request.user.company
                personTaskInfo.taskDescription = taskDescription
                personTaskInfo.deadline = deadline
                personTaskInfo.isRead = False
                personTaskInfo.Save(request)
                return redirect(reverse("taskInfo"))
            else:
                error = addForm.errors
                member_list = UserProfile.objects.filter(Q(company=request.user.company) & Q(is_active=1))
                return render(request, "function/taskManagement/taskDistributing.html",
                              {'error': error, 'member_list': member_list})

        else:
            return render(request, "function/no_permissions.html", {})


class TaskReceivingInfo(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass == 1:
            task_id = request.GET.get('id')
            task = CompanyTaskInfo.objects.get(id=task_id)
            currentInfo_list = CompanyTaskReceiveInfo.objects.filter(task=task)
            return render(request, "function/taskManagement/taskReceivingInfo.html",
                          {"currentInfo_list": currentInfo_list})
        elif request.user.identityClass == 2:
            pass
        else:
            pass

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass


class ReceivingCompanyTask(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass == 2:
            task_id = request.GET.get('id')
            task = CompanyTaskInfo.objects.get(id=task_id)
            try:
                query = CompanyTaskReceiveInfo.objects.get(Q(task=task) & Q(receiver=request.user.company))
            except CompanyTaskReceiveInfo.DoesNotExist:
                query = ''

            if query:
                currentInfo_list = CompanyTaskReceiveInfo.objects.filter(task=task)
                return render(request, "function/taskManagement/taskReceivingInfo.html",
                              {"currentInfo_list": currentInfo_list, 'exist': '1'})
            else:
                record = CompanyTaskReceiveInfo()
                record.task = task
                record.receiver = request.user.company
                record.save()
                return redirect(reverse('taskInfo'))

        else:
            pass

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass


class ReceivingPersonTask(View):
    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        if request.user.identityClass == 3:
            task_id = request.GET.get('id')
            task = PersonTaskInfo.objects.get(id=task_id)
            if task.receiver == request.user:
                task.isRead = True
                task.save()
                return redirect(reverse('taskInfo'))
        else:
            return render(request, "function/no_permissions.html", {})

    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        pass
