from django.urls import path
from . import views

urlpatterns = [
    path('', views.RouteView.as_view(), name='routes')
    
]
