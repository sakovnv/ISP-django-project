from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import *
from .models import *


def home(request):
    categories = Category.objects.all()
    ads = Ad.objects.all()
    return render(request, 'main/index.html', {'ads': ads, 'categories': categories, 'title': 'Главная страница'})


def create_ad(request):
    if request.method == 'POST':
        form = CreateAdForm(request.POST)
        if form.is_valid():
            try:
                Ad.objects.create(**form.cleaned_data)
                return redirect(home)
            except:
                form.add_error(None, 'Ошибка')

    else:
        form = CreateAdForm()
        return render(request, 'ad/create.html', {'form': form, 'title': 'Создание объявление'})


def register(request):
    pass


class Register(DataMixin, CreateView):
    form_class = RegisterForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        u_context = self.get_context(title='Регистрация')
        return dict(list(context.items()) + list(u_context.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class Login(DataMixin, LoginView):
    form_class = LoginForm
    template_name = 'auth/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        u_context = self.get_context(title="Авторизация")
        return dict(list(context.items()) + list(u_context.items()))

    def get_success_url(self):
        reverse_lazy('/')


def logout_user(request):
    logout(request)
    return redirect('login')
