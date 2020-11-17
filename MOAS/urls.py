"""MOAS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path, include

from applications.attendance import attendance
from applications.dashboard import dashboard
from applications.process import process
from applications.report import report
from applications.repository import repository
from applications.setting import setting
from applications.tools import tools
from applications.user import user
from conf.conf import SERVICE_VERSION
from lib import m_rest_framework as rest

router = rest.routers.DefaultRouter(trailing_slash=False)

router.register(f'api/v{SERVICE_VERSION}/public', user.PublicKeyView, basename='public')
router.register(f'api/v{SERVICE_VERSION}/process/submitProcess', process.ProcessView)
router.register(f'api/v{SERVICE_VERSION}/process/handleProcess', process.ProcessView)
router.register(f'api/v{SERVICE_VERSION}/process/reviewProcess', process.ReviewProcessView)
router.register(f'api/v{SERVICE_VERSION}/process/atLeader', process.AtLeaderView)
router.register(f'api/v{SERVICE_VERSION}/user/users', user.UserView)
router.register(f'api/v{SERVICE_VERSION}/user/batch', user.UserBatchView)
router.register(f'api/v{SERVICE_VERSION}/attendance/attendance', attendance.AttendanceView, basename='attendance')
router.register(f'api/v{SERVICE_VERSION}/attendance/abnormalAttendance', attendance.AbnormalAttendanceView, basename='abnormalAttendance')
router.register(f'api/v{SERVICE_VERSION}/attendance/holidayHandle', attendance.HolidayHandleView, basename='holidayHandle')
router.register(f'api/v{SERVICE_VERSION}/report/report', report.ReportView)
router.register(f'api/v{SERVICE_VERSION}/report/monthlyreport', report.MonthlyReportView)
router.register(f'api/v{SERVICE_VERSION}/user/department', user.DepartmentView)
router.register(f'api/v{SERVICE_VERSION}/user/role', user.RoleView)
router.register(f'api/v{SERVICE_VERSION}/repository/repository', repository.RepositoryView)
router.register(f'api/v{SERVICE_VERSION}/repository/myrepository', repository.MyRepositoryView)
router.register(f'api/v{SERVICE_VERSION}/repository/draft', repository.DraftView)
router.register(f'api/v{SERVICE_VERSION}/tools/analyze', tools.AnalyzeTool, basename='analyzeTool')
router.register(f'api/v{SERVICE_VERSION}/tools/analyzeManagement', tools.ManagementMappingRulerView, basename='management')

urlpatterns = [
    path(f'api/v{SERVICE_VERSION}/login', user.LoginView.as_view()),
    path(f'api/v{SERVICE_VERSION}/logout', user.LogoutView.as_view()),
    path(f'api/v{SERVICE_VERSION}/refresh', user.RefreshAPIView.as_view()),
    path(f'api/v{SERVICE_VERSION}/change', user.UserChangeViewSet.as_view()),
    path(f'api/v{SERVICE_VERSION}/navs', user.UserNavsView.as_view()),
    path(f'api/v{SERVICE_VERSION}/dashboard/dashboard', dashboard.DashboardView.as_view()),
    path(f'api/v{SERVICE_VERSION}/setting/personalSetting', setting.PersonalSettingView.as_view()),
    path(f'api/v{SERVICE_VERSION}/setting/securitySetting', setting.SecuritySettingView.as_view()),
    path(f'api/v{SERVICE_VERSION}/setting/systemSetting', setting.SystemSettingView.as_view()),
]

urlpatterns += [
    url('', include(router.urls)),
]
