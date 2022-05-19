from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [

    path('bonusi', bonusi, name='bonusi'),
    path('dodajutakmicu', dodajutakmicu, name='dodajutakmicu'),
    path('desetunizurez/<str:rezultat>', deset_u_nizu_rez, name='desetunizurez'),
]
