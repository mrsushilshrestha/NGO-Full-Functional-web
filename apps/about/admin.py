from django.contrib import admin
from .models import OrganizationInfo, Founder, ChapterLocation, Achievement


@admin.register(OrganizationInfo)
class OrganizationInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(Founder)
class FounderAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'order']
    list_editable = ['order']


@admin.register(ChapterLocation)
class ChapterLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'order']
    list_editable = ['order']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'order']
    list_editable = ['order']
