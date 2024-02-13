from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.DefaultChatView.as_view(), name='index'),
    path('chat/<uuid:pk>/', views.ChatView.as_view(), name='chat'),
    path('chat-sessions/', views.ChatSessionsView.as_view(), name='chat-sessions'),

    path('create-chat-session/', views.CreateChatSessionView.as_view(), name='create-chat-session'),
    path('delete-chat-session/<uuid:pk>/', views.DeleteChatSessionView.as_view(), name='delete-chat-session'),
]