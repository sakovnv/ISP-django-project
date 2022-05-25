import asyncio

from asgiref.sync import sync_to_async
from django.contrib.auth.models import AnonymousUser

from main.models import *


form_attr = {'class': 'form-control'}


@sync_to_async
def get_all_categories():
    return Category.objects.all()


@sync_to_async
def get_all_ads():
    return Ad.objects.select_related('author').select_related('category').all()


@sync_to_async
def get_user_ads(user: User):
    return Ad.objects.select_related('author').select_related('category').filter(author=user)


class DataMixin:

    def __init__(self):
        self.context = None
        self.request = None

    def get_context(self, **kwargs):
        kwargs_copy = kwargs.copy()
        self.context = kwargs
        categories = asyncio.run(get_all_categories())
        ads = asyncio.run(get_all_ads())
        user_ads = None

        if self.request.user.is_authenticated:
            user_ads = asyncio.run(get_user_ads(self.request.user))

            self.context['user_categories'] = self.request.user.category_subscriptions.all()

        self.context['categories'] = categories
        self.context['ads'] = ads
        self.context['user_ads'] = user_ads
        self.context.update(kwargs_copy)

        return self.context
