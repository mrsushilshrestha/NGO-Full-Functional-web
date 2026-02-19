from django.contrib import admin
from .models import Chapter, Member


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    pass


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'role_level', 'chapter', 'is_active']
    list_filter = ['role_level', 'chapter']
    search_fields = ['name', 'member_id', 'role', 'specialization']
    list_editable = ['is_active']
