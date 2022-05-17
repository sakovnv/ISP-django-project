from django.urls import path

from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('create-ad/', CreateAd.as_view(), name='create_ad'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('ad/<int:ad_id>', ad_view, name='ad'),
    path('ad/<pk>/edit/', EditAd.as_view(), name='edit_ad'),
    path('ad/<pk>/delete/', DeleteAd.as_view(), name='delete_ad'),
    path('category/<slug:category_slug>/', CategoryAds.as_view(), name='category_ads'),
    path('subscribe_category/', subscribe_category, name='subscribe_category')

]
