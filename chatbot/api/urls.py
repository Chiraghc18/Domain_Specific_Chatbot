# api/urls.py
from django.urls import path
from .views import chat, clear_conversation

urlpatterns = [
    path('chat/', chat, name='chat'),
    path('clear-conversation/', clear_conversation, name='clear-conversation'),
]