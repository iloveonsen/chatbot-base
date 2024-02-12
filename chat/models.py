from django.db import models
from django.contrib.auth.models import User
from users.models import Profile, BotConfiguration
import uuid

# Create your models here.

class ChatSession(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    title = models.CharField(max_length=100, blank=True, null=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='chat_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.owner.name}'
    
    class Meta:
        ordering = ['-created_at']
    

class UserMessage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='user_messages')
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} - {self.owner.name} - {self.session.id}'
    
    class Meta:
        ordering = ['created_at']


class BotResponse(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='bot_responses')
    user_message = models.OneToOneField(UserMessage, on_delete=models.CASCADE, related_name='bot_response')
    bot_configuration = models.ForeignKey(BotConfiguration, on_delete=models.CASCADE, default=1)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} - {self.session.title}'
    
    class Meta:
        ordering = ['created_at']
    

