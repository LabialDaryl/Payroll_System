from django.urls import path
from . import views

urlpatterns = [
    path('runs/', views.run_list, name='payroll_run_list'),
    path('runs/create/', views.run_create, name='payroll_run_create'),
    path('runs/<int:run_id>/payslips/', views.run_payslips, name='payroll_run_payslips'),

    path('my/payslips/', views.my_payslips, name='my_payslips'),
    path('my/payslips/<int:slip_id>/', views.my_payslip_detail, name='my_payslip_detail'),
    path('my/deposits/', views.my_deposit_status, name='my_deposit_status'),
    

    path('runs/<int:run_id>/generate-bank-file/', views.generate_bank_transfer_file, name='generate_bank_file'),
    path('runs/<int:run_id>/mark-deposited/', views.mark_salaries_deposited, name='mark_salaries_deposited'),
    path('loans/', views.loan_management, name='loan_management'),
    path('deductions/', views.deduction_management, name='deduction_management'),
]
