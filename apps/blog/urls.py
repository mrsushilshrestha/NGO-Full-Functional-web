from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('api/search/', views.blog_search_suggest, name='blog_search_suggest'),
    path('api/posts/', views.blog_api, name='blog_api'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
]
