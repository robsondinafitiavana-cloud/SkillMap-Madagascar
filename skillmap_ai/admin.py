from django.contrib import admin
from .models import Career, CareerSkill


class CareerSkillInline(admin.TabularInline):
    model = CareerSkill
    extra = 1


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'recommended_level')
    list_filter = ('domain',)
    search_fields = ('name', 'description')
    inlines = [CareerSkillInline]
