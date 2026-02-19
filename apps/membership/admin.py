from django.contrib import admin
from .models import MembershipFee, VolunteerApplication, MembershipApplication


@admin.register(MembershipFee)
class MembershipFeeAdmin(admin.ModelAdmin):
    list_display = ['member_type', 'amount', 'description']


@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'location', 'status', 'submitted_at']
    list_filter = ['status']


@admin.register(MembershipApplication)
class MembershipApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'member_type', 'payment_method', 'amount_paid', 'status', 'submitted_at']
    list_filter = ['status', 'member_type', 'payment_method']
