from django.contrib import admin
from .models import Category, Program


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_date', 'category']
    list_filter = ['category', 'event_date']
    prepopulated_fields = {'slug': ('title',)}
