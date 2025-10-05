from django.contrib import admin
from .models import Employee, SalaryGrade

@admin.register(SalaryGrade)
class SalaryGradeAdmin(admin.ModelAdmin):
    list_display = ("code", "step", "base_pay")
    list_filter = ("code",)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("employee_no", "last_name", "first_name", "department", "position", "salary_grade", "active")
    list_filter = ("department", "position", "active")
    search_fields = ("employee_no", "last_name", "first_name")
