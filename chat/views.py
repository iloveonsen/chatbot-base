from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class DefaultChatView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    template_name = 'chat/index.html'

    def get(self, request):
        return render(request, self.template_name)