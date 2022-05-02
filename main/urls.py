from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('create-ad/', create_ad, name='create_ad'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),

]
