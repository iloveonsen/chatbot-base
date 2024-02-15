from django.urls import path
from . import views

urlpatterns = [
    path('', views.RouteView.as_view(), name='routes'),
    
    path('vectorstores/', views.VectorStoreView.as_view()),
    path('chats/<uuid:pk>/', views.ChatSessionView.as_view()),
]
