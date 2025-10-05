from datetime import date
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django import forms
from accounts.decorators import group_required
from .models import PayrollRun, Payslip, Loan, OtherDeduction
from .utils import compute_full_payroll, generate_bank_file
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


            employees = Employee.objects.filter(active=True).select_related('salary_grade')
            for emp in employees:

                base_salary = Decimal(emp.salary_grade.base_pay)
                

                overtime_pay = Decimal('0.00')  # TODO: Calculate from attendance
                

                payroll_data = compute_full_payroll(emp, base_salary, overtime_pay)
                

                Payslip.objects.create(
                    payroll_run=run,
                    employee=emp,
                    gross_pay=payroll_data['gross_pay'],
                    overtime_pay=payroll_data['overtime_pay'],
                    sss=payroll_data['sss'],
                    philhealth=payroll_data['philhealth'],
                    pagibig=payroll_data['pagibig'],
                    tax=payroll_data['tax'],
                    loan_deductions=payroll_data['loan_deductions'],
                    other_deductions=payroll_data['other_deductions'],
                    net_pay=payroll_data['net_pay'],
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
def my_payslips(request):

    try:
        emp = request.user.employee
    except Employee.DoesNotExist:
        return render(request, 'payroll/my_payslips.html', {'slips': []})
    slips = Payslip.objects.filter(employee=emp).select_related('payroll_run').order_by('-payroll_run__created_at')
    return render(request, 'payroll/my_payslips.html', {'slips': slips})

@login_required
def my_payslip_detail(request, slip_id):
    try:
        emp = request.user.employee
    except Employee.DoesNotExist:
        emp = None
    slip = get_object_or_404(Payslip, pk=slip_id, employee=emp)
    return render(request, 'payroll/my_payslip_detail.html', {'slip': slip})

@login_required
@group_required('Staff')
def generate_bank_transfer_file(request, run_id):
    """Step 8: Send Salary Details to Bank"""
    run = get_object_or_404(PayrollRun, pk=run_id)
    

    run.payslips.update(bank_file_generated=True)
    
    return generate_bank_file(run)

@login_required
@group_required('Staff')
def mark_salaries_deposited(request, run_id):
    """Step 9: Mark salaries as deposited to employee accounts"""
    from django.utils import timezone
    
    run = get_object_or_404(PayrollRun, pk=run_id)
    
    if request.method == 'POST':

        run.payslips.update(
            salary_deposited=True,
            deposit_date=timezone.now()
        )
        return redirect('payroll_run_payslips', run_id=run.id)
    
    return render(request, 'payroll/confirm_deposit.html', {'run': run})

@login_required
@group_required('Staff')
def loan_management(request):
    """Manage employee loans"""
    loans = Loan.objects.select_related('employee').filter(is_active=True)
    return render(request, 'payroll/loan_management.html', {'loans': loans})

@login_required
@group_required('Staff')
def deduction_management(request):
    """Manage other deductions"""
    deductions = OtherDeduction.objects.select_related('employee').filter(is_active=True)
    return render(request, 'payroll/deduction_management.html', {'deductions': deductions})

@login_required
def my_deposit_status(request):
    """Employee view of their salary deposit status"""
    try:
        employee = request.user.employee

        payslips = Payslip.objects.filter(employee=employee).select_related('payroll_run').order_by('-payroll_run__created_at')[:12]  # Last 12 payslips
        return render(request, 'payroll/my_deposit_status.html', {
            'payslips': payslips,
            'employee': employee
        })
    except Employee.DoesNotExist:
        return render(request, 'payroll/my_deposit_status.html', {
            'payslips': [],
            'employee': None,
            'error': 'No employee record found for your account. Please contact HR.'
        })
