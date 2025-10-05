from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.decorators import group_required

@login_required
@group_required('Employee')
def employee_dashboard(request):
    return render(request, 'dashboards/employee_dashboard.html')

@login_required
@group_required('Staff')
def staff_dashboard(request):
    return render(request, 'dashboards/staff_dashboard.html')

@login_required
@group_required('Admin')
def admin_dashboard(request):
    return render(request, 'dashboards/admin_dashboard.html')
