from django.contrib import admin
from .models import AttendanceLog, LeaveRequest

@admin.register(AttendanceLog)
class AttendanceLogAdmin(admin.ModelAdmin):
    list_display = ("date", "employee", "time_in", "time_out", "remarks")
    list_filter = ("date",)
    search_fields = ("employee__employee_no", "employee__last_name")

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ("created_at", "employee", "leave_type", "start_date", "end_date", "status", "decided_by")
    list_filter = ("status", "leave_type")
    search_fields = ("employee__employee_no", "employee__last_name")
