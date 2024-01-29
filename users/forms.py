from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User # User, not Profile
        fields = ["username", "email", "password1", "password2"]
        labels = {
            "username": "Username",
            "email": "Email",
            "password1": "Password",
            "password2": "Confirm Password",
        }