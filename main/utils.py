from main.models import *


form_attr = {'class': 'form-control'}


class DataMixin:

    def __init__(self):
        self.context = None
        self.request = None

    def get_context(self, **kwargs):
        kwargs_copy = kwargs.copy()
        self.context = kwargs
        categories = Category.objects.all()
        ads = Ad.objects.all()
        user_ads = ads.filter(author=self.request.user)
        self.context['categories'] = categories
        self.context['ads'] = ads
        self.context['user_ads'] = user_ads
        self.context['user_categories'] = self.request.user.category_subscription.all()
        self.context.update(kwargs_copy)

        return self.context
