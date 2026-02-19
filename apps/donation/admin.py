from django.contrib import admin
from .models import DonationTier, Donation, BankDetail


@admin.register(BankDetail)
class BankDetailAdmin(admin.ModelAdmin):
    list_display = ['bank_name', 'account_number', 'order']
    list_editable = ['order']


@admin.register(DonationTier)
class DonationTierAdmin(admin.ModelAdmin):
    list_display = ['amount', 'label', 'order']
    list_editable = ['order']


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['amount', 'donor_name', 'payment_method', 'status', 'created_at']
    list_filter = ['payment_method', 'status', 'created_at']
