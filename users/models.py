from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True) 
    email = models.EmailField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="profiles/", default="profiles/user-default.png")
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False) # Primary key, not editable
    created = models.DateTimeField(auto_now_add=True) # Automatically add date and time
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username) # Return username as string
    
    class Meta:
        ordering = ["created"] # Created date ascending order 
    
    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            self.profile_image = "profiles/user-default.png"
            self.save()
            url = self.profile_image.url
        return url