from django.contrib import admin
from .models import PayrollRun, Payslip

@admin.register(PayrollRun)
class PayrollRunAdmin(admin.ModelAdmin):
    list_display = ("created_at", "period_start", "period_end", "created_by")
    list_filter = ("period_start", "period_end")
    date_hierarchy = "created_at"

@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = ("employee", "payroll_run", "gross_pay", "net_pay")
    list_filter = ("payroll_run",)
    search_fields = ("employee__employee_no", "employee__last_name")
