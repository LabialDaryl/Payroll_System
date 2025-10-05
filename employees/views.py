from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import group_required
from .models import Employee, SalaryGrade
from .forms import EmployeeForm, SalaryGradeForm

@login_required
@group_required('Staff')
def employee_list(request):
    employees = Employee.objects.select_related('salary_grade', 'user').all()
    return render(request, 'employees/employee_list.html', {'employees': employees})

@login_required
@group_required('Staff')
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Create Employee'})

@login_required
@group_required('Staff')
def employee_update(request, pk):
    obj = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=obj)
    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Update Employee'})

@login_required
@group_required('Staff')
def employee_delete(request, pk):
    obj = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('employee_list')
    return render(request, 'employees/confirm_delete.html', {'object': obj, 'type': 'Employee'})

@login_required
@group_required('Staff')
def salarygrade_list(request):
    grades = SalaryGrade.objects.all()
    return render(request, 'employees/salarygrade_list.html', {'grades': grades})

@login_required
@group_required('Staff')
def salarygrade_create(request):
    if request.method == 'POST':
        form = SalaryGradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('salarygrade_list')
    else:
        form = SalaryGradeForm()
    return render(request, 'employees/salarygrade_form.html', {'form': form, 'title': 'Create Salary Grade'})

@login_required
@group_required('Staff')
def salarygrade_update(request, pk):
    obj = get_object_or_404(SalaryGrade, pk=pk)
    if request.method == 'POST':
        form = SalaryGradeForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('salarygrade_list')
    else:
        form = SalaryGradeForm(instance=obj)
    return render(request, 'employees/salarygrade_form.html', {'form': form, 'title': 'Update Salary Grade'})
