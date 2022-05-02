from django.forms import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *
from .utils import *


class CreateAdForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Выберите категорию"

    class Meta:
        model = Ad
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs=form_attr),
            'description': forms.Textarea(attrs=form_attr),
            'cost': forms.TextInput(attrs=form_attr),
            'category': forms.Select(attrs=form_attr),
            'phone': forms.TextInput(attrs=form_attr),
            'image': forms.FileInput(attrs={**form_attr, 'accept': 'image/*,image/jpeg', 'multiple': ''})
        }


class RegisterForm(UserCreationForm):

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs=form_attr))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs=form_attr))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs=form_attr))
    email = forms.CharField(label='Электронная почта', widget=forms.EmailInput(attrs=form_attr))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs=form_attr))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs=form_attr))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs=form_attr))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs=form_attr))
