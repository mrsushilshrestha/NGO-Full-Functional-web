from django.contrib import admin
from .models import ImpactStat


@admin.register(ImpactStat)
class ImpactStatAdmin(admin.ModelAdmin):
    list_display = ['label', 'value', 'suffix', 'order']
    list_editable = ['value', 'suffix', 'order']
