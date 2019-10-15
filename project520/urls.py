"""Agriculture URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.urls import include
from django.views.static import serve

import xadmin
from captcha import views

from project520.settings import MEDIA_ROOT, STATIC_ROOT
from apps.error.views import NoPermissionsView
from apps.welcome.views import Welcome, ListView, NewsDetail, RegsDetail
from apps.login.views import LoginView, LogoutView, UserWelcomeView
from apps.systemInfo.views import ImageUploadView
from apps.systemInfo.views import SystemNewsView, SystemNewsAddView, SystemNewsUpdateView, SystemNewsDeleteView, SystemNewsDetailsView
from apps.systemInfo.views import SystemRegsView, SystemRegsAddView, SystemRegsUpdateView, SystemRegsDeleteView, SystemRegsDetailsView
from apps.company.views import CompanyInfoView, CompanyInfoAddView, CompanyInfoUpdateView, CompanyInfoDeleteView, CompanyInfoDetailsView
from apps.company.views import MemberInfoView, MemberInfoAddView, MemberInfoDeleteView, MemberInfoDetailsView, MemberInfoUpdateView
from apps.company.views import EquipmentInfoView, EquipmentInfoAddView, EquipmentInfoDetailsView, EquipmentInfoUpdateView, EquipmentInfoDeleteView
from apps.company.views import BlockInfoView, BlockInfoAddView, BlockInfoDeleteView, BlockInfoDetailsView, BlockInfoUpdateView
from apps.company.views import EquipmentShareInfoView
from apps.userManagement.views import UserListView, DistributeUserView, UserInfoDeleteView, UpdatePwd,ResetPwd
from apps.taskManagement.views import TaskInfo, TaskInfoUpdate, TaskInfoDelete, TaskInfoDetails, TaskDistributing
from apps.taskManagement.views import TaskReceivingInfo, ReceivingCompanyTask, ReceivingPersonTask
from apps.rawProduction.views import RawProductionInfoView, RawProductionInfoAddView, RawProductionInfoDeleteView, \
    RawProductionInfoDetailsView, RawProductionInfoUpdateView
from apps.rawProduction.views import RawProductionMeasureInfoView, RawProductionMeasureInfoAddView, \
    RawProductionMeasureInfoUpdateView, RawProductionMeasureInfoDeleteView, RawProductionMeasureInfoDetailsView,\
    RawProductionMeasureSort
from apps.productionManagement.views import SowingInfoView, SowingInfoAddView, SowingInfoDeleteView, SowingInfoDetailsView
from apps.productionManagement.views import MeasuresConfirmingView, MeasureConfirmingCompleteView, MeasureConfirmingDetailsView
from apps.productionManagement.views import HarvestInfoAddView, HarvestInfoView, HarvestInfoDetailsView
from apps.productionStore.views import StoreInfoAddView, StoreInfoView, StoreInfoDetailsView
from apps.saleManagement.views import SaleInfoAddView, SaleInfoView, SaleInfoDetailsView, RetrospectInfoView, QrCodeView
from apps.costManagement.views import CostManagementInfoView, CostManagementInfoAddView, CostManagementInfoDetailsView
from apps.itemStore.views import ItemInfoView, ItemInfoAddView, ItemInfoUpdateView, ItemInfoDeleteView
from apps.itemStore.views import ItemCostView, ItemCostAddView, ItemCostDeleteView, ItemCostDetailsView, ItemCostQueryView
from apps.log.views import logInfo
from apps.unity.views import UnityInfoView, UnityInfoAddView,UnityInfoDeleteView,UnityInfoUpdateView,UnityInfoDetailsView



urlpatterns = [
    path(r'xadmin/', xadmin.site.urls),
    # 无权限
    path(r'no_permissions/', NoPermissionsView.as_view(), name="noPermissions"),
    # 页面配置
    path(r'', Welcome.as_view(), name="index"),
    path(r'list/', ListView.as_view(), name="list"),
    path(r'NewsDetails', NewsDetail.as_view(), name="NewsDetails"),
    path(r'RegsDetails', RegsDetail.as_view(), name="RegsDetails"),
    path(r'imageUpload/', ImageUploadView.as_view(), name="ImageUpload"),
    # 登陆界面配置
    path(r'login/', LoginView.as_view(), name='login'),
    path(r'captcha/', include('captcha.urls')),
    path(r'refresh/', views.captcha_refresh, name='captcha-refresh'),
    path(r'welcome/', UserWelcomeView.as_view(), name='userWelcome'),
    # 注销配置
    path(r'logout/', LogoutView.as_view(), name='logout'),
    # 信息展示模块配置
    path(r'systemManagement/systemNews/', SystemNewsView.as_view(), name='systemNews'),
    path(r'systemManagement/systemNewsAdd/', SystemNewsAddView.as_view(), name='systemNewsAdd'),
    path(r'systemManagement/systemNewsUpdate/', SystemNewsUpdateView.as_view(), name='systemNewsUpdate'),
    path(r'systemManagement/systemNewsDelete/', SystemNewsDeleteView.as_view(), name='systemNewsDelete'),
    path(r'systemManagement/systemNewsDetails/', SystemNewsDetailsView.as_view(), name='systemNewsDetails'),
    path(r'systemManagement/systemRegs/', SystemRegsView.as_view(), name="systemRegs"),
    path(r'systemManagement/systemRegsAdd/', SystemRegsAddView.as_view(), name="systemRegsAdd"),
    path(r'systemManagement/systemRegsUpdate/', SystemRegsUpdateView.as_view(), name="systemRegsUpdate"),
    path(r'systemManagement/systemRegsDetails/', SystemRegsDetailsView.as_view(), name="systemRegsDetails"),
    path(r'systemManagement/systemRegsDelete/', SystemRegsDeleteView.as_view(), name="systemRegsDelete"),
    # 联盟管理
    path(r'unityManagement/unityInfo/', UnityInfoView.as_view(), name="unityInfo"),
    path(r'unitManagement/unityInfoAdd/', UnityInfoAddView.as_view(), name='unityInfoAdd'),
    path(r'unityManagement/unityInfoDelete/', UnityInfoDeleteView.as_view(), name='unityInfoDelete'),
    path(r'unityManagement/unityInfoUpdate/', UnityInfoUpdateView.as_view(), name='unityInfoUpdate'),
    path(r'unityManagement/unityInfoDetails/', UnityInfoDetailsView.as_view(), name='unityInfoDetails'),
    # 机构管理配置
    path(r'companyManagement/companyInfo/', CompanyInfoView.as_view(), name="companyInfo"),
    path(r'companyManagement/companyInfoAdd/', CompanyInfoAddView.as_view(), name="companyInfoAdd"),
    path(r'companyManagement/companyInfoUpdate/', CompanyInfoUpdateView.as_view(), name="companyInfoUpdate"),
    path(r'companyManagement/companyInfoDelete/', CompanyInfoDeleteView.as_view(), name="companyInfoDelete"),
    path(r'companyManagement/companyInfoDetails/', CompanyInfoDetailsView.as_view(), name="companyInfoDetails"),
    path(r'companyManagement/memberInfo/', MemberInfoView.as_view(), name="memberInfo"),
    path(r'companyManagement/memberInfoAdd/', MemberInfoAddView.as_view(), name="memberInfoAdd"),
    path(r'companyManagement/memberInfoDetails/', MemberInfoDetailsView.as_view(), name="memberInfoDetails"),
    path(r'companyManagement/memberInfoDelete/', MemberInfoDeleteView.as_view(), name="memberInfoDelete"),
    path(r'companyManagement/memberInfoUpdate/', MemberInfoUpdateView.as_view(), name="memberInfoUpdate"),
    path(r'companyManagement/equipmentInfo/', EquipmentInfoView.as_view(), name="equipmentInfo"),
    path(r'companyManagement/equipmentInfoAdd/', EquipmentInfoAddView.as_view(), name="equipmentInfoAdd"),
    path(r'companyManagement/equipmentInfoDetails/', EquipmentInfoDetailsView.as_view(), name="equipmentInfoDetails"),
    path(r'companyManagement/equipmentInfoDelete/', EquipmentInfoDeleteView.as_view(), name="equipmentInfoDelete"),
    path(r'companyManagement/equipmentInfoUpdate/', EquipmentInfoUpdateView.as_view(), name="equipmentInfoUpdate"),
    path(r'companyManagement/blockInfo/', BlockInfoView.as_view(), name="blockInfo"),
    path(r'companyManagement/blockInfoAdd/', BlockInfoAddView.as_view(), name="blockInfoAdd"),
    path(r'companyManagement/blockInfoDetails/', BlockInfoDetailsView.as_view(), name="blockInfoDetails"),
    path(r'companyManagement/blockInfoDelete/', BlockInfoDeleteView.as_view(), name="blockInfoDelete"),
    path(r'companyManagement/blockInfoUpdate/', BlockInfoUpdateView.as_view(), name="blockInfoUpdate"),
    path(r'companyManagement/equipmentShareInfo/', EquipmentShareInfoView.as_view(), name="equipmentShareInfo"),
    # 账号分发配置
    path(r'userManagement/userList/', UserListView.as_view(), name="userList"),
    path(r'userManagement/distributeUser/', DistributeUserView.as_view(), name="distributeUser"),
    path(r'userManagement/userInfoDelete/', UserInfoDeleteView.as_view(), name="userInfoDelete"),
    path(r'userManagement/updatePwd/', UpdatePwd.as_view(), name="updatePwd"),
    path(r'userManagement/resetPwd/',ResetPwd.as_view(), name="resetPwd"),
    # 任务管理配置
    path(r'taskManagement/taskInfo/', TaskInfo.as_view(), name='taskInfo'),
    path(r'taskManagement/taskInfoDetails/', TaskInfoDetails.as_view(), name='taskInfoDetails'),
    path(r'taskManagement/taskInfoDelete/', TaskInfoDelete.as_view(), name='taskInfoDelete'),
    path(r'taskManagement/taskInfoUpdate/', TaskInfoUpdate.as_view(), name='taskInfoUpdate'),
    path(r'taskManagement/taskDistributing/', TaskDistributing.as_view(), name='taskDistributing'),
    path(r'taskManagement/taskReceivingInfo/', TaskReceivingInfo.as_view(), name='taskReceivingInfo'),
    path(r'taskManagement/ReceivingCompanyTask/', ReceivingCompanyTask.as_view(), name='receiveCompanyTask'),
    path(r'taskManagement/ReceivingPersonTask/', ReceivingPersonTask.as_view(), name='receivingPersonTask'),
    # 品种管理配置
    path(r'rawProductionManagement/rawProductionInfo/', RawProductionInfoView.as_view(), name='rawProductionInfo'),
    path(r'rawProductionManagement/rawProductionInfoAdd/', RawProductionInfoAddView.as_view(),
         name='rawProductionInfoAdd'),
    path(r'rawProductionManagement/rawProductionInfoUpdate/', RawProductionInfoUpdateView.as_view(),
         name='rawProductionInfoUpdate'),
    path(r'rawProductionManagement/rawProductionInfoDelete/', RawProductionInfoDeleteView.as_view(),
         name='rawProductionInfoDelete'),
    path(r'rawProductionManagement/rawProductionInfoDetails/', RawProductionInfoDetailsView.as_view(),
         name='rawProductionInfoDetails'),
    path(r'rawProductionManagement/rawProductionMeasureInfo/', RawProductionMeasureInfoView.as_view(),
         name='rawProductionMeasureInfo'),
    path(r'rawProductionManagement/rawProductionMeasureInfoAdd/', RawProductionMeasureInfoAddView.as_view(),
         name='rawProductionMeasureInfoAdd'),
    path(r'rawProductionManagement/rawProductionMeasureInfoUpdate/', RawProductionMeasureInfoUpdateView.as_view(),
         name='rawProductionMeasureInfoUpdate'),
    path(r'rawProductionManagement/rawProductionMeasureInfoDelete/', RawProductionMeasureInfoDeleteView.as_view(),
         name='rawProductionMeasureInfoDelete'),
    path(r'rawProductionManagement/rawProductionMeasureInfoDetails/', RawProductionMeasureInfoDetailsView.as_view(),
         name='rawProductionMeasureInfoDetails'),
    path(r'rawProductionManagement/rawProductionMeasureSort/', RawProductionMeasureSort.as_view(),
         name='rawProductionMeasureSort'),
    # 生产管理
    path(r'productionManagement/sowingInfo/', SowingInfoView.as_view(), name='sowingInfo'),
    path(r'productionManagement/sowingInfoAdd/', SowingInfoAddView.as_view(), name='sowingInfoAdd'),
    path(r'productionManagement/sowingInfoDetails/', SowingInfoDetailsView.as_view(), name='sowingInfoDetails'),
    path(r'productionManagement/sowingInfoDelete/', SowingInfoDeleteView.as_view(), name='sowingInfoDelete'),
    path(r'productionManagement/producingMeasures/', MeasuresConfirmingView.as_view(), name='measuresConfirming'),
    path(r'productionManagement/confirmingMeasures/', MeasureConfirmingCompleteView.as_view(),
         name='measureConfirmingComplete'),
    path(r'productionManagement/confirmingDetails/', MeasureConfirmingDetailsView.as_view(),
         name='measureConfirmingDetails'),
    path(r'productionManagement/HarvestAdd/', HarvestInfoAddView.as_view(),
         name='harvestInfoAdd'),
    path(r'productionManagement/HarvestInfo/', HarvestInfoView.as_view(),
         name='harvestInfo'),
    path(r'productionManagement/HarvestInfoDetails/', HarvestInfoDetailsView.as_view(),
         name='harvestInfoDetails'),
    # 库存配置
    path(r'productionStore/storeInfoAdd/', StoreInfoAddView.as_view(),
         name='storeInfoAdd'),
    path(r'productionStore/storeInfo/', StoreInfoView.as_view(),
         name='storeInfo'),
    path(r'productionStore/storeInfoDetails/', StoreInfoDetailsView.as_view(),
         name='storeInfoDetails'),
    # 销售配置
    path(r'saleManagement/saleInfoAdd/', SaleInfoAddView.as_view(),
         name='saleInfoAdd'),
    path(r'saleManagement/saleInfo/', SaleInfoView.as_view(),
         name='saleInfo'),
    path(r'saleManagement/saleInfoDetails', SaleInfoDetailsView.as_view(),
         name='saleInfoDetails'),
    path(r'saleManagement/retrospectInfo', RetrospectInfoView.as_view(),
         name='retrospectInfo'),
    path(r'saleManagement/qrCode', QrCodeView.as_view(),
         name='qrCode'),
    # 投入品管理
    path(r'itemManagement/itemInfo', ItemInfoView.as_view(),
         name='itemInfo'),
    path(r'itemManagement/itemInfoAdd', ItemInfoAddView.as_view(),
         name='itemInfoAdd'),
    path(r'itemManagement/itemInfoUpdate', ItemInfoUpdateView.as_view(),
         name='itemInfoUpdate'),
    path(r'itemManagement/itemInfoDelete', ItemInfoDeleteView.as_view(),
         name='itemInfoDelete'),
    path(r'itemManagement/itemCost', ItemCostView.as_view(),
         name='itemCost'),
    path(r'itemManagement/itemCostAdd', ItemCostAddView.as_view(),
         name='itemCostAdd'),
    path(r'itemManagement/itemCostDelete', ItemCostDeleteView.as_view(),
         name='itemCostDelete'),
    path(r'itemManagement/itemCostDetails', ItemCostDetailsView.as_view(),
         name='itemCostDetails'),
    path(r'itemManagement/itemCostQuery', ItemCostQueryView.as_view(),
         name='itemCostQuery'),
    # 收支配置
    path(r'costManagement/costManagementInfo/', CostManagementInfoView.as_view(),
         name='costManagementInfo'),
    path(r'costManagement/costManagementInfoAdd/', CostManagementInfoAddView.as_view(),
         name='costManagementInfoAdd'),
    path(r'costManagement/costManagementInfoDetails/', CostManagementInfoDetailsView.as_view(),
         name='costManagementInfoDetails'),
    #日志配置
    path(r'logManagement/logInfo/', logInfo.as_view(),
         name='logInfo'),
    # media 配置
    path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # static 配置
    path(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),
    ]

# 全局404页面配置
handler404 = 'apps.users.views.page_not_found'
handler500 = 'apps.users.views.page_error'