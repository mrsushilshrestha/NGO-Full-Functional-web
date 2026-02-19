from django.urls import path
from . import views

urlpatterns = [
    path('', views.team_list, name='team_list'),
    path('<int:pk>/', views.member_detail, name='team_member_detail'),
    path('member/<int:pk>/', views.member_detail, name='member_detail'),
    path('collaborations/', views.collaboration_list, name='collaboration_list'),
    path('collaborations/<int:pk>/', views.collaboration_detail, name='collaboration_detail'),
    path('collaborations/<int:pk>/mou/', views.collaboration_mou_view, name='collaboration_mou_view'),
]
