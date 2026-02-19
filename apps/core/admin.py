from django.contrib import admin
from .models import HeroBanner, HomeContent, AnnouncementPopup, GalleryImage


@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order', 'aspect_ratio', 'overlay_opacity']
    list_editable = ['is_active', 'order']
    fieldsets = (
        (None, {'fields': ('title', 'subtitle', 'image', 'link_url', 'link_text', 'is_active', 'order')}),
        ('Display Options', {'fields': ('aspect_ratio', 'overlay_opacity', 'show_overlay', 'image_fit', 'text_position'),
         'description': 'Control how the banner appears: aspect ratio (16:9), overlay transparency, text position.'}),
    )


@admin.register(HomeContent)
class HomeContentAdmin(admin.ModelAdmin):
    list_display = ['key', 'title', 'is_active']
    list_editable = ['is_active']


@admin.register(AnnouncementPopup)
class AnnouncementPopupAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'has_image', 'start_date', 'end_date']
    list_filter = ['is_active']

    def has_image(self, obj):
        return bool(obj.image) if obj else False
    has_image.boolean = True
    has_image.short_description = 'Image'


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
