from rest_framework import serializers
from chat.models import ChatSession, UserMessage, BotResponse
from users.models import Profile, BotConfiguration


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'name', 'profile_image', 'created']


class BotResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotResponse
        fields = ['id', 'response', 'created_at']


class UserMessageSerializer(serializers.ModelSerializer):
    bot_response = BotResponseSerializer(many=False)

    class Meta:
        model = UserMessage
        fields = ['id', 'message', 'created_at', 'bot_response']


class ChatSessionSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    user_messages = UserMessageSerializer(many=True)
    class Meta:
        model = ChatSession
        fields = '__all__'



