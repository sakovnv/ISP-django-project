# Generated by Django 4.0.4 on 2022-05-03 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_ad_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='time_update',
            field=models.DateTimeField(auto_now=True, verbose_name='Время обновления'),
        ),
    ]