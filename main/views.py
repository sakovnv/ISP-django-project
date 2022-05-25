import logging

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView

from .forms import *
from .models import *

logger = logging.getLogger(__name__)


# def home(request):
#     categories = Category.objects.all()
#     ads = Ad.objects.all()
#     return render(request, 'main/index.html', {'ads': ads, 'categories': categories, 'title': 'Главная страница',
#                                                'selected_category': -1})


# def category_ads(request, category_slug):
#     categories = Category.objects.all()
#     selected_category = Category.objects.get(slug=category_slug)
#     ads = Ad.objects.filter(category=selected_category)
#     return render(request, 'main/index.html', {'ads': ads, 'categories': categories, 'title': selected_category,
#                                                'selected_category': selected_category.id})

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


class Home(DataMixin, TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        u_context = self.get_context(title='Главная страница', selected_category=-1)
        return dict(list(context.items()) + list(u_context.items()))


class SubscribedAds(DataMixin, TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ads = Ad.objects.filter(category__in=self.request.user.category_subscriptions.all())
        u_context = self.get_context(title='Главная страница', selected_category=0, ads=ads)
        return dict(list(context.items()) + list(u_context.items()))


class CategoryAds(DataMixin, TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_category = Category.objects.get(slug=kwargs['category_slug'])
        ads = Ad.objects.filter(category=selected_category)
        u_context = self.get_context(title='Главная страница', selected_category=selected_category.id, ads=ads)
        return dict(list(context.items()) + list(u_context.items()))


class CreateAd(DataMixin, CreateView):
    form_class = CreateAdForm
    template_name = 'ad/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        u_context = self.get_context(title='Создание объявления')
        return dict(list(context.items()) + list(u_context.items()))

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user
        ad = form.save()

        logger.info(f'{self.request.user} created ad "{ad.title}"')

        return super().form_valid(form)


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
    return render(request, 'ad/index.html',
                  {
                      'ad': ad,
                      'title': 'Объявление',
                      'categories': asyncio.run(get_all_categories())
                  })


def logout_user(request):

    logger.info(f'{request.user} logged out')

    logout(request)
    return redirect('login')


def subscribe_category(request):
    category_id = request.POST['category_id']
    if bool(request.POST['is_subscribed'] == 'true'):
        request.user.category_subscriptions.add(category_id)
    else:
        request.user.category_subscriptions.remove(category_id)

    return HttpResponse(status=204)
