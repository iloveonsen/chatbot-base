from django.shortcuts import render, redirect
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *


# Create your views here.

class DefaultChatView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    template_name = 'chat/index.html'

    def get(self, request):
        user_message_form = UserMessageForm()
        context = {
            'form': user_message_form # render the form in the template
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request):
        # create new session
        chat_session = ChatSession.objects.create(
            title="New session",
            owner=request.user.profile,
        )
        chat_session.save()

        # save input message in newly created session
        user_message_form = UserMessageForm(request.POST)
        if user_message_form.is_valid():
            user_message = user_message_form.save(commit=False)
            user_message.session = chat_session
            user_message.owner = request.user.profile
            user_message.save()
            # Redirect to the chat page or the chat session page
        else:
            print(user_message_form.errors)
        return redirect('chat', pk=chat_session.id)

    

class ChatView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    template_name = 'chat/index.html'

    def get(self, request, pk):
        user_message_form = UserMessageForm()
        profile = request.user.profile
        chat_session = profile.chat_sessions.get(id=pk)
        user_messages = chat_session.user_messages.all()
        for message in user_messages:
            print(message.message)
        context = {
            'chat_session': chat_session,
            'user_messages': user_messages,
            'form': user_message_form,
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, pk):
        chat_session = ChatSession.objects.get(id=pk)
        user_message_form = UserMessageForm(request.POST)
        if user_message_form.is_valid():
            user_message = user_message_form.save(commit=False)  
            user_message.session = chat_session
            user_message.owner = request.user.profile
            user_message.save()
            # Redirect to the chat page or the chat session page
        else:
            print(user_message_form.errors)
        return redirect('chat', pk=pk)
    

class ChatSessionsView(LoginRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    template_name = 'chat/chat-sessions.html'
    model = ChatSession
    ordering = ['-created_at']
    context_object_name = 'chat_sessions'


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


