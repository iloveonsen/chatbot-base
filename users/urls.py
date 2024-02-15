from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.LoginUserView.as_view(),name='login'),
    path('logout/', views.LogoutView.as_view(next_page='login'),name='logout'),
    path('register/', views.RegisterUserView.as_view(),name='register'),
    path('delete-account/', views.DeleteAccountView.as_view(),name='delete-account'),

    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
]
