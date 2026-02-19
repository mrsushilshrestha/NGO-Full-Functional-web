from django.urls import path
from . import views

urlpatterns = [
    path('', views.programs_list, name='programs_list'),
    path('<slug:slug>/', views.program_detail, name='program_detail'),
]
