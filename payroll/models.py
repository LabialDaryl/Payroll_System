from django.db import models
from django.conf import settings
from employees.models import Employee

class PayrollRun(models.Model):
    period_start = models.DateField()
    period_end = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"PayrollRun {self.period_start} to {self.period_end}"

class Loan(models.Model):
    """Employee loan management"""
    LOAN_TYPES = (
        ('SALARY', 'Salary Loan'),
        ('EMERGENCY', 'Emergency Loan'),
        ('HOUSING', 'Housing Loan'),
        ('OTHER', 'Other'),
    )
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
    principal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    monthly_deduction = models.DecimalField(max_digits=12, decimal_places=2)
    remaining_balance = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.employee} - {self.loan_type} Loan"

class OtherDeduction(models.Model):
    """Other deductions like uniform, tools, etc."""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_recurring = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.employee} - {self.description}"

class Payslip(models.Model):
    payroll_run = models.ForeignKey(PayrollRun, on_delete=models.CASCADE, related_name='payslips')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    

    gross_pay = models.DecimalField(max_digits=12, decimal_places=2)
    overtime_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    

    sss = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    philhealth = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pagibig = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    

    loan_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    

    net_pay = models.DecimalField(max_digits=12, decimal_places=2)
    

    bank_file_generated = models.BooleanField(default=False)
    bank_file_sent = models.BooleanField(default=False)
    salary_deposited = models.BooleanField(default=False)
    deposit_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Payslip {self.employee} {self.payroll_run}"
