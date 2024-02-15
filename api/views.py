from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ChatSessionSerializer, UserMessageSerializer
from chat.models import ChatSession, UserMessage, BotResponse
from chat.utils import delete_collections, get_chatbot_response

class RouteView(APIView):
    def get(self, request):
        routes = [
            {
                "path": "/api/",
                "method": {
                    "GET": "list of all available routes"
                },
            }, 
            {
                "path": "/api/vectorstores/",
                "method": {
                    "DELETE": "delete vectorstore collection for specified user"
                },
            },
            {
                "path": "/api/chats/",
                "method": {
                    "GET": "list of all chat sessions belongs to the user",
                },
            },
            {
                "path": "/api/chats/<uuid:pk>/",
                "method": {
                    "GET": "get all chat messages for the chat session",
                    "DELETE": "delete chat session",
                    "POST": "send message to chat session, get chatbot response",
                },
            },
        ]
        return Response(routes)


class VectorStoreView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        # delete vectorstore collection for specified user
        username = request.user.username
        if delete_collections(username):
            content = {"message": "vectorstore collection deleted successfully"}
            return Response(content, status=204) # 204 No Content
        content = {"message": "vectorstore collection not found"}
        return Response(content, status=404) # 404 Not Found
    

class ChatSessionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # list of all chat sessions belongs to the user
        chat_sessions = ChatSession.objects.filter(owner=request.user.profile)
        serializer = ChatSessionSerializer(chat_sessions, many=True)
        return Response(serializer.data)
    

class ChatSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # list of all chat sessions belongs to the user
        chat_session = ChatSession.objects.get(owner=request.user.profile, id=pk)
        serializer = ChatSessionSerializer(chat_session, many=False)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        # delete chat session
        chat_session = ChatSession.objects.get(owner=request.user.profile, id=pk)
        chat_session.delete()
        content = {"message": "chat session deleted successfully"}
        return Response(content, status=204) # 204 No Content
    
    def post(self, request, pk):
        profile = request.user.profile
        chat_session = ChatSession.objects.get(owner=profile, id=pk)

        message = request.data.get('user_message')

        user_message = UserMessage.objects.create(
            session=chat_session,
            owner=request.user.profile,
            message=message
        )

        response = get_chatbot_response(message, chat_session, profile)

        bot_response = BotResponse.objects.create(
            session=chat_session,
            user_message=user_message,
            response=response
        )

        serializer = UserMessageSerializer(user_message, many=False)
        return Response(serializer.data, status=201) # 201 Created

        