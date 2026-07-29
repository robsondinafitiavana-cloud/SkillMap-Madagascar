from django.contrib import admin
from .models import StudentProfile, Experience


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 0


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'university', 'department', 'level', 'user')
    list_filter = ('university', 'department', 'level')
    search_fields = ('first_name', 'last_name', 'user__email')
    inlines = [ExperienceInline]
