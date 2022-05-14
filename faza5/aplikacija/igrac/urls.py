from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('<int:userId>', profil, name='profil'),
    path('desetunizu', deset_u_nizu, name='deset'),
    path('isplati', isplati, name='isplati'),

]
