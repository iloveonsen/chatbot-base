from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginUserView.as_view(),name='login'),
    path('logout/', views.LogoutView.as_view(next_page='index'),name='logout'),
    path('register/', views.RegisterUserView.as_view(),name='register'),

    path('profile/<str:pk>/', views.UserProfileView.as_view(), name='user-profile'),
]
