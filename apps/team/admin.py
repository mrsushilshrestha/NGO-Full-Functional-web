from django.contrib import admin
from .models import Chapter, Location, Member


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active']
    list_editable = ['order', 'is_active']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'order', 'is_active']
    list_editable = ['order', 'is_active']


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'member_type', 'role', 'member_id', 'location', 'chapter', 'is_active']
    list_filter = ['member_type', 'location', 'chapter', 'is_active']
    search_fields = ['name', 'member_id', 'role', 'specialization']
    list_editable = ['is_active']
    readonly_fields = ['member_id']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'member_type', 'member_id', 'role', 'photo', 'bio', 'specialization')
        }),
        ('Public Location (for filtering on website)', {
            'fields': ('location',)
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'facebook_url', 'instagram_url', 'linkedin_url')
        }),
        ('Internal / Admin only', {
            'fields': ('chapter', 'category', 'education', 'join_year', 'date_of_issue', 'order', 'is_active'),
            'description': 'Chapter and category are not shown on the public site.',
        }),
    )
