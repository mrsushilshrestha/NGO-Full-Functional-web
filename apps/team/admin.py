from django.contrib import admin
from .models import Chapter, Member


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    pass


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'member_type', 'role', 'member_id', 'chapter', 'is_active']
    list_filter = ['member_type', 'chapter', 'is_active']
    search_fields = ['name', 'member_id', 'role', 'specialization']
    list_editable = ['is_active']
    readonly_fields = ['member_id']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'member_type', 'member_id', 'role', 'photo', 'bio', 'specialization')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'facebook_url', 'instagram_url', 'linkedin_url')
        }),
        ('Additional Details', {
            'fields': ('chapter', 'education', 'join_year', 'date_of_issue', 'order', 'is_active')
        }),
    )
