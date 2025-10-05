from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/employee/', permanent=False)),
    path('django-admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('employee/', include('dashboards.employee_urls')),
    path('staff/', include('dashboards.staff_urls')),
    path('admin/', include('dashboards.admin_urls')),
    path('employees/', include('employees.urls')),
    path('attendance/', include('attendance.urls')),
    path('payroll/', include('payroll.urls')),
    path('reports/', include('reports.urls')),
]
