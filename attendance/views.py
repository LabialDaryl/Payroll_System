from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from accounts.decorators import group_required
from .models import AttendanceLog, LeaveRequest
from .forms import AttendanceLogForm, LeaveRequestForm
from employees.models import Employee

@login_required
@group_required('Staff')
def attendance_list(request):
    logs = AttendanceLog.objects.select_related('employee').all()[:200]
    return render(request, 'attendance/attendance_list.html', {'logs': logs})

@login_required
@group_required('Staff')
def attendance_create(request):
    if request.method == 'POST':
        form = AttendanceLogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceLogForm()
    return render(request, 'attendance/attendance_form.html', {'form': form, 'title': 'Create Attendance Log'})

@login_required
@group_required('Employee')
def leave_submit(request):
    employee = get_object_or_404(Employee, user=request.user)
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            lr = form.save(commit=False)
            lr.employee = employee
            lr.save()
            return redirect('employee_dashboard')
    else:
        form = LeaveRequestForm()
    return render(request, 'attendance/leave_form.html', {'form': form, 'title': 'Submit Leave Request'})

@login_required
@group_required('Staff')
def leave_queue(request):
    leaves = LeaveRequest.objects.select_related('employee').all()[:200]
    return render(request, 'attendance/leave_queue.html', {'leaves': leaves})

@login_required
@group_required('Staff')
def leave_decide(request, pk, decision):
    lr = get_object_or_404(LeaveRequest, pk=pk)
    if decision.upper() in ['APPROVED', 'REJECTED']:
        lr.status = decision.upper()
        lr.decided_by = request.user
        lr.decided_at = timezone.now()
        lr.save()
    return redirect('leave_queue')
