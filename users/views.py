from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from .forms import CustomUserAuthenticationForm, CustomUserCreationForm, ProfileForm

# Create your views here.

class LoginUserView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    form_class = CustomUserAuthenticationForm
    
    def get_success_url(self):
        return reverse_lazy('index') 
    
    def get_redirect_url(self) -> str:
        return super().get_redirect_url()
     
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return super().form_invalid(form)
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username').lower()
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request,'Invalid username or password')
            return super().form_invalid(form)
    

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
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('username').lower()
            user.save()

            profile = Profile.objects.create(user=user)
            messages.success(request, 'Account created successfully')
            login(request, user)
            return redirect('user-profile')
        else:
            messages.error(request, 'Error creating account')
            context = {'form': form}
            return render(request, self.template_name, context=context)
    

class UserProfileView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    template_name = 'users/user-profile.html'
    
    def get(self, request):
        profile = request.user.profile
        form = ProfileForm(instance=profile)
        context = {'profile': profile, 'form': form}
        return render(request, self.template_name, context=context)

    def post(self, request):
        profile = request.user.profile # get the profile of the logged in user
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('user-profile')
        else:
            messages.error(request, 'Error updating profile')
            context = {'profile': profile, 'form': form}
            return render(request, self.template_name, context=context)
    

class DeleteAccountView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    model = User
    template_name = 'users/delete-account.html'
    success_url = reverse_lazy('login')

    # bypasses the need for a pk in the URL, as we are deleting the currently logged-in user
    def get_object(self, queryset=None):
        # Return the currently logged-in user; no need for a pk in the URL
        return self.request.user
    
    def delete(self, request, *args, **kwargs):
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted successfully')
        return redirect(self.get_success_url())



