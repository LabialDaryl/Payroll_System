from django.contrib import admin
from .models import UserProfile, AuditLog

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "employee_id", "department", "position")
    search_fields = ("user__username", "employee_id", "department", "position")

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user", "method", "path", "status_code", "ip")
    list_filter = ("method", "status_code")
    search_fields = ("path", "ip", "user__username")
