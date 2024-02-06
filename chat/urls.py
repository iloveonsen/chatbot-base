from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.DefaultChatView.as_view(), name='index'),
]