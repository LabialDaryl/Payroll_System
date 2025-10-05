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

class Payslip(models.Model):
    payroll_run = models.ForeignKey(PayrollRun, on_delete=models.CASCADE, related_name='payslips')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    gross_pay = models.DecimalField(max_digits=12, decimal_places=2)
    sss = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    philhealth = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pagibig = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_pay = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Payslip {self.employee} {self.payroll_run}"
