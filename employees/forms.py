from django import forms
from .models import Employee, SalaryGrade

class SalaryGradeForm(forms.ModelForm):
    class Meta:
        model = SalaryGrade
        fields = ['code', 'step', 'base_pay']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_no', 'first_name', 'last_name', 'department', 'position', 'salary_grade', 'date_hired', 'active']
