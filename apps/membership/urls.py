from django.urls import path
from . import views

urlpatterns = [
    path('volunteer/', views.volunteer_form, name='volunteer_form'),
    path('apply/', views.membership_form, name='membership_form'),
    path('esewa/success/<str:tid>/', views.membership_esewa_success, name='membership_esewa_success'),
    path('esewa/failure/<str:tid>/', views.membership_esewa_failure, name='membership_esewa_failure'),
    path('khalti/return/', views.membership_khalti_return, name='membership_khalti_return'),
]
