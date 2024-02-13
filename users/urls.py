from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginUserView.as_view(),name='login'),
    path('logout/', views.LogoutView.as_view(next_page='login'),name='logout'),
    path('register/', views.RegisterUserView.as_view(),name='register'),
    path('delete-account/', views.DeleteAccountView.as_view(),name='delete-account'),

    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
]
