from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView

from siteguys.settings import MEDIA_ROOT
from users.forms import LoginUserForm, RegisterUserForm,  ProfileUsersForm
from users.models import Profile


def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'],
                                password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))


    else:
        form = LoginUserForm()

    return render(request, 'users/login.html', {'form': form, 'title': 'Авторизация'})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'users/register_done.html')
    else:
        form = RegisterUserForm()
    return render(request, 'users/register.html', {'form': form, 'title': 'Регистрация'})


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