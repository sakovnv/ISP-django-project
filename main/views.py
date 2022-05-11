import logging

from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.defaults import page_not_found
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView

from .forms import *
from .models import *

logger = logging.getLogger(__name__)


def home(request):
    categories = Category.objects.all()
    ads = Ad.objects.all()
    return render(request, 'main/index.html', {'ads': ads, 'categories': categories, 'title': 'Главная страница'})


# def create_ad(request):
#     if request.method == 'POST':
#         form = CreateAdForm(request.POST, request.FILES)
#         if form.is_valid():
#             try:
#                 form.instance.author = request.user
#                 Ad.objects.create(**form.cleaned_data)
#                 return redirect(home)
#             except:
#                 form.add_error(None, 'Ошибка')
#                 return render(request, 'ad/create.html', {'form': form, 'title': 'Создание объявление'})
#
#         else:
#             form.add_error(None, 'Форма не прошла валидацию')
#
#         return redirect(home)
#     else:
#         form = CreateAdForm()
#         return render(request, 'ad/create.html', {'form': form, 'title': 'Создание объявление'})


class CreateAd(DataMixin, CreateView):
    form_class = CreateAdForm
    template_name = 'ad/create.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        u_context = self.get_context(title='Создание объявления')
        return dict(list(context.items()) + list(u_context.items()))

    def form_valid(self, form):
        if self.request.user is not AnonymousUser:
            form.instance.author = self.request.user
        ad = form.save()

        logger.info(f'{self.request.user} created ad "{ad.title}"')

        return redirect('home')


class EditAd(DataMixin, UpdateView):
    form_class = EditAdForm
    template_name = 'ad/edit.html'

    def get_queryset(self):
        return Ad.objects.filter(pk=self.kwargs.get('pk', None))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        u_context = self.get_context(title='Редактирование объявления')
        return dict(list(context.items()) + list(u_context.items()))

    def get_success_url(self):
        logger.info(f'"{self.get_object()}" edited by {self.request.user}')

        return reverse_lazy('ad', kwargs={'ad_id': self.kwargs.get('pk', None)})
    

class DeleteAd(DeleteView):
    model = Ad

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        logger.info(f'{self.request.user} deleted "{self.get_object()}" ad')

        return reverse_lazy('home')


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

        logger.info(f'{user} registered')

        return redirect('home')


class Login(DataMixin, LoginView):
    form_class = LoginForm
    template_name = 'auth/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        u_context = self.get_context(title="Авторизация")
        return dict(list(context.items()) + list(u_context.items()))

    def get_success_url(self):
        logger.info(f'{self.request.user} logged in')

        return reverse_lazy('home')


def ad_view(request, ad_id):
    ad = Ad.objects.select_related('author', 'category').get(pk=ad_id)
    return render(request, 'ad/index.html', {'ad': ad, 'title': 'Объявление'})


def logout_user(request):
    logger.info(f'{request.user} logged out')

    logout(request)
    return redirect('login')
