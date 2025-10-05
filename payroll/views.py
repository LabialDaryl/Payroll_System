from datetime import date
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django import forms
from accounts.decorators import group_required
from .models import PayrollRun, Payslip
from .utils import compute_contributions
from employees.models import Employee

class PayrollRunForm(forms.ModelForm):
    class Meta:
        model = PayrollRun
        fields = ['period_start', 'period_end']
        widgets = {
            'period_start': forms.DateInput(attrs={'type': 'date'}),
            'period_end': forms.DateInput(attrs={'type': 'date'}),
        }

@login_required
@group_required('Staff')
def run_list(request):
    runs = PayrollRun.objects.all()
    return render(request, 'payroll/run_list.html', {'runs': runs})

@login_required
@group_required('Staff')
def run_create(request):
    if request.method == 'POST':
        form = PayrollRunForm(request.POST)
        if form.is_valid():
            run = form.save(commit=False)
            run.created_by = request.user
            run.save()
            # Simple computation per active employee using salary grade base pay as gross
            employees = Employee.objects.filter(active=True).select_related('salary_grade')
            for emp in employees:
                gross = Decimal(emp.salary_grade.base_pay)
                comp = compute_contributions(gross)
                Payslip.objects.create(
                    payroll_run=run,
                    employee=emp,
                    gross_pay=gross,
                    sss=comp['sss'],
                    philhealth=comp['philhealth'],
                    pagibig=comp['pagibig'],
                    tax=comp['tax'],
                    net_pay=comp['net'],
                )
            return redirect('payroll_run_list')
    else:
        form = PayrollRunForm()
    return render(request, 'payroll/run_create.html', {'form': form})

@login_required
@group_required('Staff')
def run_payslips(request, run_id):
    run = get_object_or_404(PayrollRun, pk=run_id)
    slips = run.payslips.select_related('employee').all()
    return render(request, 'payroll/run_payslips.html', {'run': run, 'slips': slips})

@login_required
@group_required('Employee')
def my_payslips(request):
    # Employee views their own slips
    try:
        emp = request.user.employee
    except Employee.DoesNotExist:
        return render(request, 'payroll/my_payslips.html', {'slips': []})
    slips = Payslip.objects.filter(employee=emp).select_related('payroll_run').order_by('-payroll_run__created_at')
    return render(request, 'payroll/my_payslips.html', {'slips': slips})

@login_required
@group_required('Employee')
def my_payslip_detail(request, slip_id):
    try:
        emp = request.user.employee
    except Employee.DoesNotExist:
        emp = None
    slip = get_object_or_404(Payslip, pk=slip_id, employee=emp)
    return render(request, 'payroll/my_payslip_detail.html', {'slip': slip})
