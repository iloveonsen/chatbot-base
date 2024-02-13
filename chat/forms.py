from django import forms
from .models import ChatSession, UserMessage, BotResponse


class ChatSessionForm(forms.ModelForm):
    class Meta:
        model = ChatSession
        fields = []  # Assuming you want to handle 'title' programmatically


class UserMessageForm(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = ['message']
        widgets = {
            # choose html element (textarea) and apply custom css classes to the form fields
            'message': forms.Textarea(attrs={'id': 'user-input', 'class': 'user-input', 'placeholder': 'Type a message...', 'rows': '1', 'required': True}),
        }


class BotResponseForm(forms.ModelForm):
    class Meta:
        model = BotResponse
        fields = ['response']
