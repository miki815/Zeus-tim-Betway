from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [

    path('bonusi', bonusi, name='bonusi'),
    path('dodajutakmicu', dodajutakmicu, name='dodajutakmicu'),
    path('desetunizurez/<str:rezultat>', deset_u_nizu_rez, name='desetunizurez'),
    path('dodajutakmicu10', dodajutakmicu10, name='dodajutakmicu10'),
    path('prikaziaktivneutakmice', prikaziaktivneutakmice, name='prikaziaktivneutakmice'),  # dodato!
    path('ugasiutakmicu', ugasiutakmicu, name='ugasiutakmicu'),  #
    path('startujutakmicu', startujutakmicu, name='startujutakmicu'),  # dodato!
]
