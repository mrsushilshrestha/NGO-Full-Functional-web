"""Django admin for blog models."""
from django.contrib import admin
from .models import BlogAuthor, BlogCategory, BlogTag, BlogPost, BlogContentBlock, BlogPageSettings


class BlogContentBlockInline(admin.TabularInline):
    model = BlogContentBlock
    extra = 1
    ordering = ['order']
    fields = ['order', 'block_type', 'content', 'attribution']


@admin.register(BlogAuthor)
class BlogAuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'order']
    list_editable = ['order']


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order']


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'category', 'status', 'featured', 'created_at']
    list_filter = ['status', 'featured', 'category']
    list_editable = ['status', 'featured']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'excerpt']
    filter_horizontal = ['tags']
    date_hierarchy = 'date'
    inlines = [BlogContentBlockInline]
    raw_id_fields = ['author']
    fieldsets = [
        (None, {
            'fields': ['title', 'slug', 'date', 'status', 'featured']
        }),
        ('Author', {
            'fields': ['author', 'author_name', 'author_role', 'author_avatar'],
            'description': 'Use linked Author or fill inline fields'
        }),
        ('Content', {
            'fields': ['category', 'tags', 'excerpt', 'long_excerpt']
        }),
        ('Featured Image', {
            'fields': ['featured_image', 'image_caption']
        }),
    ]


@admin.register(BlogPageSettings)
class BlogPageSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not BlogPageSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
