from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [

    path('bonusi', bonusi, name='bonusi'),
    path('dodajutakmicu', dodajutakmicu, name='dodajutakmicu'),
]
