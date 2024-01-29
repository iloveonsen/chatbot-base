from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from .forms import CustomUserCreationForm

# Create your views here.

class LoginUserView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('index') 
     
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))
    

class RegisterUserView(View):
    template_name = 'users/register.html'

    def get(self, request):
        form = CustomUserCreationForm()
        if request.user.is_authenticated:
            return redirect('index')
        
        context = {'form': form}
        return render(request, self.template_name, context=context)
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
        else:
            messages.error(request, 'Error creating account')
            context = {'form': form}
            return render(request, self.template_name, context=context)
    

class UserProfileView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    template_name = 'users/user-profile.html'
    
    def get(self, request, pk):
        profile = get_object_or_404(Profile, id=pk)
        context = {'profile': profile}
        return render(request, self.template_name, context=context)
    



