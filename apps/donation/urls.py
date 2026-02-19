from django.urls import path
from . import views

urlpatterns = [
    path('', views.donate, name='donate'),
    path('thanks/', views.donate_thanks, name='donate_thanks'),
    path('esewa/success/<str:tid>/', views.donate_esewa_success, name='donate_esewa_success'),
    path('esewa/failure/<str:tid>/', views.donate_esewa_failure, name='donate_esewa_failure'),
    path('khalti/return/', views.donate_khalti_return, name='donate_khalti_return'),
]
