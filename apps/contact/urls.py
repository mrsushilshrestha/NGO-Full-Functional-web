from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact, name='contact'),
    path('chat/', views.contact_chat, name='contact_chat'),
    path('chat/send/', views.chat_send, name='chat_send'),
    path('chat/get/', views.chat_get, name='chat_get'),
]
