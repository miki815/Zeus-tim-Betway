from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('<int:userId>/napravikvote', napravikvote, name='napravikvote'),
    path('<int:userId>/prikaziaktivneutakmice', prikaziaktivneutakmice, name='prikaziaktivneutakmice'),
    path('<int:userId>/statistika', statistika, name='statistika'),
    path('<int:userId>/prikazisvetikete', prikazisvetikete, name='prikazisvetikete'),
    path('<int:userId>/postavivipkvotu', postavivipkvotu, name='postavivipkvotu'),
]
