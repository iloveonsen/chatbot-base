from django.shortcuts import render, redirect
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .forms import *
from .models import *
from .utils import *


# Create your views here.

class DefaultChatView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    template_name = 'chat/index.html'

    def get(self, request):
        bot_config = BotConfiguration.objects.first()
        bot_profile = bot_config.bot_profile
        user_message_form = UserMessageForm()
        context = {
            'bot_profile': bot_profile,
            'form': user_message_form # render the form in the template
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request):
        # create new session
        chat_session = ChatSession.objects.create(
            title="New session",
            owner=request.user.profile,
        )

        # save input message in newly created session
        user_message_form = UserMessageForm(request.POST)
        if user_message_form.is_valid():
            user_message = user_message_form.save(commit=False)
            user_message.session = chat_session
            user_message.owner = request.user.profile
            user_message.save()

            # update session title with summarized title
            chat_session.title = summarize_session_title(user_message.message)
            chat_session.save()

            response = get_chatbot_response(user_message.message, user_message.session, user_message.owner)

            bot_response = BotResponse.objects.create(
                session=chat_session,
                user_message=user_message,
                response=response,
            )
            bot_response.save()
        else:
            print(user_message_form.errors)
        return redirect('chat', pk=chat_session.id)

    

class ChatView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    template_name = 'chat/index.html'

    def get(self, request, pk):
        bot_config = BotConfiguration.objects.first()
        bot_profile = bot_config.bot_profile
        user_message_form = UserMessageForm()
        profile = request.user.profile
        chat_session = profile.chat_sessions.get(id=pk)
        user_messages = chat_session.user_messages.all()
        context = {
            'bot_profile': bot_profile,
            'profile': profile,
            'chat_session': chat_session,
            'user_messages': user_messages,
            'form': user_message_form,
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, pk):
        chat_session = ChatSession.objects.get(id=pk)
        user_input = request.POST.get('message')
        user_message = UserMessage.objects.create(
            message=user_input,
            session=chat_session,
            owner=request.user.profile,
        )    
        user_message.save()

        response = get_chatbot_response(user_message.message, user_message.session, user_message.owner)

        bot_response = BotResponse.objects.create(
            session=chat_session,
            user_message=user_message,
            response=response,
        )
        bot_response.save()

        context = {
            'response': response
        }
        return JsonResponse(context)
    

class ChatSessionsView(LoginRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    template_name = 'chat/chat-sessions.html'
    model = ChatSession
    ordering = ['-created_at']
    context_object_name = 'chat_sessions'

    def get_queryset(self):
        profile = self.request.user.profile
        return profile.chat_sessions.all()


class CreateChatSessionView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    form_class = ChatSessionForm

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            chat_session = form.save(commit=False)
            chat_session.title = "New session"
            chat_session.owner = request.user.profile  # Set the session owner
            chat_session.save()
            print(f"{chat_session.id} has been created")
            # Redirect to the sessions list page or the detail page of the new session
        else:
            print(form.errors)
        return redirect('chat-sessions')  # Adjust the redirect as needed
    

class DeleteChatSessionView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def post(self, request, pk):
        profile = request.user.profile
        session = profile.chat_sessions.get(id=pk)
        session.delete()
        return redirect('chat-sessions')


