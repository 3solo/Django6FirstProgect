from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, CreateView
from users.forms import LoginUserForm, RegisterUserForm,  ProfileUsersForm
from users.models import Profile


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

class LogoutUser(LogoutView):
    next_page = reverse_lazy('users:login')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users/register.html')
    extra_context = {'title': 'Регистрация'}

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return render(self.request, 'users/register_done.html')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUsersForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    extra_context = {'title': 'Профиль'}

    def get_object(self):
        return self.request.user

    def get_initial(self):
        initial = {}
        if hasattr(self.request.user, 'profile'):
            initial['date_of_birth'] = self.request.user.profile.date_of_birth
        return initial

    def form_valid(self, form):
        user = form.save()
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.date_of_birth = form.cleaned_data.get('date_of_birth')
        if self.request.FILES.get('photo'):
            profile.photo = self.request.FILES['photo']
        profile.save()  
        return HttpResponseRedirect(self.success_url)