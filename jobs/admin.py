from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'contract_type', 'deadline', 'is_active')
    list_filter = ('contract_type', 'is_active')
    search_fields = ('title', 'company__company_name')
