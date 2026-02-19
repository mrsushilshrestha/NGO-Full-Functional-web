"""
URL configuration for NHAF Nepal project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.contact import views as contact_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-login/', include('apps.cms.urls')),
    path('', include('apps.core.urls')),
    path('about/', include('apps.about.urls')),
    path('gallery/', contact_views.gallery_page, name='gallery'),
    path('programs/', include('apps.programs.urls')),
    path('team/', include('apps.team.urls')),
    path('membership/', include('apps.membership.urls')),
    path('impact/', include('apps.impact.urls')),
    path('contact/', include('apps.contact.urls')),
    path('donate/', include('apps.donation.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
