from main.models import *


form_attr = {'class': 'form-control'}


class DataMixin:

    def __init__(self):
        self.context = None

    def get_context(self, **kwargs):
        self.context = kwargs
        categories = Category.objects.all()
        self.context['categories'] = categories
        return self.context
