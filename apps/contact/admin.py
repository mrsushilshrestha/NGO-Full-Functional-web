from django.contrib import admin
from .models import ContactInfo, ContactMessage


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'submitted_at']
