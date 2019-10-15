from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


class NoPermissionsView(View):
    def get(self, request):
        return render(request, "function/no_permissions.html", {})

    def post(self, request):
        pass