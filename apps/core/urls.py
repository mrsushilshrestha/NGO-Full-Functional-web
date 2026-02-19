from django.urls import path
from . import views
from apps.contact import views as contact_views

urlpatterns = [
    path('', views.home, name='home'),
    path('terms/members/', contact_views.members_page, name='members_page'),
]
