from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    ads_count = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = verbose_name


class Ad(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(blank=False, verbose_name='Описание')
    cost = models.IntegerField(verbose_name='Стоимость')
    category = models.ForeignKey("Category", on_delete=models.PROTECT, verbose_name='Категория')
    phone = models.CharField(max_length=32, verbose_name='Номер телефона')
    image = models.ImageField(upload_to=f"images/{title}/", verbose_name='Изображения', null=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    author = models.ForeignKey("User", on_delete=models.PROTECT, verbose_name='Автор', null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ad', kwargs={'ad_id': self.pk})

    class Meta:
        verbose_name = 'Объявления'
        verbose_name_plural = verbose_name
