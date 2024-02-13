from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import uuid

# Create your models here.

name_validator = RegexValidator(r'^[ㄱ-ㅎ가-힣a-zA-Z0-9][ㄱ-ㅎ가-힣a-zA-Z0-9 ]*[ㄱ-ㅎ가-힣a-zA-Z0-9]$', 'Only letters, numbers, and spaces are allowed')

class Profile(models.Model):
    # remove username and email from here (use User model instead)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True, validators=[name_validator]) 
    profile_image = models.ImageField(null=True, blank=True, upload_to="profiles/", default="profiles/user-default.png")
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False) # Primary key, not editable
    created = models.DateTimeField(auto_now_add=True) # Automatically add date and time

    def __str__(self):
        return str(self.name) # Return username as string
    
    class Meta:
        ordering = ["created"] # Created date ascending order 
    
    @property
    def image_url(self):
        try:
            url = self.profile_image.url
        except:
            self.profile_image = "profiles/user-default.png"
            self.save()
            url = self.profile_image.url
        return url


class BotConfiguration(models.Model):
    bot_profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.bot_profile.name} - Bot Configuration'